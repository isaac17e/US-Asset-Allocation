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
