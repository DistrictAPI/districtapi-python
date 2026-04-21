# districtapi

Python SDK for [districtapi.dev](https://districtapi.dev) — US school district and school data from NCES federal datasets.

**The killer feature:** look up any US address and get back the school district serving it, with full enrollment, demographics, finances, school list, and GeoJSON boundary — all in one call.

## Install

```bash
pip install districtapi
```

## Quick start

Get a free API key at [districtapi.dev/dashboard](https://districtapi.dev/dashboard) — no credit card, 250 requests/month free forever.

```python
from districtapi import DistrictAPI

client = DistrictAPI(api_key="sk_live_...")

# Address → district (the killer feature)
district = client.districts.get(address="123 Main St, Apple Valley, CA")
print(district.name)                           # Apple Valley Unified School District
print(district.enrollment.total)               # 17432
print(district.finance.per_pupil_expenditure)  # 9823.45
print(district.geo.boundary)                   # GeoJSON MultiPolygon

# Lat/lng lookup
district = client.districts.get(lat=34.4988, lng=-117.1858)

# By NCES ID
district = client.districts.fetch("0600017")

# Search by name/state
results = client.districts.search(name="Apple Valley", state="CA")
for d in results:
    print(d.nces_id, d.name, d.enrollment_total)

# Schools in a district
schools = client.districts.schools("0600017")
for school in schools:
    print(school.name, school.grades.low, school.grades.high)

# Schools near an address
nearby = client.schools.near(address="123 Main St, Apple Valley, CA", radius_miles=3.0)

# A specific school
school = client.schools.fetch("060001700123")
print(school.name, school.flags.is_charter)

# School → district
district = client.schools.district("060001700123")
```

## Async support

```python
import asyncio
from districtapi import AsyncDistrictAPI

async def main():
    async with AsyncDistrictAPI(api_key="sk_live_...") as client:
        district = await client.districts.get(address="123 Main St, Apple Valley, CA")
        print(district.name)

asyncio.run(main())
```

## Context manager

```python
with DistrictAPI(api_key="sk_live_...") as client:
    district = client.districts.get(address="1600 Pennsylvania Ave, Washington, DC")
```

## Error handling

```python
from districtapi import DistrictAPI, NotFoundError, AuthenticationError, RateLimitError

client = DistrictAPI(api_key="sk_live_...")

try:
    district = client.districts.get(address="123 Nowhere St")
except NotFoundError:
    print("No district found for that address")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded — upgrade at districtapi.dev/pricing")
```

## Response types

All methods return typed dataclasses. Key types:

| Type | Fields |
|------|--------|
| `District` | `nces_id`, `name`, `state`, `county`, `enrollment`, `finance`, `students`, `geo`, `schools_count` |
| `DistrictSummary` | `nces_id`, `name`, `state`, `county`, `enrollment_total`, `lat`, `lng` |
| `School` | `nces_id`, `nces_district_id`, `name`, `state`, `grades`, `flags`, `enrollment`, `address`, `geo` |
| `DistrictEnrollment` | `total`, `year`, `demographics` |
| `DistrictFinance` | `per_pupil_expenditure`, `total_revenue`, `federal_revenue_pct`, `fiscal_year` |
| `GeoPoint` | `lat`, `lng`, `boundary` (GeoJSON) |

## Links

- **Docs:** [districtapi.dev/docs](https://districtapi.dev/docs)
- **Dashboard:** [districtapi.dev/dashboard](https://districtapi.dev/dashboard)
- **Pricing:** [districtapi.dev/pricing](https://districtapi.dev/pricing)
- **GitHub:** [github.com/districtapi/districtapi-python](https://github.com/districtapi/districtapi-python)
- **Issues:** [github.com/districtapi/districtapi-python/issues](https://github.com/districtapi/districtapi-python/issues)
