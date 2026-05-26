"""Report helper facade."""

from i2os_gate import save_json_report, save_markdown_report

try:
    from i2os_gate import save_html_report
except ImportError:  # pragma: no cover
    save_html_report = None

__all__ = ["save_json_report", "save_markdown_report", "save_html_report"]
