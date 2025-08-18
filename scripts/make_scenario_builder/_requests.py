"""Very small subset of the :mod:`requests` API used for testing.

This module provides ``get``, ``post`` and ``put`` functions returning objects
with ``json`` and ``raise_for_status`` methods. It relies solely on the Python
standard library and is intentionally lightweight – network calls are rarely
executed in tests where the functions are typically mocked.
"""

from __future__ import annotations

import json
from urllib import request, error


class Response:
    def __init__(self, data: str, status: int):
        self._data = data
        self.status_code = status

    def json(self) -> dict:
        return json.loads(self._data) if self._data else {}

    def raise_for_status(self) -> None:
        if not (200 <= self.status_code < 300):
            raise error.HTTPError(None, self.status_code, "HTTP error", hdrs=None, fp=None)


def _send(method: str, url: str, headers: dict | None = None, payload: dict | None = None) -> Response:
    data = json.dumps(payload).encode() if payload is not None else None
    req = request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode()
            status = resp.getcode()
    except error.HTTPError as e:
        body = e.read().decode()
        status = e.code
    return Response(body, status)


def post(url: str, headers: dict | None = None, json: dict | None = None) -> Response:  # noqa: A002
    return _send("POST", url, headers, json)


def get(url: str, headers: dict | None = None) -> Response:
    return _send("GET", url, headers)


def put(url: str, headers: dict | None = None, json: dict | None = None) -> Response:  # noqa: A002
    return _send("PUT", url, headers, json)
