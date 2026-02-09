"""Tests for core utility functions."""


from vn_lunar_calendar.utils import (
    get_new_moon_day,
    get_sun_longitude,
    jd_from_date,
    jd_to_date,
)


def test_jdn_conversion():
    """Test round-trip conversion between date and JDN."""
    test_dates = [
        (1, 1, 2024),
        (29, 2, 2024),  # Leap day
        (1, 1, 1900),
        (31, 12, 2099),
        (15, 8, 1945),
    ]

    for d, m, y in test_dates:
        jd = jd_from_date(d, m, y)
        d2, m2, y2 = jd_to_date(jd)
        assert (d, m, y) == (d2, m2, y2)


def test_known_jdn_values():
    """Test JDN calculation against known values."""
    # Source: https://aa.usno.navy.mil/data/JulianDate
    # 2000-01-01 12:00:00 UT is JD 2451545.0
    # Our function takes integer date (midnight), so 2000-01-01 should be 2451545
    # Wait, 2451545.0 is noon. Midnight starts at .5 of previous day?
    # Actually standard generic calendar conversion:
    # 2000-01-01 -> 2451545
    assert jd_from_date(1, 1, 2000) == 2451545
    assert jd_from_date(1, 1, 1970) == 2440588
    assert jd_from_date(2, 9, 1945) == 2431701


def test_new_moon_consistency():
    """Test that new moon days are increasing."""
    k_start = 0  # Around 1900
    prev_jd = get_new_moon_day(k_start)

    for k in range(1, 100):
        curr_jd = get_new_moon_day(k_start + k)
        assert curr_jd > prev_jd
        # Synodic month is approx 29.53 days
        diff = curr_jd - prev_jd
        assert 29 <= diff <= 30
        prev_jd = curr_jd


def test_sun_longitude_range():
    """Test that sun longitude segment is within 0-11."""
    start_jd = jd_from_date(1, 1, 2024)
    for i in range(366):
        seg = get_sun_longitude(start_jd + i)
        assert 0 <= seg <= 11
