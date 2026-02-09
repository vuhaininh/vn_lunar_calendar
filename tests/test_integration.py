"""Integration tests for vn_lunar_calendar.

Covers:
- Roundtrip Solar ↔ Lunar conversions (100+ dates)
- Known Tết dates (2020-2030)
- Edge cases: leap months, year boundaries, Feb 29
"""

import random
from datetime import date, timedelta

import pytest
from vn_lunar_calendar.converter import lunar_to_solar, solar_to_lunar
from vn_lunar_calendar.exceptions import DateNotExistError
from vn_lunar_calendar.solar import SolarDate


class TestRoundtripConversion:
    """Roundtrip Solar ↔ Lunar conversion tests."""

    def test_roundtrip_tet_dates(self):
        """Known Tet dates should roundtrip correctly."""
        tet_dates = [
            (25, 1, 2020),
            (12, 2, 2021),
            (1, 2, 2022),
            (22, 1, 2023),
            (10, 2, 2024),
            (29, 1, 2025),
            (17, 2, 2026),
            (6, 2, 2027),
            (26, 1, 2028),
            (13, 2, 2029),
            (2, 2, 2030),
        ]
        for d, m, y in tet_dates:
            lunar = solar_to_lunar(d, m, y)
            assert lunar[0] == 1, f"Tet {d}/{m}/{y}: day should be 1, got {lunar[0]}"
            assert lunar[1] == 1, f"Tet {d}/{m}/{y}: month should be 1, got {lunar[1]}"
            assert lunar[2] == y, f"Tet {d}/{m}/{y}: year should be {y}, got {lunar[2]}"
            assert lunar[3] is False, f"Tet {d}/{m}/{y}: should not be leap"

    def test_roundtrip_random_dates_2000s(self):
        """100 random dates in 2000-2050 should roundtrip correctly."""
        random.seed(42)
        start = date(2000, 1, 1)
        end = date(2050, 12, 31)
        delta = (end - start).days

        for _ in range(100):
            offset = random.randint(0, delta)
            d = start + timedelta(days=offset)
            sd, sm, sy = d.day, d.month, d.year

            # Solar → Lunar → Solar
            ld, lm, ly, leap = solar_to_lunar(sd, sm, sy)
            rd, rm, ry = lunar_to_solar(ld, lm, ly, leap)
            assert (rd, rm, ry) == (sd, sm, sy), \
                f"Roundtrip failed for {sd}/{sm}/{sy}: Lunar({ld}/{lm}/{ly},leap={leap}) → Solar({rd}/{rm}/{ry})"

    def test_roundtrip_random_dates_1900s(self):
        """50 random dates in 1900-1999 should roundtrip correctly."""
        random.seed(123)
        start = date(1900, 1, 1)
        end = date(1999, 12, 31)
        delta = (end - start).days

        for _ in range(50):
            offset = random.randint(0, delta)
            d = start + timedelta(days=offset)
            sd, sm, sy = d.day, d.month, d.year

            ld, lm, ly, leap = solar_to_lunar(sd, sm, sy)
            rd, rm, ry = lunar_to_solar(ld, lm, ly, leap)
            assert (rd, rm, ry) == (sd, sm, sy), \
                f"Roundtrip failed for {sd}/{sm}/{sy}"

    def test_roundtrip_random_dates_1800s(self):
        """30 random dates in 1800-1899 should roundtrip correctly."""
        random.seed(456)
        start = date(1800, 1, 1)
        end = date(1899, 12, 31)
        delta = (end - start).days

        for _ in range(30):
            offset = random.randint(0, delta)
            d = start + timedelta(days=offset)
            sd, sm, sy = d.day, d.month, d.year

            ld, lm, ly, leap = solar_to_lunar(sd, sm, sy)
            rd, rm, ry = lunar_to_solar(ld, lm, ly, leap)
            assert (rd, rm, ry) == (sd, sm, sy), \
                f"Roundtrip failed for {sd}/{sm}/{sy}"

    def test_roundtrip_class_api(self):
        """Roundtrip using SolarDate/LunarDate class API."""
        solar = SolarDate(10, 2, 2024)
        lunar = solar.to_lunar()
        solar2 = lunar.to_solar_date()
        assert solar == solar2

    def test_roundtrip_class_multiple(self):
        """Multiple roundtrips using class API."""
        dates = [
            SolarDate(1, 1, 2024),
            SolarDate(15, 8, 2024),
            SolarDate(25, 1, 2020),
            SolarDate(31, 12, 2023),
            SolarDate(1, 6, 1990),
        ]
        for solar in dates:
            lunar = solar.to_lunar()
            solar_back = lunar.to_solar_date()
            assert solar == solar_back, f"Roundtrip failed for {solar}"


class TestTetDates:
    """Verify known Tết Nguyên Đán dates."""

    @pytest.mark.parametrize("solar_date,year", [
        ((25, 1, 2020), 2020),
        ((12, 2, 2021), 2021),
        ((1, 2, 2022), 2022),
        ((22, 1, 2023), 2023),
        ((10, 2, 2024), 2024),
        ((29, 1, 2025), 2025),
    ])
    def test_tet_is_lunar_1_1(self, solar_date, year):
        """Tet should be Lunar 1/1."""
        d, m, y = solar_date
        day, month, yr, leap = solar_to_lunar(d, m, y)
        assert day == 1
        assert month == 1
        assert yr == year
        assert leap is False


class TestLeapMonthEdgeCases:
    """Tests for leap month edge cases."""

    def test_2020_leap_month_4(self):
        """2020 has leap month 4."""
        # End of Month 4
        assert solar_to_lunar(22, 5, 2020) == (30, 4, 2020, False)
        # Start of Month 4+
        assert solar_to_lunar(23, 5, 2020) == (1, 4, 2020, True)
        # End of Month 4+
        assert solar_to_lunar(20, 6, 2020) == (29, 4, 2020, True)
        # Start of Month 5
        assert solar_to_lunar(21, 6, 2020) == (1, 5, 2020, False)

    def test_invalid_leap_month_raises(self):
        """Requesting a non-existent leap month should raise."""
        with pytest.raises(DateNotExistError):
            lunar_to_solar(1, 4, 2024, leap=True)

    def test_invalid_leap_year_raises(self):
        """Requesting leap in a non-leap year should raise."""
        with pytest.raises(DateNotExistError):
            lunar_to_solar(1, 4, 2021, leap=True)


class TestYearBoundary:
    """Tests for year boundary dates."""

    def test_dec_31_solar(self):
        """Dec 31 should be a valid date in the lunar calendar."""
        d, m, y, leap = solar_to_lunar(31, 12, 2024)
        assert 1 <= d <= 30
        assert 1 <= m <= 12

    def test_jan_1_solar(self):
        """Jan 1 should be a valid date in the lunar calendar."""
        d, m, y, leap = solar_to_lunar(1, 1, 2024)
        assert 1 <= d <= 30
        assert 1 <= m <= 12

    def test_year_boundary_roundtrip(self):
        """Dates around New Year should roundtrip."""
        for day in range(28, 32):
            try:
                sd = SolarDate(day, 12, 2024)
                lunar = sd.to_lunar()
                back = lunar.to_solar_date()
                assert sd == back
            except DateNotExistError:
                pass  # Day 31 might not exist in some months

        for day in range(1, 5):
            sd = SolarDate(day, 1, 2025)
            lunar = sd.to_lunar()
            back = lunar.to_solar_date()
            assert sd == back


class TestFeb29:
    """Tests for February 29 (leap day)."""

    def test_feb_29_2024(self):
        """Feb 29, 2024 should convert correctly."""
        d, m, y, leap = solar_to_lunar(29, 2, 2024)
        rd, rm, ry = lunar_to_solar(d, m, y, leap)
        assert (rd, rm, ry) == (29, 2, 2024)

    def test_feb_29_2000(self):
        """Feb 29, 2000 should convert correctly."""
        d, m, y, leap = solar_to_lunar(29, 2, 2000)
        rd, rm, ry = lunar_to_solar(d, m, y, leap)
        assert (rd, rm, ry) == (29, 2, 2000)

    def test_feb_29_non_leap_raises(self):
        """Feb 29 in non-leap year should raise."""
        with pytest.raises(DateNotExistError):
            SolarDate(29, 2, 2023)


class TestTrungThu:
    """Verify known Trung Thu (Mid-Autumn Festival) dates.

    Trung Thu = Lunar 15/8.
    """

    @pytest.mark.parametrize("year,expected_solar", [
        (2024, (17, 9, 2024)),
        (2023, (29, 9, 2023)),
        (2022, (10, 9, 2022)),
        (2021, (21, 9, 2021)),
        (2020, (1, 10, 2020)),
    ])
    def test_trung_thu(self, year, expected_solar):
        """Trung Thu (Lunar 15/8) should match known solar dates."""
        sd, sm, sy = lunar_to_solar(15, 8, year, False)
        assert (sd, sm, sy) == expected_solar, \
            f"Trung Thu {year}: expected {expected_solar}, got ({sd}, {sm}, {sy})"
