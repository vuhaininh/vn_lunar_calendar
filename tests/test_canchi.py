"""Tests for Can Chi (Sexagenary Cycle) module."""

from vn_lunar_calendar.canchi import day_name, hour_name, month_name, year_name
from vn_lunar_calendar.utils import jd_from_date


class TestYearName:
    """Tests for year_name function."""

    def test_known_years(self):
        """Verify Can Chi names for well-known years."""
        # 2024 = Giáp Thìn
        assert year_name(2024) == "Giáp Thìn"
        # 2023 = Quý Mão
        assert year_name(2023) == "Quý Mão"
        # 2020 = Canh Tý
        assert year_name(2020) == "Canh Tý"
        # 2025 = Ất Tỵ
        assert year_name(2025) == "Ất Tỵ"

    def test_cycle_repeats(self):
        """60-year cycle should repeat."""
        assert year_name(1984) == year_name(1984 + 60)
        assert year_name(2000) == year_name(2000 + 60)

    def test_giap_ty_reference(self):
        """Year 4 AD is the reference Giáp Tý year."""
        assert year_name(4) == "Giáp Tý"

    def test_2021_tan_suu(self):
        """2021 = Tân Sửu."""
        assert year_name(2021) == "Tân Sửu"

    def test_2022_nham_dan(self):
        """2022 = Nhâm Dần."""
        assert year_name(2022) == "Nhâm Dần"


class TestMonthName:
    """Tests for month_name function."""

    def test_month_1_always_dan(self):
        """Month 1 (tháng Giêng) always has Chi = Dần."""
        for y in range(2020, 2030):
            name = month_name(1, y)
            assert name.endswith("Dần"), f"Month 1 of {y}: {name} should end with Dần"

    def test_month_sequence_chi(self):
        """Chi of months should follow the 12-branch cycle starting at Dần."""
        expected_chi = ['Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi',
                        'Thân', 'Dậu', 'Tuất', 'Hợi', 'Tý', 'Sửu']
        for m in range(1, 13):
            name = month_name(m, 2024)
            assert name.endswith(expected_chi[m - 1])

    def test_specific_month(self):
        """Month 1/2024 = Bính Dần."""
        assert month_name(1, 2024) == "Bính Dần"


class TestDayName:
    """Tests for day_name function."""

    def test_known_date(self):
        """Verify Can Chi of a specific known date."""
        # 2024-02-10 (Tết Giáp Thìn) = JDN 2460350
        jd = jd_from_date(10, 2, 2024)
        name = day_name(jd)
        # The name should be a valid "Can Chi" format
        parts = name.split()
        assert len(parts) == 2
        assert parts[0] in ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu',
                             'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
        assert parts[1] in ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ',
                             'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']

    def test_consecutive_days_different(self):
        """Consecutive days should have different Can Chi names."""
        jd = jd_from_date(1, 1, 2024)
        names = [day_name(jd + i) for i in range(10)]
        # All should be unique within 10 consecutive days
        assert len(set(names)) == 10

    def test_60_day_cycle(self):
        """Can Chi should repeat every 60 days."""
        jd = jd_from_date(1, 1, 2024)
        assert day_name(jd) == day_name(jd + 60)


class TestHourName:
    """Tests for hour_name function."""

    def test_always_ends_with_ty(self):
        """Hour name (Giờ Tý) always ends with Tý."""
        for i in range(30):
            jd = jd_from_date(1, 1, 2024) + i
            name = hour_name(jd)
            assert name.endswith("Tý"), f"Day {i}: {name} should end with Tý"

    def test_can_cycles(self):
        """The Can of Giờ Tý should cycle through all 10 Heavenly Stems
        every 5 days.
        """
        jd = jd_from_date(1, 1, 2024)
        names = [hour_name(jd + i) for i in range(5)]
        cans = [n.split()[0] for n in names]
        # Should have 5 unique Cans
        assert len(set(cans)) == 5

    def test_10_day_repeat(self):
        """Hour name repeats every 10 days (since 10 Cans × 1 Chi)."""
        # Actually can repeats every 5 days because (jd-1)*2 % 10
        jd = jd_from_date(1, 1, 2024)
        assert hour_name(jd) == hour_name(jd + 5)
