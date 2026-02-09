"""Tests for Lucky Hours (Giờ Hoàng Đạo) module."""

from vn_lunar_calendar.lucky_hours import get_lucky_hour_names, get_lucky_hours
from vn_lunar_calendar.utils import jd_from_date


class TestGetLuckyHours:
    """Tests for get_lucky_hours function."""

    def test_returns_12_hours(self):
        """Should return exactly 12 double-hours."""
        jd = jd_from_date(10, 2, 2024)
        hours = get_lucky_hours(jd)
        assert len(hours) == 12

    def test_6_lucky_hours(self):
        """Exactly 6 hours should be lucky."""
        jd = jd_from_date(1, 1, 2024)
        hours = get_lucky_hours(jd)
        lucky_count = sum(1 for h in hours if h['is_lucky'])
        assert lucky_count == 6

    def test_hour_structure(self):
        """Each hour should have required keys."""
        jd = jd_from_date(15, 6, 2024)
        hours = get_lucky_hours(jd)
        for h in hours:
            assert 'name' in h
            assert 'start' in h
            assert 'end' in h
            assert 'is_lucky' in h
            assert isinstance(h['is_lucky'], bool)

    def test_chi_names(self):
        """Hour names should match the 12 Earthly Branches."""
        expected = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ',
                    'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
        jd = jd_from_date(1, 1, 2024)
        hours = get_lucky_hours(jd)
        names = [h['name'] for h in hours]
        assert names == expected

    def test_first_hour_is_ty(self):
        """First double-hour should be Tý (23:00-01:00)."""
        jd = jd_from_date(1, 1, 2024)
        hours = get_lucky_hours(jd)
        assert hours[0]['name'] == 'Tý'
        assert hours[0]['start'] == 23
        assert hours[0]['end'] == 1

    def test_different_days_different_patterns(self):
        """Different days should potentially have different lucky patterns."""
        jd = jd_from_date(1, 1, 2024)
        patterns = set()
        for i in range(6):  # 6 days covers all patterns
            hours = get_lucky_hours(jd + i)
            pattern = tuple(h['is_lucky'] for h in hours)
            patterns.add(pattern)
        # Should have multiple distinct patterns
        assert len(patterns) >= 2

    def test_pattern_repeats_every_6_days(self):
        """Lucky hour pattern should repeat in groups of 6 (mod 6 of Chi)."""
        jd = jd_from_date(1, 1, 2024)
        # Days with same chi % 6 should have same pattern
        pattern_day0 = get_lucky_hours(jd)
        # chi_of_day = (jd + 1) % 12, so we need (jd2 + 1) % 12 % 6 == (jd + 1) % 12 % 6
        # This happens every 6 days since (jd+6+1) % 12 shifts by 6, but % 6 stays same
        pattern_day6 = get_lucky_hours(jd + 6)
        for h0, h6 in zip(pattern_day0, pattern_day6):
            assert h0['is_lucky'] == h6['is_lucky']

    def test_always_6_lucky(self):
        """Every day should have exactly 6 lucky hours."""
        jd = jd_from_date(1, 1, 2024)
        for i in range(30):
            hours = get_lucky_hours(jd + i)
            lucky = sum(1 for h in hours if h['is_lucky'])
            assert lucky == 6, f"Day {i}: expected 6 lucky hours, got {lucky}"


class TestGetLuckyHourNames:
    """Tests for get_lucky_hour_names function."""

    def test_returns_6_names(self):
        """Should return exactly 6 lucky hour names."""
        jd = jd_from_date(1, 1, 2024)
        names = get_lucky_hour_names(jd)
        assert len(names) == 6

    def test_names_are_chi(self):
        """All names should be valid Earthly Branch names."""
        valid_chi = {'Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ',
                     'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi'}
        jd = jd_from_date(15, 8, 2024)
        names = get_lucky_hour_names(jd)
        for name in names:
            assert name in valid_chi
