import os
from . import HardwareDetector


def parse_uevent_file(uevent_path):
    data = {"driver": "", "class_id": "", "pci_id": "", "modalias_id": "", "pci_slot_name": ""}

    try:
        with open(uevent_path) as uevent_file:
            for line in uevent_file:
                if "=" not in line:
                    continue
                key, value = line.strip().split("=", 1)
                if key == "DRIVER":
                    data["driver"] = value
                elif key == "PCI_CLASS":
                    data["class_id"] = value
                elif key == "PCI_ID":
                    data["pci_id"] = value
                elif key == "MODALIAS":
                    data["modalias_id"] = value
                elif key == "PCI_SLOT_NAME":
                    data["pci_slot_name"] = value
    except Exception as e:
        print(f"Error reading uevent file {uevent_path}: {e}")
    return data


def get_sys_bus_uevent():
    dev_path = "/sys/bus/pci/devices"
    info_list = []

    if not os.path.exists(dev_path):
        return info_list

    for dir in os.listdir(dev_path):
        uevent_file = os.path.join(dev_path, dir, "uevent")
        if os.path.isfile(uevent_file):
            info = parse_uevent_file(uevent_file)
            info_list.append(info)

    return info_list


def match_class_with_category(class_id):
    if not class_id:
        return None
    normalized = str(class_id).lower()
    if normalized.startswith("0x"):
        normalized = normalized[2:]
    normalized = normalized.lstrip("0")

    device_classes = {"28": "wifi", "3": "graphics", "4": "audio", "20": "ethernet"}

    for key, value in device_classes.items():
        if normalized.startswith(key):
            return value

    return None


pci_devices = None


def get_pci_devices():
    global pci_devices
    if pci_devices:
        return pci_devices

    dev_info = get_sys_bus_uevent()

    data = {}

    for pci in dev_info:
        category = match_class_with_category(pci.get("class_id", ""))
        if not category:
            category = "pci"

        if category not in data:
            data[category] = []

        modalias = pci.get("modalias_id") or ""
        available_drivers = HardwareDetector.find_drivers(modalias) if modalias else []
        pci_id = pci.get("pci_id") or ""

        vendor_id, product_id = "", ""
        if ":" in pci_id:
            parts = pci_id.lower().split(":", 1)
            vendor_id, product_id = parts[0], parts[1]

        vendor, name = None, None
        if vendor_id and product_id:
            vendor, name = HardwareDetector.get_vendor_product_name(
                "pci", vendor_id, product_id
            )
        if modalias and (name is None or vendor is None):
            if "d" in modalias and "s" in modalias:
                vendor_text = (
                    modalias.split("d")[0] + "*" + "\n ID_VENDOR_FROM_DATABASE="
                )
                product_text = (
                    modalias.split("s")[0] + "*" + "\n ID_MODEL_FROM_DATABASE="
                )

                vendor, name = HardwareDetector.get_vendor_product_name_from_udev(
                    "pci", vendor_text, product_text
                )

        bus_address = pci.get("pci_slot_name", "")

        # Vendor renaming:
        if vendor is None:
            vendor = ""
        if "INTEL" in vendor.upper():
            vendor = "Intel"

        device = {
            "device_id": pci_id,
            "name": name or "",
            "vendor": vendor,
            "driver": pci.get("driver") or "",
            "available_drivers": available_drivers,
            "bus": "pci",
            "bus_address": bus_address,
        }

        for k in device.keys():
            if device[k] is None:
                device[k] = ""

        data[category].append(device)

    pci_devices = data
    return pci_devices
