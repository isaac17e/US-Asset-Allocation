"""Pruebas del transporte FMP compartido y de su envoltura tolerante en Corp_FR_Optimization (sin red)."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import fmp_client  # noqa: E402


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


corp = _load("corp_fr_optimization", "Corp_FR_Optimization.py")


class FakeResponse:
    def __init__(self, status=200, payload=None, headers=None):
        self.status_code = status
        self.ok = status < 400
        self._payload = payload
        self.headers = headers or {}

    def json(self):
        if self._payload is None:
            raise ValueError("no json")
        return self._payload


def _client(responses):
    client = fmp_client.FMPClient("k", "https://x/stable/", 0.0, 5, 3)
    client.session = mock.Mock()
    client.session.get.side_effect = responses
    return client


class TransportTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.object(fmp_client.time, "sleep")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_retries_on_429_then_succeeds(self):
        client = _client([FakeResponse(429), FakeResponse(200, [{"a": 1}])])
        self.assertEqual(client._get("quote", {"symbol": "SPY"}), [{"a": 1}])
        self.assertEqual(client.n_calls, 2)

    def test_gives_up_after_max_retries(self):
        client = _client([FakeResponse(500)] * 3)
        with self.assertRaises(fmp_client.APIError):
            client._get("quote")

    def test_auth_status_raises_authorization_error(self):
        client = _client([FakeResponse(403)])
        with self.assertRaises(fmp_client.APIAuthorizationError):
            client._get("etf/holdings", {"symbol": "SPY"})

    def test_plan_message_in_body_is_authorization_error(self):
        client = _client([FakeResponse(200, {"Error Message": "Premium subscription required"})])
        with self.assertRaises(fmp_client.APIAuthorizationError):
            client._get("etf/holdings")

    def test_responses_are_cached(self):
        client = _client([FakeResponse(200, [{"a": 1}])])
        client._get("quote", {"symbol": "SPY"})
        client._get("quote", {"symbol": "SPY"})
        self.assertEqual(client.session.get.call_count, 1)

    def test_as_records_unwraps_common_containers(self):
        self.assertEqual(fmp_client.FMPClient._as_records({"historical": [{"x": 1}, 3]}), [{"x": 1}])
        self.assertEqual(fmp_client.FMPClient._as_records(None), [])


class SecretRedactionTests(unittest.TestCase):
    KEY = "SECRETKEY1234567890"

    def setUp(self):
        patcher = mock.patch.object(fmp_client.time, "sleep")
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_redact_secrets_covers_apikey_variants(self):
        for name in ("apikey", "apiKey", "api_key", "APIKEY"):
            text = f"GET https://h/stable/x?symbol=SPY&{name}={self.KEY}&limit=1 failed"
            out = fmp_client.redact_secrets(text)
            self.assertNotIn(self.KEY, out)
            self.assertIn("symbol=SPY", out)
            self.assertIn("limit=1", out)
            self.assertIn(f"{name}=***", out)

    def test_redact_secrets_masks_literal_secret_and_leaves_clean_text(self):
        self.assertEqual(fmp_client.redact_secrets(f"token {self.KEY} here", self.KEY), "token *** here")
        self.assertEqual(fmp_client.redact_secrets("sin credenciales ?symbol=SPY"), "sin credenciales ?symbol=SPY")

    def test_network_error_after_retries_does_not_leak_key(self):
        leaky = fmp_client.requests.ConnectionError(
            f"HTTPSConnectionPool(host='h', port=443): Max retries exceeded with url: /stable/quote?symbol=SPY&apikey={self.KEY}"
        )
        client = fmp_client.FMPClient(self.KEY, "https://h/stable", 0.0, 5, 2)
        client.session = mock.Mock()
        client.session.get.side_effect = [leaky, leaky]
        with self.assertRaises(fmp_client.APIError) as ctx:
            client._get("quote", {"symbol": "SPY"})
        self.assertNotIn(self.KEY, str(ctx.exception))
        self.assertIn("symbol=SPY", str(ctx.exception))

    def test_polygon_style_apikey_param_is_redacted(self):
        leaky = fmp_client.requests.ConnectionError(f"boom https://api.massive.com/v3/x?limit=250&apiKey={self.KEY}")
        client = fmp_client.BaseHTTPClient(self.KEY, "Polygon", 0.0, 5, 1)
        client.session = mock.Mock()
        client.session.get.side_effect = [leaky]
        with self.assertRaises(fmp_client.APIError) as ctx:
            client._request_json("https://api.massive.com/v3/x", {"apiKey": self.KEY}, "v3/x")
        self.assertNotIn(self.KEY, str(ctx.exception))

    def test_no_key_in_logged_messages(self):
        client = fmp_client.FMPClient(self.KEY, "https://h/stable", 0.0, 5, 2)
        client.session = mock.Mock()
        client.session.get.side_effect = [FakeResponse(500), FakeResponse(500)]
        with self.assertLogs("FMP", level="WARNING") as logs, self.assertRaises(fmp_client.APIError) as ctx:
            client._get("quote", {"symbol": "SPY"})
        self.assertNotIn(self.KEY, "\n".join(logs.output) + str(ctx.exception))


class CorpTolerantClientTests(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.object(fmp_client.time, "sleep")
        patcher.start()
        self.addCleanup(patcher.stop)

    def _corp_client(self, responses):
        client = corp.FMPClient("k")
        client.session = mock.Mock()
        client.session.get.side_effect = responses
        return client

    def test_returns_none_and_counts_failure_on_auth_error(self):
        client = self._corp_client([FakeResponse(401)])
        self.assertIsNone(client.get("income-statement", symbol="AAPL"))
        self.assertEqual(client.n_failures, 1)

    def test_returns_none_on_error_key(self):
        client = self._corp_client([FakeResponse(200, {"error": "boom"})])
        self.assertIsNone(client.get("profile", symbol="AAPL"))
        self.assertEqual(client.n_failures, 1)

    def test_get_records_always_returns_list(self):
        client = self._corp_client([FakeResponse(200, {"symbol": "AAPL"}), FakeResponse(404)])
        self.assertEqual(client.get_records("profile", symbol="AAPL"), [{"symbol": "AAPL"}])
        self.assertEqual(client.get_records("profile", symbol="ZZZ"), [])

    def test_boolean_params_are_lowercased_and_none_dropped(self):
        client = self._corp_client([FakeResponse(200, [])])
        client.get("company-screener", isActivelyTrading=True, sector=None)
        _, kwargs = client.session.get.call_args
        self.assertEqual(kwargs["params"]["isActivelyTrading"], "true")
        self.assertNotIn("sector", kwargs["params"])


if __name__ == "__main__":
    unittest.main()
