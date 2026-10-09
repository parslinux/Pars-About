import os


def get_serio_devices():
    def _read_file(path):
        if os.path.isfile(path):
            try:
                with open(path, "r") as f:
                    return f.read().strip()
            except Exception:
                pass
        return ""

    data = {"mouse": [], "keyboard": []}
    serio_path = "/sys/bus/serio/devices"
    if not os.path.exists(serio_path):
        return data

    for dev in os.listdir(serio_path):
        dev_name = dev
        dev_dir = f"{serio_path}/{dev}"
        if not os.path.isdir(dev_dir):
            continue

        input_dir = f"{dev_dir}/input"
        if not os.path.exists(input_dir):
            continue

        driver = ""
        driver_symlink = f"{dev_dir}/driver"
        if os.path.exists(driver_symlink):
            try:
                driver = os.readlink(driver_symlink).split("/")[-1]
            except OSError:
                driver = ""

        try:
            for finput in os.listdir(input_dir):
                if not finput.startswith("input"):
                    continue

                info = {
                    "name": _read_file(f"{input_dir}/{finput}/name"),
                    "vendor_id": _read_file(f"{input_dir}/{finput}/id/vendor"),
                    "product_id": _read_file(f"{input_dir}/{finput}/id/product"),
                    "driver": driver,
                    "bus": "serio",
                    "bus_address": dev_name,
                    "input_device": finput,
                }

                if driver == "psmouse":
                    data["mouse"].append(info)
                else:
                    data["keyboard"].append(info)
        except Exception as e:
            print("Error scanning serio inputs:", e)

    return data


if __name__ == "__main__":
    print(get_serio_devices())
