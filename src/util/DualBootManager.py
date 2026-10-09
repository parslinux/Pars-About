import os
import subprocess
import json


def list_parts():
    ret = []
    if not os.path.exists("/sys/block"):
        return ret
    for disk in os.listdir("/sys/block"):
        disk_path = f"/sys/block/{disk}"
        if not os.path.isdir(disk_path):
            continue
        for part in os.listdir(disk_path):
            if not part.startswith(disk):
                continue
            ret.append(part)
    return ret


def get_root_part():
    if not os.path.isfile("/proc/mounts"):
        return None
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2 and parts[1] == "/":
                    return parts[0]
    except Exception:
        pass
    return None


win_table = {
    "10.": "10",
    "6.4": "10",
    "6.3": "8.1",
    "6.2": "8",
    "6.1": "7",
    "6.0": "Vista",
    "5.2": "XP Pro x64",
    "5.1": "XP",
    "5.0": "2000",
    "4.9": "ME",
    "4.1": "98",
    "4.0": "95",
}


def get_windows_version():
    if not os.path.isdir("/run/winroot/Windows/servicing/Version"):
        return ""
    for item in os.listdir("/run/winroot/Windows/servicing/Version"):
        if len(item) < 3:
            continue
        item = item[:3]
        if item in win_table.keys():
            return win_table[item]
    return ""


def get_dualboot_oses():
    dualboot = {}
    try:
        os.makedirs("/run/winroot", exist_ok=True)
        os.chown("/run/winroot", 0, 0)
        os.chmod("/run/winroot", 0o700)
    except Exception as e:
        print("Failed to prepare /run/winroot:", e)
        return json.dumps(dualboot)

    root_part = get_root_part()
    for part in list_parts():
        if f"/dev/{part}" == root_part:
            continue
        sp = subprocess.run(
            ["mount", "-o", "ro,nosuid,nodev,noexec", f"/dev/{part}", "/run/winroot"],
            capture_output=True,
        )
        if 0 == sp.returncode:
            # Windows
            if os.path.exists("/run/winroot/Windows/System32/ntoskrnl.exe"):
                dualboot[part] = "Windows " + get_windows_version()
            # Mac OS X
            if os.path.exists(
                "/run/winroot/System/Library/CoreServices/SystemVersion.plist"
            ):
                dualboot[part] = "Mac OS X"
            # Linux
            if os.path.exists("/run/winroot/etc/os-release"):
                try:
                    with open("/run/winroot/etc/os-release", "r") as f:
                        for line in f.read().splitlines():
                            if line.startswith("NAME="):
                                name_val = line.split("=", 1)[1].strip('"\'')
                                dualboot[part] = name_val
                                break
                except Exception:
                    pass
            os.system("umount -lf /run/winroot")

    try:
        os.rmdir("/run/winroot")
    except Exception:
        pass
    return json.dumps(dualboot)


if __name__ == "__main__":
    print(get_dualboot_oses())
