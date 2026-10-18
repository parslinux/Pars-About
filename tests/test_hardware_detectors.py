import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from util import ComputerManager, OSManager, DiskManager, PCIManager, USBManager, desktop, HostnameManager


class TestHardwareDetectors(unittest.TestCase):
    def test_os_manager(self):
        """Test OSManager returns distribution details."""
        os_info = OSManager.get_os_info()
        self.assertIsInstance(os_info, dict)
        self.assertIn("os_id", os_info)
        self.assertIn("kernel", os_info)

    def test_desktop_version_helper(self):
        """Test desktop version parsing helper."""
        ver = desktop.get_desktop_version("xfce")
        self.assertIsInstance(ver, str)

    def test_hostname_manager(self):
        """Test HostnameManager returns valid hostname."""
        hostname = HostnameManager.get_hostname()
        self.assertIsInstance(hostname, str)
        self.assertTrue(len(hostname) > 0)

    def test_computer_manager_aggregation(self):
        """Test ComputerManager collects aggregated system dictionary."""
        manager = ComputerManager.ComputerManager()
        all_info = manager.get_all_device_info()
        self.assertIsInstance(all_info, dict)

    def test_pci_manager(self):
        """Test PCIManager parses PCI devices into categories."""
        devices = PCIManager.get_pci_devices()
        self.assertIsInstance(devices, dict)
        self.assertIn("pci", devices)
        self.assertIsInstance(devices["pci"], list)

    def test_usb_manager(self):
        """Test USBManager parses USB devices into categories."""
        devices = USBManager.get_usb_devices()
        self.assertIsInstance(devices, dict)
        self.assertIn("usb", devices)
        self.assertIsInstance(devices["usb"], list)

    def test_disk_manager(self):
        """Test DiskManager parses disks."""
        disks = DiskManager.get_disks()
        self.assertIsInstance(disks, list)


if __name__ == "__main__":
    unittest.main()
