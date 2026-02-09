"""Tests for SolarDate class."""

from datetime import date

import pytest
from vn_lunar_calendar.exceptions import DateNotExistError
from vn_lunar_calendar.solar import SolarDate


class TestSolarDateInit:
    """Tests for SolarDate initialization and validation."""

    def test_basic_init(self):
        d = SolarDate(1, 1, 2024)
        assert d.day == 1
        assert d.month == 1
        assert d.year == 2024

    def test_invalid_day(self):
        with pytest.raises(DateNotExistError):
            SolarDate(32, 1, 2024)

    def test_invalid_month(self):
        with pytest.raises(DateNotExistError):
            SolarDate(1, 13, 2024)

    def test_invalid_feb_non_leap(self):
        with pytest.raises(DateNotExistError):
            SolarDate(29, 2, 2023)  # Not leap

    def test_valid_feb_leap(self):
        d = SolarDate(29, 2, 2024)
        assert d.day == 29

    def test_invalid_day_zero(self):
        with pytest.raises(DateNotExistError):
            SolarDate(0, 1, 2024)

    def test_frozen(self):
        d = SolarDate(1, 1, 2024)
        with pytest.raises(AttributeError):
            d.day = 2  # type: ignore


class TestSolarDateLeapYear:
    """Tests for is_leap_year."""

    def test_leap_year_divisible_by_4(self):
        assert SolarDate.is_leap_year(2024) is True

    def test_non_leap_century(self):
        assert SolarDate.is_leap_year(1900) is False

    def test_leap_year_400(self):
        assert SolarDate.is_leap_year(2000) is True

    def test_non_leap(self):
        assert SolarDate.is_leap_year(2023) is False


class TestSolarDateConversions:
    """Tests for conversion methods."""

    def test_from_date(self):
        py_date = date(2024, 2, 10)
        d = SolarDate.from_date(py_date)
        assert d.day == 10
        assert d.month == 2
        assert d.year == 2024

    def test_to_date(self):
        d = SolarDate(10, 2, 2024)
        py_date = d.to_date()
        assert py_date == date(2024, 2, 10)

    def test_roundtrip_date(self):
        original = date(2024, 6, 15)
        d = SolarDate.from_date(original)
        assert d.to_date() == original

    def test_to_jd_and_from_jd(self):
        d = SolarDate(1, 1, 2024)
        jd = d.to_jd()
        d2 = SolarDate.from_jd(jd)
        assert d == d2

    def test_to_jdn_alias(self):
        d = SolarDate(1, 1, 2024)
        assert d.to_jdn() == d.to_jd()

    def test_from_jdn_alias(self):
        d = SolarDate(1, 1, 2024)
        jd = d.to_jd()
        assert SolarDate.from_jdn(jd) == SolarDate.from_jd(jd)

    def test_to_lunar_date(self):
        # Tet 2024 is Feb 10
        solar = SolarDate(10, 2, 2024)
        lunar = solar.to_lunar_date()
        assert lunar.day == 1
        assert lunar.month == 1
        assert lunar.year == 2024
        assert not lunar.is_leap

    def test_to_lunar_alias(self):
        solar = SolarDate(10, 2, 2024)
        assert solar.to_lunar() == solar.to_lunar_date()


class TestSolarDateComparison:
    """Tests for comparison operators."""

    def test_lt(self):
        assert SolarDate(1, 1, 2024) < SolarDate(2, 1, 2024)

    def test_lt_month(self):
        assert SolarDate(1, 1, 2024) < SolarDate(1, 2, 2024)

    def test_lt_year(self):
        assert SolarDate(1, 1, 2024) < SolarDate(1, 1, 2025)

    def test_eq(self):
        assert SolarDate(1, 1, 2024) == SolarDate(1, 1, 2024)

    def test_le(self):
        assert SolarDate(1, 1, 2024) <= SolarDate(1, 1, 2024)
        assert SolarDate(1, 1, 2024) <= SolarDate(2, 1, 2024)

    def test_gt(self):
        assert SolarDate(2, 1, 2024) > SolarDate(1, 1, 2024)

    def test_ge(self):
        assert SolarDate(1, 1, 2024) >= SolarDate(1, 1, 2024)


class TestSolarDateStrRepr:
    """Tests for string representations."""

    def test_str(self):
        assert str(SolarDate(1, 5, 2024)) == "01/05/2024"

    def test_repr(self):
        assert repr(SolarDate(1, 5, 2024)) == "SolarDate(1, 5, 2024)"


class TestSolarDateCanChi:
    """Tests for Can Chi methods on SolarDate."""

    def test_day_canchi_returns_string(self):
        d = SolarDate(10, 2, 2024)
        name = d.day_canchi()
        assert isinstance(name, str)
        parts = name.split()
        assert len(parts) == 2

    def test_hour_canchi_returns_string(self):
        d = SolarDate(10, 2, 2024)
        name = d.hour_canchi()
        assert isinstance(name, str)
        assert name.endswith("Tý")


class TestSolarDateSolarTerm:
    """Tests for solar_term method on SolarDate."""

    def test_solar_term_dong_chi(self):
        d = SolarDate(21, 12, 2024)
        term = d.solar_term()
        assert term == "Đông chí"

    def test_solar_term_returns_string(self):
        d = SolarDate(1, 6, 2024)
        term = d.solar_term()
        assert isinstance(term, str)
        assert len(term) > 0
