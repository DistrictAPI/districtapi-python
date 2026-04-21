from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class ResponseMeta:
    request_id: str
    credits_used: int
    credits_remaining: int

    @classmethod
    def _from_dict(cls, d: dict) -> ResponseMeta:
        return cls(
            request_id=d.get("requestId", ""),
            credits_used=d.get("creditsUsed", 0),
            credits_remaining=d.get("creditsRemaining", 0),
        )


@dataclass
class ResponseSource:
    nces_year: str
    updated_at: str
    freshness_days: int

    @classmethod
    def _from_dict(cls, d: dict) -> ResponseSource:
        return cls(
            nces_year=d.get("ncesYear", ""),
            updated_at=d.get("updatedAt", ""),
            freshness_days=d.get("freshnessDays", 0),
        )


@dataclass
class Address:
    state: str
    street: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    zip4: Optional[str] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[Address]:
        if not d:
            return None
        return cls(
            state=d.get("state", ""),
            street=d.get("street"),
            city=d.get("city"),
            zip=d.get("zip"),
            zip4=d.get("zip4"),
        )


@dataclass
class LocaleInfo:
    code: Optional[str] = None
    name: Optional[str] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[LocaleInfo]:
        if not d:
            return None
        return cls(code=d.get("code"), name=d.get("name"))


@dataclass
class TypeInfo:
    code: Optional[int] = None
    name: Optional[str] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[TypeInfo]:
        if not d:
            return None
        return cls(code=d.get("code"), name=d.get("name"))


@dataclass
class GradeSpan:
    low: Optional[str] = None
    high: Optional[str] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[GradeSpan]:
        if not d:
            return None
        return cls(low=d.get("low"), high=d.get("high"))


@dataclass
class GeoPoint:
    lat: float
    lng: float
    boundary: Optional[Any] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[GeoPoint]:
        if not d:
            return None
        return cls(lat=d.get("lat", 0.0), lng=d.get("lng", 0.0), boundary=d.get("boundary"))


@dataclass
class DemographicBreakdown:
    american_indian_pct: Optional[float] = None
    asian_pct: Optional[float] = None
    hispanic_pct: Optional[float] = None
    black_pct: Optional[float] = None
    white_pct: Optional[float] = None
    pacific_islander_pct: Optional[float] = None
    two_or_more_pct: Optional[float] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[DemographicBreakdown]:
        if not d:
            return None
        return cls(
            american_indian_pct=d.get("americanIndianPct"),
            asian_pct=d.get("asianPct"),
            hispanic_pct=d.get("hispanicPct"),
            black_pct=d.get("blackPct"),
            white_pct=d.get("whitePct"),
            pacific_islander_pct=d.get("pacificIslanderPct"),
            two_or_more_pct=d.get("twoOrMorePct"),
        )


@dataclass
class DistrictEnrollment:
    total: Optional[int] = None
    year: Optional[str] = None
    demographics: Optional[DemographicBreakdown] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[DistrictEnrollment]:
        if not d:
            return None
        return cls(
            total=d.get("total"),
            year=d.get("year"),
            demographics=DemographicBreakdown._from_dict(d.get("demographics") or {}),
        )


@dataclass
class DistrictStudents:
    free_reduced_lunch_pct: Optional[float] = None
    english_learner_pct: Optional[float] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[DistrictStudents]:
        if not d:
            return None
        return cls(
            free_reduced_lunch_pct=d.get("freeReducedLunchPct"),
            english_learner_pct=d.get("englishLearnerPct"),
        )


@dataclass
class DistrictFinance:
    per_pupil_expenditure: Optional[float] = None
    total_revenue: Optional[int] = None
    federal_revenue_pct: Optional[float] = None
    state_revenue_pct: Optional[float] = None
    local_revenue_pct: Optional[float] = None
    fiscal_year: Optional[str] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[DistrictFinance]:
        if not d:
            return None
        return cls(
            per_pupil_expenditure=d.get("perPupilExpenditure"),
            total_revenue=d.get("totalRevenue"),
            federal_revenue_pct=d.get("federalRevenuePct"),
            state_revenue_pct=d.get("stateRevenuePct"),
            local_revenue_pct=d.get("localRevenuePct"),
            fiscal_year=d.get("fiscalYear"),
        )


@dataclass
class SchoolSummary:
    nces_id: str
    name: str
    grades: Optional[GradeSpan] = None
    type: Optional[str] = None
    is_charter: bool = False
    enrollment: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    address: Optional[Address] = None

    @classmethod
    def _from_dict(cls, d: dict) -> SchoolSummary:
        return cls(
            nces_id=d.get("ncesId", ""),
            name=d.get("name", ""),
            grades=GradeSpan._from_dict(d.get("grades") or {}),
            type=d.get("type"),
            is_charter=d.get("isCharter", False),
            enrollment=d.get("enrollment"),
            lat=d.get("lat"),
            lng=d.get("lng"),
            address=Address._from_dict(d.get("address") or {}),
        )


@dataclass
class District:
    nces_id: str
    name: str
    state: str
    county: Optional[str] = None
    locale: Optional[LocaleInfo] = None
    type: Optional[TypeInfo] = None
    status: Optional[str] = None
    grades: Optional[GradeSpan] = None
    address: Optional[Address] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    geo: Optional[GeoPoint] = None
    enrollment: Optional[DistrictEnrollment] = None
    students: Optional[DistrictStudents] = None
    finance: Optional[DistrictFinance] = None
    schools_count: Optional[int] = None
    schools: Optional[list[SchoolSummary]] = None

    @classmethod
    def _from_dict(cls, d: dict) -> District:
        return cls(
            nces_id=d.get("ncesId", ""),
            name=d.get("name", ""),
            state=d.get("state", ""),
            county=d.get("county"),
            locale=LocaleInfo._from_dict(d.get("locale") or {}),
            type=TypeInfo._from_dict(d.get("type") or {}),
            status=d.get("status"),
            grades=GradeSpan._from_dict(d.get("grades") or {}),
            address=Address._from_dict(d.get("address") or {}),
            phone=d.get("phone"),
            website=d.get("website"),
            geo=GeoPoint._from_dict(d.get("geo") or {}),
            enrollment=DistrictEnrollment._from_dict(d.get("enrollment") or {}),
            students=DistrictStudents._from_dict(d.get("students") or {}),
            finance=DistrictFinance._from_dict(d.get("finance") or {}),
            schools_count=d.get("schoolsCount"),
            schools=[SchoolSummary._from_dict(s) for s in d["schools"]] if d.get("schools") else None,
        )


@dataclass
class DistrictSummary:
    nces_id: str
    name: str
    state: str
    county: Optional[str] = None
    status: Optional[str] = None
    grades: Optional[GradeSpan] = None
    enrollment_total: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

    @classmethod
    def _from_dict(cls, d: dict) -> DistrictSummary:
        return cls(
            nces_id=d.get("ncesId", ""),
            name=d.get("name", ""),
            state=d.get("state", ""),
            county=d.get("county"),
            status=d.get("status"),
            grades=GradeSpan._from_dict(d.get("grades") or {}),
            enrollment_total=d.get("enrollmentTotal"),
            lat=d.get("lat"),
            lng=d.get("lng"),
        )


@dataclass
class SchoolFlags:
    is_charter: bool = False
    is_magnet: bool = False
    is_virtual: bool = False
    is_title1: Optional[bool] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[SchoolFlags]:
        if not d:
            return None
        return cls(
            is_charter=d.get("isCharter", False),
            is_magnet=d.get("isMagnet", False),
            is_virtual=d.get("isVirtual", False),
            is_title1=d.get("isTitle1"),
        )


@dataclass
class SchoolEnrollment:
    total: Optional[int] = None
    year: Optional[str] = None
    free_reduced_lunch_total: Optional[int] = None
    free_reduced_lunch_pct: Optional[float] = None

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[SchoolEnrollment]:
        if not d:
            return None
        return cls(
            total=d.get("total"),
            year=d.get("year"),
            free_reduced_lunch_total=d.get("freeReducedLunchTotal"),
            free_reduced_lunch_pct=d.get("freeReducedLunchPct"),
        )


@dataclass
class SchoolDistrictRef:
    nces_id: str
    name: str

    @classmethod
    def _from_dict(cls, d: dict) -> Optional[SchoolDistrictRef]:
        if not d:
            return None
        return cls(nces_id=d.get("ncesId", ""), name=d.get("name", ""))


@dataclass
class School:
    nces_id: str
    nces_district_id: str
    name: str
    state: str
    county: Optional[str] = None
    locale: Optional[LocaleInfo] = None
    type: Optional[TypeInfo] = None
    status: Optional[str] = None
    grades: Optional[GradeSpan] = None
    flags: Optional[SchoolFlags] = None
    address: Optional[Address] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    geo: Optional[Any] = None
    enrollment: Optional[SchoolEnrollment] = None
    district: Optional[SchoolDistrictRef] = None

    @classmethod
    def _from_dict(cls, d: dict) -> School:
        return cls(
            nces_id=d.get("ncesId", ""),
            nces_district_id=d.get("ncesDistrictId", ""),
            name=d.get("name", ""),
            state=d.get("state", ""),
            county=d.get("county"),
            locale=LocaleInfo._from_dict(d.get("locale") or {}),
            type=TypeInfo._from_dict(d.get("type") or {}),
            status=d.get("status"),
            grades=GradeSpan._from_dict(d.get("grades") or {}),
            flags=SchoolFlags._from_dict(d.get("flags") or {}),
            address=Address._from_dict(d.get("address") or {}),
            phone=d.get("phone"),
            website=d.get("website"),
            geo=d.get("geo"),
            enrollment=SchoolEnrollment._from_dict(d.get("enrollment") or {}),
            district=SchoolDistrictRef._from_dict(d.get("district") or {}),
        )
