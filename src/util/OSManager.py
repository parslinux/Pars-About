import os
import subprocess
import socket
import platform

from util.desktop import get_desktop_version

import gi
gi.require_versions({'Gdk': '3.0'})
from gi.repository import GObject, Gdk


operating_system_info = None


def is_wayland():
    if "WAYLAND_DISPLAY" in os.environ or os.environ.get("XDG_SESSION_TYPE") == "wayland":
        return True
    try:
        display = Gdk.Display.get_default()
        if display is None:
            return False
        return type(display).__name__ == "WaylandDisplay"
    except Exception:
        return False

def get_os_info():
    global operating_system_info
    if operating_system_info:
        return operating_system_info

    operating_system_info = {}

    hostname = socket.gethostname()
    operating_system_info["hostname"] = hostname.capitalize()

    try:
        os_info = platform.freedesktop_os_release()
    except Exception:
        os_info = {}

    operating_system_info["os_pretty_name"] = str(os_info.get("PRETTY_NAME", ""))
    operating_system_info["os_name"] = str(os_info.get("NAME", ""))
    operating_system_info["os_id"] = str(os_info.get("ID", ""))
    operating_system_info["os_version"] = str(os_info.get("VERSION", ""))
    operating_system_info["os_version_id"] = str(os_info.get("VERSION_ID", ""))
    operating_system_info["os_codename"] = str(os_info.get("VERSION_CODENAME", ""))
    operating_system_info["kernel"] = platform.release()
    operating_system_info["architecture"] = platform.machine()

    operating_system_info["desktop"] = "Unknown"
    operating_system_info["desktop_version"] = "Unknown"
    operating_system_info["display"] = "x11"
    if "LANG" in os.environ:
        operating_system_info["language"] = os.environ["LANG"]
    if "XDG_CURRENT_DESKTOP" in os.environ:
        operating_system_info["desktop"] = os.environ["XDG_CURRENT_DESKTOP"]
        operating_system_info["desktop_version"] = get_desktop_version(os.environ["XDG_CURRENT_DESKTOP"])
    if is_wayland():
        operating_system_info["display"] = "wayland"

    operating_system_info["fstype"] = "Unknown"
    if os.path.isfile("/proc/mounts"):
        try:
            with open("/proc/mounts", "r") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) >= 3 and parts[1] == "/":
                        operating_system_info["fstype"] = parts[2]
                        break
        except Exception:
            pass

    return operating_system_info

