"""Tests for offline report PDF export."""
from __future__ import annotations

import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import report_pdf

sys.path.insert(0, str(Path(__file__).resolve().parent))


class ReportPdfUnitTests(unittest.TestCase):
    def test_default_path_uses_report_folder_and_stem(self):
        self.assertEqual(
            report_pdf.default_pdf_path(Path("reports/example.html")),
            Path("reports/example.pdf"),
        )

    def test_missing_playwright_has_install_hint(self):
        with mock.patch.dict("sys.modules", {"playwright.sync_api": None}):
            with tempfile.TemporaryDirectory() as folder:
                source = Path(folder) / "report.html"
                source.write_text("<title>Report</title>", encoding="utf-8")
                with self.assertRaisesRegex(report_pdf.ReportExportError, "playwright install chromium"):
                    report_pdf.export_report_pdf(source)

    def test_cli_missing_file_returns_two_with_one_line(self):
        with mock.patch("sys.stderr") as stderr:
            result = report_pdf.main(["missing.html"])
        self.assertEqual(result, 2)
        self.assertIn("HTML report not found", str(stderr.write.call_args_list))


class ReportPdfBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.environ.get("SKIP_BROWSER_TESTS") == "1":
            raise unittest.SkipTest("SKIP_BROWSER_TESTS=1")
        # Only probe that Chromium can launch, then shut Playwright down again:
        # export_report_pdf starts its own sync session, and two cannot overlap.
        try:
            from browser_test_helpers import launch_browser, load_playwright

            sync_playwright, _ = load_playwright()
            with sync_playwright() as playwright:
                launch_browser(playwright).close()
        except Exception as exc:
            raise unittest.SkipTest(f"Playwright Chromium unavailable: {exc}") from exc

    def test_static_table_exports_as_single_page_pdf(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "synthetic-risk-summary.html"
            source.write_text(
                """<!doctype html><html><head><title>Synthetic Risk Summary</title>
                <style>body{font:14px sans-serif}table{border-collapse:collapse}td{padding:8px;border:1px solid #444}</style>
                </head><body><h1>Synthetic Risk Summary</h1><table><tr><th>Portfolio</th><th>Regime</th></tr>
                <tr><td>TEST-PORTFOLIO</td><td>Normal</td></tr></table></body></html>""",
                encoding="utf-8",
            )
            output = report_pdf.export_report_pdf(source, layout="single")
            payload = output.read_bytes()
            self.assertTrue(payload.startswith(b"%PDF-"))
            self.assertRegex(payload, rb"/Count\s+1\b")
            self.assertRegex(payload, rb"/Title\s*\(Synthetic Risk Summary\)")

    def test_external_script_is_blocked_and_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "cdn.html"
            source.write_text(
                '<html><head><title>CDN test</title><script src="https://cdn.plot.ly/plotly.js"></script></head></html>',
                encoding="utf-8",
            )
            with self.assertRaisesRegex(report_pdf.ReportExportError, "cdn.plot.ly"):
                report_pdf.export_report_pdf(source)


if __name__ == "__main__":
    unittest.main()
