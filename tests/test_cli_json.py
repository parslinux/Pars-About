import json
import os
import subprocess
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCLIJson(unittest.TestCase):
    def test_json_flag_stdout_validity(self):
        """Test that --json produces valid JSON output and exits with 0."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "pars-about.py"), "--json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        self.assertEqual(
            proc.returncode, 0, f"pars-about --json failed with error: {proc.stderr}"
        )

        try:
            data = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            self.fail(f"Output is not valid JSON: {e}\nOutput was: {proc.stdout[:200]}")

        self.assertIsInstance(data, dict)
        # Should have at least one of processor, memory, os, storage
        expected_keys = {"processor", "memory", "os", "storage"}
        present = expected_keys.intersection(data.keys())
        self.assertTrue(len(present) > 0, f"Expected keys {expected_keys} in {data.keys()}")

    def test_short_j_flag(self):
        """Test that -j short flag works equivalently."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "pars-about.py"), "-j"]
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT)
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertIsInstance(data, dict)

    def test_headless_no_display(self):
        """Test that --json runs completely headless without DISPLAY variable."""
        cmd = [sys.executable, os.path.join(PROJECT_ROOT, "pars-about.py"), "--json"]
        env = os.environ.copy()
        env.pop("DISPLAY", None)
        env.pop("WAYLAND_DISPLAY", None)

        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=PROJECT_ROOT, env=env)
        self.assertEqual(
            proc.returncode,
            0,
            f"Headless execution without DISPLAY failed: {proc.stderr}",
        )
        data = json.loads(proc.stdout)
        self.assertIsInstance(data, dict)


if __name__ == "__main__":
    unittest.main()
