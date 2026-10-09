import os
from . import HardwareDetector


def read_file(filepath):
    """Reads the first line of a file. Returns None if the file is not found."""
    try:
        with open(filepath) as f:
            return f.readline().strip()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    return None


def get_interface_info(device_path):
    info = {"driver_link": "", "interface_id": "", "modalias_id": ""}
    if not os.path.isdir(device_path):
        return info

    # Scan interfaces
    for device_file in os.listdir(device_path):
        if ":" in device_file:
            iface_dir = os.path.join(device_path, device_file)
            if not os.path.isdir(iface_dir):
                continue

            driver_link_path = os.path.join(iface_dir, "driver")
            # MODALIAS=usb:v048Dp600Bd0003dc00dsc00dp00ic03isc00ip00in01
            modalias_id = read_file(os.path.join(iface_dir, "modalias"))
            # Read interface class subclass protocol if exist
            i_class = ""
            i_subclass = ""
            i_protocol = ""
            if modalias_id and "ic" in modalias_id:
                ic_index = modalias_id.index("ic")
                i_class = modalias_id[ic_index + 2 :][0:2]
                if len(modalias_id) >= ic_index + 9:
                    i_subclass = modalias_id[ic_index + 7 :][0:2]
                if len(modalias_id) >= ic_index + 13:
                    i_protocol = modalias_id[ic_index + 11 :][0:2]

            if i_class and i_class != "FF" and i_class != "FE":
                info["driver_link"] = driver_link_path
                info["interface_id"] = (
                    i_class + " " + i_subclass + " " + i_protocol
                ).strip()
                info["modalias_id"] = modalias_id or ""

                return info

    return info


def get_sys_bus_uevent():
    """
    Reads USB device information such as driver, vendor, product, and class_id
    from /sys/bus/usb/devices

    Returns:
        list: A list of dictionaries containing driver, vendor, product, and class_id
    """
    dev_path = "/sys/bus/usb/devices"
    infos = []

    if not os.path.exists(dev_path):
        return infos  # Return empty list if path doesn't exist

    for entry in os.listdir(dev_path):
        if ":" in entry:
            continue  # Skip interface subdirectories like 1-8:1.0
        if "usb" in entry:
            continue  # Skip interface subdirectories like usb1, usb2
        device_path = os.path.join(dev_path, entry)

        vendor_id = read_file(os.path.join(device_path, "idVendor"))
        product_id = read_file(os.path.join(device_path, "idProduct"))
        dev_class = read_file(os.path.join(device_path, "bDeviceClass"))
        dev_protocol = read_file(os.path.join(device_path, "bDeviceProtocol"))
        dev_subclass = read_file(os.path.join(device_path, "bDeviceSubClass"))
        busnum = read_file(os.path.join(device_path, "busnum"))
        devnum = read_file(os.path.join(device_path, "devnum"))

        product_file = os.path.join(device_path, "product")
        product = None
        if os.path.exists(product_file):
            product = read_file(product_file)

        # Construct the interface directory name (e.g., 1-8:1.0)
        # Scan interfaces:
        interface_info = get_interface_info(device_path)
        driver_link_path = interface_info["driver_link"]

        driver = None
        if os.path.exists(driver_link_path):
            try:
                driver = os.readlink(driver_link_path).split("/")[-1]
            except OSError as e:
                print(f"Failed to read symlink: {driver_link_path} → {e}")

        class_id_str = " ".join([c for c in [dev_class, dev_protocol, dev_subclass] if c])

        # Create a fresh dictionary per device
        info = {
            "driver": driver,
            "vendor_id": vendor_id,
            "product_id": product_id,
            "modalias_id": interface_info["modalias_id"],
            "class_id": class_id_str,
            "interface_id": interface_info["interface_id"],
            "product": product,
            "busnum": busnum,
            "devnum": devnum,
        }

        infos.append(info)

    return infos


def get_hid_input_name(input_path):
    name_path = os.path.join(input_path, "name")
    if not os.path.exists(name_path):
        return ""

    try:
        with open(name_path, "r") as f:
            return f.read()
    except Exception:
        return ""


def get_hid_input_type(input_path):
    modalias_path = os.path.join(input_path, "modalias")
    if not os.path.exists(modalias_path):
        return ""

    data = read_file(modalias_path)
    if not data or "-" not in data:
        return ""

    try:
        capabilities = data.split("-")[1]
        events = []
        keys = []
        others = []

        current_arr = events
        current_value = ""
        for c in capabilities:
            if c == ",":
                current_arr.append(current_value)
                current_value = ""
                continue

            if c.islower() and c.isalpha():
                if c == "e":
                    current_arr = events
                elif c == "k":
                    current_arr = keys
                else:
                    current_arr = others
            else:
                current_value += c
        if current_value:
            current_arr.append(current_value)

        BTN_TOUCH = "14A" in keys  # touch support
        BTN_RIGHT = "111" in keys  # mouse right click
        EV_REL = "2" in events  # mouse, relative movement
        EV_REP = (
            "14" in events
        )  # keyboard detection, repeat key strokes on pressed down

        if BTN_TOUCH:
            if BTN_RIGHT:
                return "touchpad"
            else:
                return "touchscreen"
        elif BTN_RIGHT and EV_REL:
            return "mouse"
        elif EV_REP:
            return "keyboard"
    except Exception:
        pass

    return ""


hid_devices = []


def get_hid_devices():
    global hid_devices
    if hid_devices:
        return hid_devices

    dev_path = "/sys/bus/hid/devices"

    if not os.path.exists(dev_path):
        return hid_devices  # Return empty list if path doesn't exist

    for entry in os.listdir(dev_path):
        device_path = os.path.join(dev_path, entry)

        # Create a fresh dictionary per device
        info = {
            "name": "",
            "driver": "",
            "vendor_id": "",
            "product_id": "",
            "bus": "",
            "bus_address": "",
            "type": "",
            "input_device": "",
        }

        # Base HID device informations
        uevent_file = os.path.join(device_path, "uevent")
        if os.path.isfile(uevent_file):
            try:
                with open(uevent_file, "r") as f:
                    data = f.read()
                    for line in data.splitlines():
                        if "=" not in line:
                            continue
                        key, value = line.split("=", 1)
                        if key == "DRIVER":
                            info["driver"] = value
                        elif key == "HID_NAME":
                            info["name"] = value
                        elif key == "HID_ID":
                            parts = value.split(":")
                            if len(parts) == 3:
                                bus, vendor, product = parts
                                try:
                                    info["bus_address"] = f"0x{int(bus, base=16):01X}"
                                    info["vendor_id"] = f"0x{int(vendor, base=16):01X}"
                                    info["product_id"] = f"0x{int(product, base=16):01X}"
                                except ValueError:
                                    pass
                        elif key == "HID_PHYS":
                            if "usb-" in value:
                                info["bus"] = "usb"
                            elif "i2c-" in value:
                                info["bus"] = "i2c"
                            elif len(value.split(":")) == 6 and len(value) == 17:
                                info["bus"] = "bluetooth"
            except Exception:
                pass

        # is input device? (mouse, keyboard, touch)
        input_dir = os.path.join(device_path, "input")
        if os.path.exists(input_dir):
            for input_device in os.listdir(input_dir):
                info_input = info.copy()
                input_device_path = os.path.join(input_dir, input_device)

                # Get Type and name
                input_type = get_hid_input_type(input_device_path)
                input_name = get_hid_input_name(input_device_path).strip()

                if input_name:
                    info_input["name"] = input_name

                if input_type != "":
                    info_input["type"] = input_type
                    info_input["input_device"] = input_device

                    hid_devices.append(info_input)

    return hid_devices


def match_class_with_category(class_id):
    if not class_id:
        return None
    device_classes = {
        "02": "ethernet",
        "01": "audio",
        "e0 01 01": "bluetooth",
        "ef 01": "camera",
        "0e": "camera",
        "ff ff": "fingerprint",
        "e0 02": "wifi",
        "2c 06": "ethernet",
        "07": "printer",
    }

    for key, value in device_classes.items():
        if class_id.startswith(key):
            return value
    return None


def match_driver_with_category(driver):
    if not driver:
        return None
    device_classes = {
        "btusb": "bluetooth",
        "uvcvideo": "camera",
        "cdc_ether": "ethernet",
    }

    if driver in device_classes:
        return device_classes[driver]

    return None


usb_devices = None


def is_hid_device(usb):
    def match(var1, var2):
        if not var1 or not var2:
            return False
        v1 = str(var1).lower()
        v2 = str(var2).lower()
        if not v1.startswith("0x"):
            v1 = "0x" + v1
        if not v2.startswith("0x"):
            v2 = "0x" + v2
        return v1 == v2

    usb_vendor = usb.get("vendor_id")
    usb_product = usb.get("product_id")
    for hid in get_hid_devices():
        if match(hid.get("vendor_id"), usb_vendor) and match(hid.get("product_id"), usb_product):
            return True
    return False


def get_usb_devices():
    global usb_devices
    if usb_devices:
        return usb_devices

    dev_info = get_sys_bus_uevent()

    data = {}
    for usb in dev_info:
        if usb.get("class_id", "").startswith("09"):
            # USB BUS, Skip
            continue

        class_category = match_class_with_category(usb.get("class_id", ""))
        driver_category = match_driver_with_category(usb.get("driver", ""))
        interface_category = match_class_with_category(usb.get("interface_id", ""))

        if driver_category:
            category = driver_category
        elif class_category:
            category = class_category
        elif interface_category:
            category = interface_category
        elif is_hid_device(usb):
            category = "usb-hid"
        else:
            category = "usb"

        if category not in data:
            data[category] = []

        modalias = usb.get("modalias_id", "")
        available_drivers = HardwareDetector.find_drivers(modalias) if modalias else []
        vendor_id = usb.get("vendor_id") or ""
        product_id = usb.get("product_id") or ""
        vendor, name = HardwareDetector.get_vendor_product_name("usb", vendor_id, product_id)

        vendor_upper = vendor_id.upper()
        product_upper = product_id.upper()

        if name is None or vendor is None:
            vendor_text = f"usb:v{vendor_upper}*\n ID_VENDOR_FROM_DATABASE="
            product_text = (
                f"usb:v{vendor_upper}p{product_upper}*\n ID_MODEL_FROM_DATABASE="
            )

            vendor, name = HardwareDetector.get_vendor_product_name_from_udev(
                "usb", vendor_text, product_text
            )

        if name is None:
            name = usb.get("product") or ""

        device_id = f"{vendor_upper}:{product_upper}"

        try:
            busnum = f"{int(usb.get('busnum', 0)):04}"
        except (TypeError, ValueError):
            busnum = "0000"

        try:
            devnum = f"{int(usb.get('devnum', 0)):04}"
        except (TypeError, ValueError):
            devnum = "0000"

        bus_address = f"{busnum}:{devnum}"

        if not vendor:
            vendor = ""

        # Big corp renaming:
        if "INTEL" in vendor.upper():
            vendor = "Intel"

        device = {
            "device_id": device_id,
            "name": name,
            "vendor": vendor,
            "driver": usb.get("driver") or "",
            "available_drivers": available_drivers,
            "bus": "usb",
            "bus_address": bus_address,
        }

        for k in device.keys():
            if device[k] is None:
                device[k] = ""

        data[category].append(device)

    usb_devices = data
    return usb_devices
