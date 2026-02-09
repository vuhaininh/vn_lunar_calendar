"""24 Solar Terms (Tiết Khí / 節氣) calculation.

Provides functions to determine the current solar term for a given day
and to list all 24 solar terms in a given year.

Based on the algorithm in docs/PRD/02_Algorithm_Design.md §2.7.
"""

from typing import Dict, List

from vn_lunar_calendar.constants import DEFAULT_TIMEZONE, TIET_KHI
from vn_lunar_calendar.utils import get_sun_longitude, jd_from_date, jd_to_date


def get_solar_term(jd: int, timezone: float = DEFAULT_TIMEZONE) -> str:
    """Get the solar term (Tiết Khí) name for a given Julian Day.

    Uses the algorithm: TIET_KHI[getSunLongitude(jd + 1, timezone)]
    where the +1 offset accounts for the astronomical convention.

    Each sun longitude segment (0-11) maps to a pair of consecutive
    solar terms (Trung Khí). The index into TIET_KHI is segment * 2.

    Args:
        jd: Julian Day Number.
        timezone: Timezone offset (default 7.0 for Vietnam).

    Returns:
        Vietnamese name of the solar term, e.g. "Đông chí".

    Examples:
        >>> from vn_lunar_calendar.utils import jd_from_date
        >>> get_solar_term(jd_from_date(21, 12, 2024))
        'Đông chí'
    """
    # Per algorithm doc: getTietKhi(jd) = TIET_KHI[getSunLongitude(jd + 1, tz)]
    # But TIET_KHI has 24 entries and segment is 0-11, so we use segment * 2
    segment = get_sun_longitude(jd + 1, timezone)
    return TIET_KHI[segment * 2]


def get_solar_term_index(jd: int, timezone: float = DEFAULT_TIMEZONE) -> int:
    """Get the solar term segment index (0-11) for a given Julian Day.

    Args:
        jd: Julian Day Number.
        timezone: Timezone offset (default 7.0 for Vietnam).

    Returns:
        Segment index 0-11.
    """
    return get_sun_longitude(jd + 1, timezone)


def get_all_solar_terms(year: int, timezone: float = DEFAULT_TIMEZONE) -> List[Dict]:
    """Get all 24 solar terms for a given solar year with their dates.

    Searches through each day of the year to detect when the sun longitude
    segment changes, which indicates a solar term boundary.

    Args:
        year: Solar year (e.g. 2024).
        timezone: Timezone offset (default 7.0 for Vietnam).

    Returns:
        List of dicts with keys: 'name' (str), 'date' (tuple of d,m,y),
        'jd' (int), 'index' (int 0-23).

    Examples:
        >>> terms = get_all_solar_terms(2024)
        >>> len(terms)
        24
    """
    terms: List[Dict] = []
    jd_start = jd_from_date(1, 1, year)
    jd_end = jd_from_date(31, 12, year)

    # Use jd+1 offset consistently with get_solar_term
    prev_segment = get_sun_longitude(jd_start + 1, timezone)

    for jd in range(jd_start + 1, jd_end + 1):
        curr_segment = get_sun_longitude(jd + 1, timezone)
        if curr_segment != prev_segment:
            # A segment boundary occurred — this is a solar term day
            term_index = curr_segment * 2
            d, m, y = jd_to_date(jd)
            terms.append({
                'name': TIET_KHI[term_index],
                'date': (d, m, y),
                'jd': jd,
                'index': term_index,
            })
            prev_segment = curr_segment

    return terms
