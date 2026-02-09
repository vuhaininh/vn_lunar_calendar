"""Tests for Solar Terms (Tiết Khí) module."""

from vn_lunar_calendar.solar_terms import (
    get_all_solar_terms,
    get_solar_term,
    get_solar_term_index,
)
from vn_lunar_calendar.utils import jd_from_date


class TestGetSolarTerm:
    """Tests for get_solar_term function."""

    def test_dong_chi_2024(self):
        """Winter Solstice 2024 is around Dec 21."""
        # Đông chí 2024 = Dec 21
        jd = jd_from_date(21, 12, 2024)
        term = get_solar_term(jd)
        assert term == "Đông chí"

    def test_xuan_phan_approx(self):
        """Spring Equinox is around March 20."""
        # Xuân phân ~ March 20
        jd = jd_from_date(20, 3, 2024)
        term = get_solar_term(jd)
        assert term == "Xuân phân"

    def test_ha_chi_approx(self):
        """Summer Solstice is around June 21."""
        jd = jd_from_date(21, 6, 2024)
        term = get_solar_term(jd)
        assert term == "Hạ chí"

    def test_segment_index_range(self):
        """Solar term index must be 0-11."""
        jd = jd_from_date(1, 1, 2024)
        for i in range(366):
            idx = get_solar_term_index(jd + i)
            assert 0 <= idx <= 11

    def test_returns_string(self):
        """get_solar_term should return a string."""
        jd = jd_from_date(1, 6, 2024)
        term = get_solar_term(jd)
        assert isinstance(term, str)
        assert len(term) > 0


class TestGetAllSolarTerms:
    """Tests for get_all_solar_terms function."""

    def test_returns_list(self):
        """Should return a list."""
        terms = get_all_solar_terms(2024)
        assert isinstance(terms, list)

    def test_has_entries(self):
        """Should have solar term entries (typically 11-12 per year since we
        track segment changes, not all 24 individual terms).
        """
        terms = get_all_solar_terms(2024)
        assert len(terms) >= 10

    def test_term_structure(self):
        """Each term should have required keys."""
        terms = get_all_solar_terms(2024)
        for t in terms:
            assert 'name' in t
            assert 'date' in t
            assert 'jd' in t
            assert 'index' in t

    def test_terms_are_ordered(self):
        """Terms should be in chronological order."""
        terms = get_all_solar_terms(2024)
        for i in range(1, len(terms)):
            assert terms[i]['jd'] > terms[i - 1]['jd']

    def test_dong_chi_in_december(self):
        """Đông chí should appear in December."""
        terms = get_all_solar_terms(2024)
        dong_chi = [t for t in terms if t['name'] == 'Đông chí']
        assert len(dong_chi) == 1
        d, m, y = dong_chi[0]['date']
        assert m == 12
        assert 20 <= d <= 23

    def test_multiple_years(self):
        """Should work for various years."""
        for year in [2000, 2010, 2024, 2050]:
            terms = get_all_solar_terms(year)
            assert len(terms) >= 10
