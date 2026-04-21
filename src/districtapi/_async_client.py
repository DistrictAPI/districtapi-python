from __future__ import annotations
from typing import Optional
import httpx
from ._http import _raise_for_error
from ._models import District, DistrictSummary, School
from ._client import BASE_URL


class AsyncDistrictResource:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def get(
        self,
        *,
        address: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        nces_id: Optional[str] = None,
    ) -> District:
        """Look up the school district for an address, coordinates, or NCES ID."""
        params: dict = {}
        if address:
            params["address"] = address
        if lat is not None:
            params["lat"] = lat
        if lng is not None:
            params["lng"] = lng
        if nces_id:
            params["nces_id"] = nces_id
        resp = await self._http.get("/v1/districts", params=params)
        _raise_for_error(resp)
        return District._from_dict(resp.json()["data"])

    async def fetch(self, nces_id: str) -> District:
        """Fetch a district by its 7-digit NCES LEA ID."""
        resp = await self._http.get(f"/v1/districts/{nces_id}")
        _raise_for_error(resp)
        return District._from_dict(resp.json()["data"])

    async def schools(self, nces_id: str) -> list[School]:
        """List all open schools in a district."""
        resp = await self._http.get(f"/v1/districts/{nces_id}/schools")
        _raise_for_error(resp)
        return [School._from_dict(s) for s in resp.json()["data"]]

    async def search(
        self,
        *,
        name: Optional[str] = None,
        state: Optional[str] = None,
        county: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[DistrictSummary]:
        """Search districts by name, state, and/or county."""
        params: dict = {"limit": limit, "offset": offset}
        if name:
            params["name"] = name
        if state:
            params["state"] = state
        if county:
            params["county"] = county
        resp = await self._http.get("/v1/districts/search", params=params)
        _raise_for_error(resp)
        return [DistrictSummary._from_dict(d) for d in resp.json()["data"]]


class AsyncSchoolResource:
    def __init__(self, http: httpx.AsyncClient):
        self._http = http

    async def fetch(self, nces_id: str) -> School:
        """Fetch a school by its 12-digit NCES school ID."""
        resp = await self._http.get(f"/v1/schools/{nces_id}")
        _raise_for_error(resp)
        return School._from_dict(resp.json()["data"])

    async def near(
        self,
        *,
        address: Optional[str] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        radius_miles: float = 5.0,
        limit: int = 20,
    ) -> list[School]:
        """Find schools near an address or coordinates."""
        params: dict = {"radius_miles": radius_miles, "limit": limit}
        if address:
            params["address"] = address
        if lat is not None:
            params["lat"] = lat
        if lng is not None:
            params["lng"] = lng
        resp = await self._http.get("/v1/schools", params=params)
        _raise_for_error(resp)
        return [School._from_dict(s) for s in resp.json()["data"]]

    async def district(self, nces_school_id: str) -> District:
        """Get the district that a school belongs to."""
        resp = await self._http.get(f"/v1/schools/{nces_school_id}/district")
        _raise_for_error(resp)
        return District._from_dict(resp.json()["data"])


class AsyncDistrictAPI:
    """Async client for the districtapi.dev API.

    Args:
        api_key: Your API key from districtapi.dev/dashboard
        base_url: Override the API base URL
        timeout: Request timeout in seconds (default: 30)

    Example:
        async with AsyncDistrictAPI(api_key="sk_live_...") as client:
            district = await client.districts.get(address="123 Main St, Apple Valley, CA")
            print(district.name)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
    ):
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={"X-API-Key": api_key},
            timeout=timeout,
        )
        self.districts = AsyncDistrictResource(self._http)
        self.schools = AsyncSchoolResource(self._http)

    async def aclose(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncDistrictAPI:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.aclose()
