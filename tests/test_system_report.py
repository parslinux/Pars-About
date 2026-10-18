import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from util import SystemReportManager


class TestSystemReport(unittest.TestCase):
    def test_archive_directory_path(self):
        """Test that ARCHIVE_DIR points to /tmp/pars_system_report."""
        self.assertEqual(SystemReportManager.ARCHIVE_DIR, "/tmp/pars_system_report")

    def test_detect_pkexec_user(self):
        """Test pkexec user detection returns valid string."""
        user = SystemReportManager.detect_pkexec_user()
        self.assertIsInstance(user, str)
        self.assertTrue(len(user) > 0)


if __name__ == "__main__":
    unittest.main()
