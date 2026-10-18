import glob
import os
import shutil
import subprocess
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PO_DIR = os.path.join(PROJECT_ROOT, "po")


class TestTranslations(unittest.TestCase):
    def test_po_files_exist(self):
        """Test that po files exist for supported languages."""
        po_files = glob.glob(os.path.join(PO_DIR, "*.po"))
        self.assertTrue(len(po_files) > 0, "No .po translation files found in po/")
        basenames = [os.path.basename(p) for p in po_files]
        self.assertIn("tr.po", basenames, "Missing tr.po translation")

    def test_msgfmt_validation(self):
        """Test that msgfmt validates each .po file without syntax errors."""
        msgfmt = shutil.which("msgfmt")
        if not msgfmt:
            self.skipTest("msgfmt command not available on this system")

        po_files = glob.glob(os.path.join(PO_DIR, "*.po"))
        for po in po_files:
            with self.subTest(po=os.path.basename(po)):
                res = subprocess.run(
                    [msgfmt, "-c", "-v", po, "-o", "/dev/null"],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(
                    res.returncode,
                    0,
                    f"msgfmt error in {os.path.basename(po)}: {res.stderr}",
                )


if __name__ == "__main__":
    unittest.main()
