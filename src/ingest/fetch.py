"""Outbound HTTPS with a host allowlist, a size cap and gzip, ported from regdelta's `src/shared/fetch.py`.

The port keeps the two properties regdelta enforces on every hop: the
scheme is https and the host is on the allowlist (checked on each
redirect too), and the body stops at the cap. It adds what the eCFR
versioner needs and regdelta's Lambda got for free from its runtime: the
`/full/` endpoint answers 406 unless the request accepts compression, so
every request says `Accept-Encoding: gzip` and the body is inflated here.

Two hosts are allowed: ecfr.gov's API and DailyMed's. Nothing else is
read by the build, and nothing this module reads decides where it reads
next except an on-host redirect.
"""

from __future__ import annotations

import gzip
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from typing import Any

ALLOWED_HOSTS = frozenset({"www.ecfr.gov", "dailymed.nlm.nih.gov"})
ALLOWED_SCHEMES = frozenset({"https"})
MAX_BYTES = 8 * 1024 * 1024
USER_AGENT = "pharmadelta-m02-gate/0.1 (+https://github.com/andaro74/pharmadelta)"
ATTEMPTS = 3
BACKOFF_SECONDS = 2.0


class FetchNotAllowedError(ValueError):
    """A URL failed the allowlist, on the initial request or on a redirect."""


class ResponseTooLargeError(ValueError):
    """The response body exceeded MAX_BYTES."""


class SourceUnread(Exception):
    """The source did not answer 200 after the allowed attempts. Carries the last status."""

    def __init__(self, url: str, status: int | None, detail: str):
        super().__init__(f"{url}: {detail}")
        self.url, self.status, self.detail = url, status, detail


def check_url(url: str) -> str:
    """Raise unless `url` is https and its parsed hostname is on the allowlist (never a substring test)."""
    if not isinstance(url, str) or not url:
        raise FetchNotAllowedError(f"not a URL: {url!r}")
    parts = urllib.parse.urlsplit(url)
    if parts.scheme.lower() not in ALLOWED_SCHEMES:
        raise FetchNotAllowedError(f"scheme {parts.scheme!r} not allowed: {url!r}")
    host = (parts.hostname or "").lower()
    if host not in ALLOWED_HOSTS:
        raise FetchNotAllowedError(f"host {host!r} not on the fetch allowlist {sorted(ALLOWED_HOSTS)}: {url!r}")
    return url


class _AllowlistRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _build_opener() -> urllib.request.OpenerDirector:
    """An opener carrying only https: no file, ftp, http or proxy handler exists in it."""
    opener = urllib.request.OpenerDirector()
    for handler in (
        urllib.request.HTTPSHandler(),
        _AllowlistRedirectHandler(),
        urllib.request.HTTPErrorProcessor(),
        urllib.request.HTTPDefaultErrorHandler(),
        urllib.request.UnknownHandler(),
    ):
        opener.add_handler(handler)
    return opener


_opener = _build_opener()
_cache: dict[str, bytes] = {}


def _inflate(body: bytes, encoding: str | None) -> bytes:
    enc = (encoding or "").lower().strip()
    if enc == "gzip" or enc == "x-gzip":
        return gzip.decompress(body)
    if enc == "deflate":
        return zlib.decompress(body)
    return body


def get_bytes(url: str, *, timeout: int = 60) -> bytes:
    """Fetch `url` once per process after the allowlist check; 200 or `SourceUnread`.

    A 5xx, a 429 or a network error is retried ATTEMPTS times with a short
    backoff; any other status is final. The body is read one byte past the
    cap and refused if it arrives, before inflation, and again after.
    """
    check_url(url)
    if url in _cache:
        return _cache[url]
    last: tuple[int | None, str] = (None, "not attempted")
    for attempt in range(1, ATTEMPTS + 1):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
        try:
            with _opener.open(req, timeout=timeout) as r:
                raw = r.read(MAX_BYTES + 1)
                encoding = r.headers.get("Content-Encoding")
        except urllib.error.HTTPError as exc:
            last = (exc.code, f"HTTP {exc.code}")
            if exc.code >= 500 or exc.code == 429:
                time.sleep(BACKOFF_SECONDS * attempt)
                continue
            raise SourceUnread(url, exc.code, f"HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = (None, f"{type(exc).__name__}: {exc}")
            time.sleep(BACKOFF_SECONDS * attempt)
            continue
        if len(raw) > MAX_BYTES:
            raise ResponseTooLargeError(f"response exceeded {MAX_BYTES} bytes: {url!r}")
        body = _inflate(raw, encoding)
        if len(body) > MAX_BYTES:
            raise ResponseTooLargeError(f"inflated response exceeded {MAX_BYTES} bytes: {url!r}")
        _cache[url] = body
        return body
    raise SourceUnread(url, last[0], f"{last[1]} after {ATTEMPTS} attempts")


def get_json(url: str, *, timeout: int = 60) -> Any:
    return json.loads(get_bytes(url, timeout=timeout).decode("utf-8"))
