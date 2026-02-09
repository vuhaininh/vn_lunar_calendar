"""Core conversion engine: Solar <-> Lunar date conversion.

Hybrid approach:
1. Use lookup table (data.py) for 1900-2100 (100% accuracy).
2. Use astronomical calculations (Jean Meeus) for other years.
"""

from dataclasses import dataclass
from functools import lru_cache
from typing import List, Tuple

from vn_lunar_calendar import data
from vn_lunar_calendar.constants import DEFAULT_TIMEZONE
from vn_lunar_calendar.exceptions import DateNotExistError
from vn_lunar_calendar.utils import (
    get_new_moon_day,
    get_sun_longitude,
    jd_from_date,
    jd_to_date,
)

# --- Astronomical Implementation (Fallback) ---

@lru_cache(maxsize=256)
def get_lunar_month_11(year: int, timezone: float = DEFAULT_TIMEZONE) -> int:
    """Find the day starting lunar month 11 of the given solar year."""
    # Algorithm: Find month containing Winter Solstice (Sun Longitude 270 deg)
    off = jd_from_date(31, 12, year) - 2415021.0
    k = int(off / 29.530588853)
    nm = get_new_moon_day(k, timezone)
    sun_long = get_sun_longitude(nm, timezone)

    if sun_long >= 9:
        nm = get_new_moon_day(k - 1, timezone)

    return nm


@lru_cache(maxsize=256)
def get_leap_month_offset(a11: int, timezone: float = DEFAULT_TIMEZONE) -> int:
    """Find the offset of the leap month after the month starting on day a11."""
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = get_sun_longitude(get_new_moon_day(k, timezone), timezone)
    i = 1

    while i < 14:
        nm = get_new_moon_day(k + i, timezone)
        arc = get_sun_longitude(nm, timezone)
        if i > 1 and arc == last:
            return i - 1
        last = arc
        i += 1

    return 0


def _solar_to_lunar_astro(dd: int, mm: int, yy: int, timezone: float) -> Tuple[int, int, int, bool]:
    """Convert Solar to Lunar using astronomical algorithms."""
    day_number = jd_from_date(dd, mm, yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, timezone)

    if month_start > day_number:
        month_start = get_new_moon_day(k, timezone)

    a11 = get_lunar_month_11(yy, timezone)
    b11 = a11

    if a11 >= month_start:
        lunar_year = yy
        a11 = get_lunar_month_11(yy - 1, timezone)
    else:
        lunar_year = yy + 1
        b11 = get_lunar_month_11(yy + 1, timezone)

    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29)
    lunar_leap = False
    lunar_month = diff + 11

    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, timezone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = True

    if lunar_month > 12:
        lunar_month -= 12

    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1

    return lunar_day, lunar_month, lunar_year, lunar_leap


def _lunar_to_solar_astro(dd: int, mm: int, yy: int, leap: bool, timezone: float) -> Tuple[int, int, int]:
    """Convert Lunar to Solar using astronomical algorithms."""
    if mm < 11:
        a11 = get_lunar_month_11(yy - 1, timezone)
        b11 = get_lunar_month_11(yy, timezone)
    else:
        a11 = get_lunar_month_11(yy, timezone)
        b11 = get_lunar_month_11(yy + 1, timezone)

    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = mm - 11
    if off < 0:
        off += 12

    if b11 - a11 > 365:
        leap_off = get_leap_month_offset(a11, timezone)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12

        if leap and mm != leap_month:
            raise DateNotExistError(f"Month {mm} is not a leap month in year {yy}")

        if leap or off >= leap_off:
            off += 1
    else:
        if leap:
             raise DateNotExistError(f"Year {yy} is not a leap year")

    month_start = get_new_moon_day(k + off, timezone)
    return jd_to_date(month_start + dd - 1)


# --- Lookup Table Implementation ---

@dataclass
class LunarMonthInfo:
    month: int
    days: int
    is_leap: bool
    jd_start: int



def _get_lunar_year_data(year: int) -> Tuple[int, List[LunarMonthInfo]]:
    """Decode year code into list of month info.

    Returns:
        Tuple (jd_tet, list_of_months)
    """
    try:
        year_code = data.get_year_code(year)
    except ValueError:
        return 0, []

    offset_tet = year_code >> 17
    # Solar Date of Tet (Jan 1 + offset)
    jd_tet = jd_from_date(1, 1, year) + offset_tet

    leap_month_idx = year_code & 0xf  # 1-12, or 0
    leap_month_len = 30 if (year_code >> 16) & 1 else 29

    months = []
    current_jd = jd_tet

    # Bits 4-15 encode month lengths.
    # Bit 4 -> Month 12. Bit 15 -> Month 1.
    j = year_code >> 4
    reg_month_lens = [0] * 12
    for i in range(12):
        # i=0 (Month 12) -> lowest bit of j.
        reg_month_lens[11 - i] = 30 if (j & 1) else 29
        j >>= 1

    for m in range(1, 13):
        # Regular Month
        days = reg_month_lens[m - 1]
        months.append(LunarMonthInfo(m, days, False, current_jd))
        current_jd += days

        # Leap Month
        if m == leap_month_idx:
            # Leap month follows month 'm'
            months.append(LunarMonthInfo(m, leap_month_len, True, current_jd))
            current_jd += leap_month_len

    return jd_tet, months


def _solar_to_lunar_lookup(dd: int, mm: int, yy: int) -> Tuple[int, int, int, bool]:
    """Convert Solar to Lunar using lookup table."""
    day_jd = jd_from_date(dd, mm, yy)

    # Check if year in range
    if not (1800 <= yy <= 2099):
        # Try next/prev year logic if near boundary?
        # If yy=2100 Jan 1. It might belong to Lunar 2099.
        # But get_year_code(2099) works.
        # So we can proceed if we can find the lunar year.
        pass

    # Try current solar year
    try:
        jd_tet, months = _get_lunar_year_data(yy)
    except ValueError:
        return None  # Out of range

    if day_jd < jd_tet:
        # Belongs to previous lunar year
        try:
            jd_tet_prev, months_prev = _get_lunar_year_data(yy - 1)
        except ValueError:
             return None

        # Use months_prev
        months = months_prev
        lunar_year = yy - 1
    else:
        lunar_year = yy

    # Find month
    for m in reversed(months):
        if day_jd >= m.jd_start:
            day = day_jd - m.jd_start + 1
            return day, m.month, lunar_year, m.is_leap

    return None # Should not happen


def _lunar_to_solar_lookup(dd: int, mm: int, yy: int, leap: bool) -> Tuple[int, int, int]:
    """Convert Lunar to Solar using lookup table."""
    try:
        jd_tet, months = _get_lunar_year_data(yy)
    except ValueError:
        return None

    for m in months:
        if m.month == mm and m.is_leap == leap:
            if dd > m.days:
                raise DateNotExistError(f"Day {dd} does not exist in month {mm}/{yy} (max {m.days})")

            solar_jd = m.jd_start + dd - 1
            return jd_to_date(solar_jd)

    if leap:
        raise DateNotExistError(f"Month {mm} is not a leap month in year {yy}")

    raise DateNotExistError("Date lookup failed")


# --- Main Public API ---

def solar_to_lunar(dd: int, mm: int, yy: int, timezone: float = DEFAULT_TIMEZONE) -> Tuple[int, int, int, bool]:
    """Convert Solar date to Lunar date.

    Args:
        dd: Day.
        mm: Month.
        yy: Year.
        timezone: Timezone offset (used only for astronomical fallback).

    Returns:
        Tuple (day, month, year, is_leap).
    """
    # 1. Try lookup
    res = _solar_to_lunar_lookup(dd, mm, yy)
    if res is not None:
        return res

    # 2. Fallback
    return _solar_to_lunar_astro(dd, mm, yy, timezone)


def lunar_to_solar(
    day: int, month: int, year: int, leap: bool, timezone: float = DEFAULT_TIMEZONE
) -> Tuple[int, int, int]:
    """Convert Lunar date to Solar date.

    Args:
        day: Lunar day.
        month: Lunar month.
        year: Lunar year.
        leap: Whether it's a leap month.
        timezone: Timezone offset.

    Returns:
        Tuple (day, month, year).
    """
    # 1. Try lookup
    res = _lunar_to_solar_lookup(day, month, year, leap)
    if res is not None:
        return res

    # 2. Fallback
    return _lunar_to_solar_astro(day, month, year, leap, timezone)
