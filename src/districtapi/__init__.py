"""
districtapi — Python SDK for the districtapi.dev API

US school district and school data from NCES federal datasets.

Usage:
    from districtapi import DistrictAPI

    client = DistrictAPI(api_key="sk_live_...")
    district = client.districts.get(address="123 Main St, Apple Valley, CA")
    print(district.name)           # Apple Valley Unified School District
    print(district.enrollment.total)  # 17432
    print(district.finance.per_pupil_expenditure)  # 9823.45

Docs:    https://districtapi.dev/docs
GitHub:  https://github.com/districtapi/districtapi-python
"""

from ._client import DistrictAPI
from ._async_client import AsyncDistrictAPI
from ._models import (
    District,
    DistrictSummary,
    School,
    SchoolSummary,
    Address,
    GradeSpan,
    GeoPoint,
    LocaleInfo,
    TypeInfo,
    DemographicBreakdown,
    DistrictEnrollment,
    DistrictStudents,
    DistrictFinance,
    SchoolFlags,
    SchoolEnrollment,
    SchoolDistrictRef,
    ResponseMeta,
    ResponseSource,
)
from ._exceptions import (
    DistrictAPIError,
    NotFoundError,
    AuthenticationError,
    RateLimitError,
    InvalidParamsError,
)

__version__ = "0.2.0"
__all__ = [
    "DistrictAPI",
    "AsyncDistrictAPI",
    "District",
    "DistrictSummary",
    "School",
    "SchoolSummary",
    "Address",
    "GradeSpan",
    "GeoPoint",
    "LocaleInfo",
    "TypeInfo",
    "DemographicBreakdown",
    "DistrictEnrollment",
    "DistrictStudents",
    "DistrictFinance",
    "SchoolFlags",
    "SchoolEnrollment",
    "SchoolDistrictRef",
    "ResponseMeta",
    "ResponseSource",
    "DistrictAPIError",
    "NotFoundError",
    "AuthenticationError",
    "RateLimitError",
    "InvalidParamsError",
]
