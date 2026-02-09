"""Tests for LunarDate class."""

from datetime import date

import pytest
from vn_lunar_calendar.exceptions import DateNotExistError
from vn_lunar_calendar.lunar import LunarDate
from vn_lunar_calendar.solar import SolarDate


class TestLunarDateInit:
    """Tests for LunarDate initialization and validation."""

    def test_basic_init(self):
        d = LunarDate(1, 1, 2024, False)
        assert d.day == 1
        assert d.month == 1
        assert d.year == 2024
        assert not d.is_leap

    def test_default_not_leap(self):
        d = LunarDate(1, 1, 2024)
        assert d.is_leap is False

    def test_invalid_month_zero(self):
        with pytest.raises(DateNotExistError):
            LunarDate(1, 0, 2024)

    def test_invalid_month_13(self):
        with pytest.raises(DateNotExistError):
            LunarDate(1, 13, 2024)

    def test_invalid_day_zero(self):
        with pytest.raises(DateNotExistError):
            LunarDate(0, 1, 2024)

    def test_invalid_day_31(self):
        with pytest.raises(DateNotExistError):
            LunarDate(31, 1, 2024)

    def test_frozen(self):
        d = LunarDate(1, 1, 2024)
        with pytest.raises(AttributeError):
            d.day = 2  # type: ignore


class TestLunarDateConversions:
    """Tests for conversion methods."""

    def test_to_solar_date_tet_2024(self):
        lunar = LunarDate(1, 1, 2024)
        solar = lunar.to_solar_date()
        assert solar.day == 10
        assert solar.month == 2
        assert solar.year == 2024

    def test_to_date(self):
        lunar = LunarDate(1, 1, 2024)
        py_date = lunar.to_date()
        assert py_date == date(2024, 2, 10)

    def test_from_date(self):
        py_date = date(2024, 2, 10)
        lunar = LunarDate.from_date(py_date)
        assert lunar.day == 1
        assert lunar.month == 1
        assert lunar.year == 2024

    def test_from_solar_date(self):
        solar = SolarDate(10, 2, 2024)
        lunar = LunarDate.from_solar_date(solar)
        assert lunar.day == 1
        assert lunar.month == 1
        assert lunar.year == 2024

    def test_invalid_leap_month_raises(self):
        lunar = LunarDate(1, 4, 2021, True)
        with pytest.raises(DateNotExistError):
            lunar.to_solar_date()


class TestLunarDateOrdering:
    """Tests for comparison operators."""

    def test_regular_before_leap(self):
        d1 = LunarDate(1, 4, 2020, False)
        d2 = LunarDate(1, 4, 2020, True)
        assert d1 < d2

    def test_leap_after_regular(self):
        d1 = LunarDate(1, 4, 2020, False)
        d2 = LunarDate(1, 4, 2020, True)
        assert d2 > d1

    def test_late_regular_before_early_leap(self):
        d3 = LunarDate(30, 4, 2020, False)
        d2 = LunarDate(1, 4, 2020, True)
        assert d3 < d2

    def test_same_date_equal(self):
        assert LunarDate(15, 1, 2024) == LunarDate(15, 1, 2024)

    def test_different_years(self):
        assert LunarDate(1, 1, 2023) < LunarDate(1, 1, 2024)

    def test_different_months(self):
        assert LunarDate(1, 1, 2024) < LunarDate(1, 2, 2024)


class TestLunarDateCanChi:
    """Tests for Can Chi methods on LunarDate."""

    def test_year_name_2024(self):
        d = LunarDate(1, 1, 2024)
        assert d.year_name() == "Giáp Thìn"

    def test_year_name_2023(self):
        d = LunarDate(1, 1, 2023)
        assert d.year_name() == "Quý Mão"

    def test_year_name_2020(self):
        d = LunarDate(1, 1, 2020)
        assert d.year_name() == "Canh Tý"

    def test_month_name_returns_string(self):
        d = LunarDate(1, 1, 2024)
        name = d.month_name()
        assert isinstance(name, str)
        assert name.endswith("Dần")  # Month 1 always Dần

    def test_day_name_returns_canchi(self):
        d = LunarDate(1, 1, 2024)
        name = d.day_name()
        parts = name.split()
        assert len(parts) == 2

    def test_hour_name_ends_ty(self):
        d = LunarDate(1, 1, 2024)
        name = d.hour_name()
        assert name.endswith("Tý")


class TestLunarDateSolarTerm:
    """Tests for solar_term method."""

    def test_solar_term_returns_string(self):
        d = LunarDate(1, 1, 2024)
        term = d.solar_term()
        assert isinstance(term, str)
        assert len(term) > 0


class TestLunarDateLuckyHours:
    """Tests for lucky_hours method."""

    def test_returns_12_hours(self):
        d = LunarDate(1, 1, 2024)
        hours = d.lucky_hours()
        assert len(hours) == 12

    def test_has_6_lucky(self):
        d = LunarDate(15, 8, 2024)
        hours = d.lucky_hours()
        lucky = sum(1 for h in hours if h['is_lucky'])
        assert lucky == 6


class TestLunarDateStrRepr:
    """Tests for string representations."""

    def test_str_regular(self):
        d = LunarDate(1, 1, 2024)
        assert str(d) == "01/01/2024"

    def test_str_leap(self):
        d = LunarDate(1, 4, 2020, True)
        assert "01/04/2020 (Nhuận)" in str(d)

    def test_repr(self):
        d = LunarDate(1, 4, 2020, True)
        assert repr(d) == "LunarDate(1, 4, 2020, is_leap=True)"
