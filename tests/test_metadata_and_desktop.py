import os
import unittest
import xml.etree.ElementTree as ET

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestMetadataAndDesktop(unittest.TestCase):
    def test_main_desktop_file(self):
        """Test org.parslinux.about.desktop contains mandatory XDG fields."""
        desktop_path = os.path.join(PROJECT_ROOT, "org.parslinux.about.desktop")
        self.assertTrue(os.path.exists(desktop_path), "Missing org.parslinux.about.desktop")

        with open(desktop_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Exec=pars-about", content)
        self.assertIn("Icon=pars-about", content)
        self.assertIn("Name=About Pars", content)
        self.assertIn("Name[tr]=Pars Linux Hakkında", content)
        self.assertIn("Categories=", content)

    def test_hardware_desktop_file(self):
        """Test org.parslinux.about-hardware.desktop contains mandatory XDG fields."""
        desktop_path = os.path.join(PROJECT_ROOT, "org.parslinux.about-hardware.desktop")
        self.assertTrue(os.path.exists(desktop_path), "Missing org.parslinux.about-hardware.desktop")

        with open(desktop_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("[Desktop Entry]", content)
        self.assertIn("Exec=pars-about --hardware", content)
        self.assertIn("Icon=pars-hardware-info", content)
        self.assertIn("Name=Pars Hardware Information", content)

    def test_metainfo_xml_validity(self):
        """Test that data/org.parslinux.about.metainfo.xml is valid XML and has required AppStream tags."""
        metainfo_path = os.path.join(PROJECT_ROOT, "data", "org.parslinux.about.metainfo.xml")
        self.assertTrue(os.path.exists(metainfo_path), "Missing metainfo XML file")

        tree = ET.parse(metainfo_path)
        root = tree.getroot()
        self.assertEqual(root.tag, "component")
        self.assertEqual(root.attrib.get("type"), "desktop-application")

        id_elem = root.find("id")
        self.assertIsNotNone(id_elem)
        self.assertEqual(id_elem.text, "org.parslinux.about")

    def test_polkit_policy_xml_validity(self):
        """Test that policy file is valid XML."""
        policy_path = os.path.join(
            PROJECT_ROOT, "polkit", "org.parslinux.pkexec.pars-about.policy"
        )
        self.assertTrue(os.path.exists(policy_path), "Missing polkit policy file")

        tree = ET.parse(policy_path)
        root = tree.getroot()
        self.assertEqual(root.tag, "policyconfig")

        vendor = root.find("vendor")
        self.assertIsNotNone(vendor)
        self.assertEqual(vendor.text, "Pars Linux Developers")


if __name__ == "__main__":
    unittest.main()
