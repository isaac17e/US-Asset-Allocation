"""Shared offline browser helpers for Plotly report tests."""
from __future__ import annotations

from urllib.parse import urlparse


def load_playwright():
    """Import the synchronous Playwright API only when a browser test runs."""
    from playwright.sync_api import expect, sync_playwright

    return sync_playwright, expect


def launch_browser(sync_playwright):
    """Launch Chromium with external name resolution disabled."""
    return sync_playwright.chromium.launch(
        args=[
            "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost, EXCLUDE 127.0.0.1"
        ]
    )


def install_offline_route(context, blocked_requests):
    """Allow local and embedded content while recording external requests."""
    def handle_route(route):
        url = route.request.url
        parsed = urlparse(url)
        if parsed.scheme in {"file", "data", "about"}:
            route.continue_()
        elif parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
            route.continue_()
        else:
            blocked_requests.append(url)
            route.abort()

    context.route("**/*", handle_route)


def collect_page_errors(page, page_errors, console_errors):
    """Collect page failures and console errors, ignoring favicon 404 noise."""
    page.on("pageerror", lambda error: page_errors.append(str(error)))

    def on_console(message):
        if message.type == "error" and "favicon.ico" not in message.text:
            console_errors.append(message.text)

    page.on("console", on_console)


def wait_for_plotly(page, expected_count):
    """Wait until the requested number of plots has rendered SVG content."""
    page.wait_for_function(
        "count => document.querySelectorAll('.js-plotly-plot svg.main-svg').length >= count",
        arg=expected_count,
        timeout=15000,
    )
