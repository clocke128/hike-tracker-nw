"""Deterministic, fictional data for exercising the pipeline without API calls."""

from __future__ import annotations

import random
from datetime import date, timedelta


def build_mock_data(as_of_date: date, seed: int = 42) -> dict[str, list[dict]]:
    """Return related mock datasets. Identical inputs produce identical records."""
    rng = random.Random(seed)
    parks = [
        {
            "park_code": "pine",
            "park_name": "Pine Ridge National Park (Fictional)",
            "state": "CO",
            "latitude": 39.12,
            "longitude": -105.73,
            "designation": "National Park",
        },
        {
            "park_code": "mesa",
            "park_name": "Red Mesa National Preserve (Fictional)",
            "state": "UT",
            "latitude": 37.41,
            "longitude": -110.22,
            "designation": "National Preserve",
        },
        {
            "park_code": "lake",
            "park_name": "Silver Lake National Recreation Area (Fictional)",
            "state": "MI",
            "latitude": 46.18,
            "longitude": -86.44,
            "designation": "National Recreation Area",
        },
        {
            "park_code": "cave",
            "park_name": "Wind Cave Hills National Monument (Fictional)",
            "state": "NM",
            "latitude": 34.77,
            "longitude": -106.11,
            "designation": "National Monument",
        },
    ]
    campgrounds = [
        {
            "campground_id": "pine-01",
            "park_code": "pine",
            "campground_name": "North Fork Campground",
            "reservation_required": True,
            "tent_sites": 24,
            "rv_sites": 8,
            "nightly_fee_usd": 28.0,
        },
        {
            "campground_id": "mesa-01",
            "park_code": "mesa",
            "campground_name": "Juniper Flats",
            "reservation_required": False,
            "tent_sites": 15,
            "rv_sites": 0,
            "nightly_fee_usd": 18.0,
        },
        {
            "campground_id": "lake-01",
            "park_code": "lake",
            "campground_name": "Lakeshore Camp",
            "reservation_required": True,
            "tent_sites": 30,
            "rv_sites": 20,
            "nightly_fee_usd": 35.0,
        },
    ]
    alerts = [
        {
            "alert_id": "pine-closure-01",
            "park_code": "pine",
            "category": "closure",
            "title": "Fictional ridge trail closure",
            "description": "Synthetic closure used only for pipeline testing.",
            "effective_date": as_of_date.isoformat(),
            "expires_date": (as_of_date + timedelta(days=7)).isoformat(),
        },
        {
            "alert_id": "lake-info-01",
            "park_code": "lake",
            "category": "information",
            "title": "Fictional dock maintenance",
            "description": "Synthetic advisory used only for pipeline testing.",
            "effective_date": as_of_date.isoformat(),
            "expires_date": None,
        },
    ]
    weather = []
    climate = {
        "pine": (58, 34),
        "mesa": (76, 49),
        "lake": (51, 31),
        "cave": (69, 42),
    }
    for park in parks:
        high_base, low_base = climate[park["park_code"]]
        for offset in range(3):
            high = high_base + rng.randint(-4, 4)
            low = min(high, low_base + rng.randint(-4, 4))
            weather.append(
                {
                    "park_code": park["park_code"],
                    "forecast_date": (as_of_date + timedelta(days=offset)).isoformat(),
                    "temperature_high_f": high,
                    "temperature_low_f": low,
                    "precipitation_probability_pct": rng.randrange(0, 101, 5),
                    "wind_speed_mph": rng.randrange(2, 26),
                }
            )
    return {
        "parks": parks,
        "campgrounds": campgrounds,
        "alerts": alerts,
        "weather": weather,
    }
