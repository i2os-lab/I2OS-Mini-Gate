"""Policy profile helper paths."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = ROOT / "policy"

STRICT_POLICY = POLICY_DIR / "strict_policy.json"
BALANCED_POLICY = POLICY_DIR / "balanced_policy.json"
PERMISSIVE_POLICY = POLICY_DIR / "permissive_policy.json"

PROFILES = {
    "strict": STRICT_POLICY,
    "balanced": BALANCED_POLICY,
    "permissive": PERMISSIVE_POLICY,
}

__all__ = [
    "STRICT_POLICY",
    "BALANCED_POLICY",
    "PERMISSIVE_POLICY",
    "PROFILES",
]
