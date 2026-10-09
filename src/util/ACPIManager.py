import os


def is_acpi_supported():
    """Requires root permission. Use only in Actions.py with pkexec."""
    path = "/sys/firmware/acpi/tables/DSDT"
    if not os.path.isfile(path):
        return False
    try:
        with open(path, "rb") as f:
            return "linux" in str(f.read()).lower()
    except Exception:
        return False
