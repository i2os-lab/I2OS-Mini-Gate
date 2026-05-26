"""Package CLI entry point for I2OS Mini Gate.

Usage:
  python -m i2os_mini_gate --action examples/audit_block_prompt_injection.json
"""

import sys

from i2os_gate import main as legacy_main


def main():
    legacy_main()


if __name__ == "__main__":
    main()
