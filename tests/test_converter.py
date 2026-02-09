"""Tests for core conversion logic."""


import pytest
from vn_lunar_calendar.converter import lunar_to_solar, solar_to_lunar
from vn_lunar_calendar.exceptions import DateNotExistError


def test_solar_to_lunar_tet_dates():
    """Verify standard Tet (Lunar 1/1) dates."""
    # Source: https://www.informatik.uni-leipzig.de/~duc/amlich/
    test_cases = [
        # Solar (d, m, y) -> Lunar (d, m, y, leap)
        ((10, 2, 2024), (1, 1, 2024, False)),  # Giáp Thìn
        ((22, 1, 2023), (1, 1, 2023, False)),  # Quý Mão
        ((1, 2, 2022), (1, 1, 2022, False)),   # Nhâm Dần
        ((12, 2, 2021), (1, 1, 2021, False)),  # Tân Sửu
        ((25, 1, 2020), (1, 1, 2020, False)),  # Canh Tý
    ]

    for (sd, sm, sy), expected in test_cases:
        assert solar_to_lunar(sd, sm, sy) == expected


def test_lunar_to_solar_tet_dates():
    """Verify roundtrip Lunar -> Solar for Tet."""
    test_cases = [
        # Lunar (d, m, y, leap) -> Solar (d, m, y)
        ((1, 1, 2024, False), (10, 2, 2024)),
        ((1, 1, 2023, False), (22, 1, 2023)),
        ((1, 1, 2020, False), (25, 1, 2020)),
    ]

    for (ld, lm, ly, leap), expected in test_cases:
        assert lunar_to_solar(ld, lm, ly, leap) == expected


def test_leap_month_2020():
    """Verify leap month (4+) in 2020."""
    # 2020 has leap month 4
    # Month 4: starts 2020-04-23
    # Month 4+: starts 2020-05-23
    # Month 5: starts 2020-06-21

    # End of Month 4
    assert solar_to_lunar(22, 5, 2020) == (30, 4, 2020, False)
    # Start of Month 4+
    assert solar_to_lunar(23, 5, 2020) == (1, 4, 2020, True)
    # End of Month 4+
    assert solar_to_lunar(20, 6, 2020) == (29, 4, 2020, True)
    # Start of Month 5
    assert solar_to_lunar(21, 6, 2020) == (1, 5, 2020, False)


def test_leap_month_invalid_input():
    """Test invalid leap month request."""
    # 2024 has no leap month
    with pytest.raises(DateNotExistError):
        lunar_to_solar(1, 4, 2024, leap=True)


def test_19th_century_dates():
    """Test dates in 19th century (supported by algorithm)."""
    # 1890-01-31 -> Lunar 1890-01-11
    # Check random online converter for verification or use internal consistency
    # Solar: 1890-01-31 (Tet was 1890-01-21)
    # 1890 Tet -> Jan 21
    assert solar_to_lunar(21, 1, 1890) == (1, 1, 1890, False)


def test_21st_century_dates():
    """Test dates in 21st century."""
    # 2099-02-22 -> Lunar 2099-01-01 (Tet 2099? Need verify)
    # Just checking consistency
    lunar = solar_to_lunar(1, 1, 2099)
    solar = lunar_to_solar(*lunar)
    assert solar == (1, 1, 2099)
