from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
BASE_VARS = ("MASSIVE_API_BASE", "POLYGON_API_BASE", "MASSIVE_WS_BASE")


def _load_manager(env: dict[str, str] | None = None):
    supplied = env or {}
    with mock.patch.dict("os.environ", supplied, clear=False) as patched:
        for name in BASE_VARS:
            if name not in supplied:
                patched.pop(name, None)
        spec = importlib.util.spec_from_file_location("us_asset_manager_massive", ROOT / "US Asset Manager.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules["us_asset_manager_massive"] = module
        try:
            with mock.patch("dotenv.load_dotenv", return_value=None):
                spec.loader.exec_module(module)
        finally:
            sys.modules.pop("us_asset_manager_massive", None)
    return module


class MassiveBaseTests(unittest.TestCase):
    def test_python_sources_do_not_hardcode_legacy_hosts(self):
        tracked = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.py"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.splitlines()
        forbidden = ("api." + "polygon.io", "socket." + "polygon.io")
        for filename in tracked:
            if Path(filename).resolve() == Path(__file__).resolve():
                continue
            source = (ROOT / filename).read_text(encoding="utf-8")
            for host in forbidden:
                self.assertNotIn(host, source, f"hardcoded legacy host in {filename}")

    def test_defaults(self):
        module = _load_manager()
        self.assertEqual(module.MASSIVE_API_BASE, "https://api.massive.com")
        self.assertEqual(module.MASSIVE_WS_BASE, "wss://socket.massive.com")

    def test_environment_overrides_and_precedence(self):
        self.assertEqual(_load_manager({"MASSIVE_API_BASE": "https://example.test/"}).MASSIVE_API_BASE,
                         "https://example.test")
        self.assertEqual(_load_manager({"POLYGON_API_BASE": "https://legacy.test/"}).MASSIVE_API_BASE,
                         "https://legacy.test")
        self.assertEqual(_load_manager({"MASSIVE_API_BASE": "https://new.test", "POLYGON_API_BASE": "https://legacy.test"}).MASSIVE_API_BASE,
                         "https://new.test")
        self.assertEqual(_load_manager({"MASSIVE_API_BASE": "", "POLYGON_API_BASE": "https://legacy.test"}).MASSIVE_API_BASE,
                         "https://legacy.test")

    def test_client_follows_next_url_as_returned(self):
        module = _load_manager()
        client = module.PolygonClient("key", module.MASSIVE_API_BASE, 0, 1, 1)
        old_host = "https://api." + "polygon.io"
        next_url = f"{old_host}/v3/snapshot/options/SPY?cursor=x"
        calls = []

        def request(url, params, endpoint):
            calls.append((url, params, endpoint))
            if len(calls) == 1:
                return {"results": [{"ticker": "O:SPY"}], "next_url": next_url}
            return {"results": []}

        client._request_json = request
        results = client.options_chain_snapshot("SPY", module.date(2026, 1, 1), module.date(2026, 1, 31), 2)
        self.assertEqual(results, [{"ticker": "O:SPY"}])
        self.assertEqual(calls[0][0], "https://api.massive.com/v3/snapshot/options/SPY")
        self.assertEqual(calls[1][0], next_url)
        self.assertEqual(calls[1][1], {"apiKey": "key"})


if __name__ == "__main__":
    unittest.main()
