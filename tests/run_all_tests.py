#!/usr/bin/env python3
import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if os.path.join(PROJECT_ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))


def main():
    print("=" * 60)
    print("  Pars About — Test Paketi Doğrulama (Test Suite)")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=TESTS_DIR, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("-" * 60)
    print(f"Toplam Test     : {result.testsRun}")
    print(f"Başarılı        : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Hatalar (Errors): {len(result.errors)}")
    print(f"Başarısız (Fail): {len(result.failures)}")
    print("=" * 60)

    if result.wasSuccessful():
        print("TÜM TESTLER BAŞARIYLA GEÇTİ! [OK]")
        return 0
    else:
        print("BAZI TESTLER BAŞARISIZ OLDU! [FAILED]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
