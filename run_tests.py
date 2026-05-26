import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TESTS_DIR = ROOT / "tests"

print("[I2OS] Running unit tests...")

if not TESTS_DIR.exists():
    print("[I2OS] tests directory not found. Skipping unit tests.")
    sys.exit(0)

result = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
    cwd=str(ROOT)
)

if result.returncode == 0:
    print("[I2OS] All tests passed.")
else:
    print("[I2OS] Tests failed.")

sys.exit(result.returncode)
