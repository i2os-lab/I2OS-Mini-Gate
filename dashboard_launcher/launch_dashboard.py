import argparse
import json
import subprocess
import sys
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from i2os_gate import i2os_gate, load_policy, save_json_report, save_markdown_report, save_html_report


def load_action(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def launch_dashboard(action_path, policy_path=None, report_prefix="dashboard_scan", open_browser=False):
    action = load_action(action_path)
    policy = load_policy(policy_path)

    result = i2os_gate(action, policy=policy)

    save_json_report(result, f"{report_prefix}.json")
    save_markdown_report(result, f"{report_prefix}.md")
    save_html_report(result, f"{report_prefix}.html")

    html_path = ROOT / "dashboard" / f"{report_prefix}.html"

    output = {
        "decision": result["decision"],
        "risk_level": result["risk_level"],
        "html_report": str(html_path),
        "json_report": str(ROOT / "reports" / f"{report_prefix}.json"),
        "markdown_report": str(ROOT / "reports" / f"{report_prefix}.md"),
    }

    if open_browser:
        webbrowser.open(html_path.as_uri())

    return output


def main():
    parser = argparse.ArgumentParser(description="I2OS Dashboard Launcher")
    parser.add_argument("--action", required=True, help="Action JSON file")
    parser.add_argument("--policy", default=None, help="Policy JSON file")
    parser.add_argument("--report-prefix", default="dashboard_scan", help="Output report prefix")
    parser.add_argument("--open", action="store_true", help="Open generated HTML dashboard in browser")
    parser.add_argument("--json", action="store_true", help="Print JSON output")
    args = parser.parse_args()

    output = launch_dashboard(
        action_path=args.action,
        policy_path=args.policy,
        report_prefix=args.report_prefix,
        open_browser=args.open,
    )

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("=== I2OS Dashboard Launcher ===")
        print(f"Decision: {output['decision']}")
        print(f"Risk: {output['risk_level']}")
        print(f"HTML: {output['html_report']}")
        print(f"JSON: {output['json_report']}")
        print(f"Markdown: {output['markdown_report']}")


if __name__ == "__main__":
    main()
