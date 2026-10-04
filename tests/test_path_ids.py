"""
Path-injection tests for identifiers interpolated into request paths.

Each identifier must be rejected with ValueError before any request is sent;
otherwise an id like "../../v2/internal/admin" redirects the request, with the
caller's API key, to another path on the API host. Offline: every request
goes to an httpx.MockTransport, so no API key or network access is needed.

Run:
    pytest -v tests/test_path_ids.py
"""
import asyncio

import httpx
import pytest

from districtapi import AsyncDistrictAPI, DistrictAPI, NotFoundError

BAD_IDS = [
    "../../v2/internal/admin",
    "..",
    ".",
    "a/b",
    "0600017?admin=1",
    "0600017#frag",
    "%2e%2e",
    "0600017\n",
    "0600017 ",
    "",
    "a" * 65,
    "\u0661\u0662\u0663",  # non-ASCII digits
    None,
    True,
]

CALLS = [
    ("districts.fetch", lambda c, i: c.districts.fetch(i), "0600017", "/v1/districts/0600017"),
    ("districts.schools", lambda c, i: c.districts.schools(i), "0600017", "/v1/districts/0600017/schools"),
    ("schools.fetch", lambda c, i: c.schools.fetch(i), "060001709098", "/v1/schools/060001709098"),
    ("schools.district", lambda c, i: c.schools.district(i), "060001709098", "/v1/schools/060001709098/district"),
]


@pytest.fixture
def sent(monkeypatch):
    """Route every client the SDK builds through a transport that records requests."""
    requests = []

    def handler(request):
        requests.append(request)
        return httpx.Response(404, json={"detail": "not found"})

    transport = httpx.MockTransport(handler)
    for cls in (httpx.Client, httpx.AsyncClient):
        init = cls.__init__
        monkeypatch.setattr(
            cls, "__init__", lambda self, *a, _init=init, **kw: _init(self, *a, transport=transport, **kw)
        )
    return requests


def run(is_async, call, ident):
    if is_async:
        async def go():
            async with AsyncDistrictAPI(api_key="test") as c:
                return await call(c, ident)
        return asyncio.run(go())
    with DistrictAPI(api_key="test") as c:
        return call(c, ident)


@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("name,call,good,path", CALLS, ids=[c[0] for c in CALLS])
@pytest.mark.parametrize("bad", BAD_IDS, ids=repr)
def test_rejects_unsafe_id_before_request(sent, is_async, name, call, good, path, bad):
    with pytest.raises(ValueError, match="must contain only letters, digits"):
        run(is_async, call, bad)
    assert sent == []


@pytest.mark.parametrize("is_async", [False, True], ids=["sync", "async"])
@pytest.mark.parametrize("name,call,good,path", CALLS, ids=[c[0] for c in CALLS])
def test_accepts_real_id(sent, is_async, name, call, good, path):
    with pytest.raises(NotFoundError):
        run(is_async, call, good)
    assert [(r.url.host, r.url.raw_path.decode()) for r in sent] == [
        ("api.districtapi.dev", path)
    ]


def test_integer_id_still_accepted(sent):
    with pytest.raises(NotFoundError):
        run(False, lambda c, i: c.districts.fetch(i), 3600076)
    assert [r.url.raw_path.decode() for r in sent] == ["/v1/districts/3600076"]
