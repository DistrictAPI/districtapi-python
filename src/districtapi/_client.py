from __future__ import annotations
from typing import Optional
import httpx
from ._http import _raise_for_error
from ._models import District, DistrictSummary, School

BASE_URL = "https://api.districtapi.dev"


class DistrictResource:
    def __init__(self, http: httpx.Client):
        self._http = http

    def get(
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
        resp = self._http.get("/v1/districts", params=params)
        _raise_for_error(resp)
        return District._from_dict(resp.json()["data"])

    def fetch(self, nces_id: str) -> District:
        """Fetch a district by its 7-digit NCES LEA ID."""
        resp = self._http.get(f"/v1/districts/{nces_id}")
        _raise_for_error(resp)
        return District._from_dict(resp.json()["data"])

    def schools(self, nces_id: str) -> list[School]:
        """List all open schools in a district."""
        resp = self._http.get(f"/v1/districts/{nces_id}/schools")
        _raise_for_error(resp)
        return [School._from_dict(s) for s in resp.json()["data"]]

    def search(
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
        resp = self._http.get("/v1/districts/search", params=params)
        _raise_for_error(resp)
        return [DistrictSummary._from_dict(d) for d in resp.json()["data"]]


class SchoolResource:
    def __init__(self, http: httpx.Client):
        self._http = http

    def fetch(self, nces_id: str) -> School:
        """Fetch a school by its 12-digit NCES school ID."""
        resp = self._http.get(f"/v1/schools/{nces_id}")
        _raise_for_error(resp)
        return School._from_dict(resp.json()["data"])

    def near(
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
        resp = self._http.get("/v1/schools", params=params)
        _raise_for_error(resp)
        return [School._from_dict(s) for s in resp.json()["data"]]

    def district(self, nces_school_id: str) -> District:
        """Get the district that a school belongs to."""
        resp = self._http.get(f"/v1/schools/{nces_school_id}/district")
        _raise_for_error(resp)
        return District._from_dict(resp.json()["data"])


class DistrictAPI:
    """Sync client for the districtapi.dev API.

    Args:
        api_key: Your API key from districtapi.dev/dashboard
        base_url: Override the API base URL
        timeout: Request timeout in seconds (default: 30)

    Example:
        client = DistrictAPI(api_key="sk_live_...")
        district = client.districts.get(address="123 Main St, Apple Valley, CA")
        print(district.name)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
    ):
        self._http = httpx.Client(
            base_url=base_url,
            headers={"X-API-Key": api_key},
            timeout=timeout,
        )
        self.districts = DistrictResource(self._http)
        self.schools = SchoolResource(self._http)

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> DistrictAPI:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()
