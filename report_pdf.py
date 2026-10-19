"""Offline HTML-to-PDF export for one-shot reports.

Kept identical in Portfolio-Manager, Options-Flow and US-Asset-Allocation:
change all three copies together.
"""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import sys
from pathlib import Path
import tempfile
from threading import Thread
from urllib.parse import quote


class ReportExportError(RuntimeError):
    """Raised when a report cannot be rendered as an offline PDF."""


def default_pdf_path(html_path):
    """Return the PDF path beside an HTML report."""
    return Path(html_path).with_suffix(".pdf")


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def export_report_pdf(
    html_path,
    pdf_path=None,
    *,
    layout="a4",
    landscape=False,
    viewport_width=1200,
    timeout_ms=30_000,
):
    """Render a local HTML report with network access disabled."""
    source = Path(html_path).resolve()
    if not source.is_file():
        raise ReportExportError(f"HTML report not found: {source}")
    if layout not in {"a4", "single"}:
        raise ReportExportError("layout must be 'a4' or 'single'")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise ReportExportError(
            "Playwright is required; install with: pip install playwright && "
            "python -m playwright install chromium"
        ) from exc

    handler = partial(_QuietHandler, directory=str(source.parent))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    blocked = []
    try:
        url = f"http://127.0.0.1:{server.server_port}/{quote(source.name)}"
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(args=[
                    "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost, EXCLUDE 127.0.0.1"
                ])
                context = browser.new_context(viewport={"width": viewport_width, "height": 900})
                try:
                    def route_request(route):
                        request_url = route.request.url
                        if request_url.startswith(("http://127.0.0.1", "http://localhost", "data:", "blob:", "about:")):
                            route.continue_()
                        else:
                            blocked.append(request_url)
                            route.abort()

                    context.route("**/*", route_request)
                    page = context.new_page()
                    page.goto(url, wait_until="load", timeout=timeout_ms)
                    plots = page.locator(".js-plotly-plot")
                    if plots.count():
                        page.wait_for_function(
                            "() => [...document.querySelectorAll('.js-plotly-plot')].every(gd => gd.querySelector('svg.main-svg'))",
                            timeout=timeout_ms,
                        )
                    page.evaluate("() => document.fonts.ready")
                    if blocked:
                        raise ReportExportError("External requests blocked: " + ", ".join(blocked))
                    page.add_style_tag(content="@media print { .card, section, .js-plotly-plot, table { break-inside: avoid; } }")
                    options = {"print_background": True}
                    if layout == "a4":
                        options.update(format="A4", landscape=landscape, margin={"top": "12mm", "bottom": "12mm", "left": "10mm", "right": "10mm"})
                    else:
                        height = page.evaluate("document.documentElement.scrollHeight") + 1
                        options.update(width=f"{viewport_width}px", height=f"{height}px")
                    pdf_bytes = page.pdf(**options)
                    if blocked:
                        raise ReportExportError("External requests blocked: " + ", ".join(blocked))
                finally:
                    # Close while the Playwright session is still running.
                    context.close()
                    browser.close()
        except ReportExportError:
            raise
        except Exception as exc:
            raise ReportExportError(f"Chromium PDF export failed: {exc}") from exc

        target = Path(pdf_path) if pdf_path else default_pdf_path(source)
        target = target.resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        try:
            with os.fdopen(fd, "wb") as output:
                output.write(pdf_bytes)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return target
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def main(argv=None):
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Export an offline HTML report as PDF")
    parser.add_argument("html")
    parser.add_argument("--out")
    parser.add_argument("--layout", choices=("a4", "single"), default="a4")
    parser.add_argument("--landscape", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = export_report_pdf(args.html, args.out, layout=args.layout, landscape=args.landscape)
    except ReportExportError as exc:
        print(f"PDF export failed: {exc}", file=sys.stderr)
        return 2
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
