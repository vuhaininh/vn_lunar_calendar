"""Core utility functions for Vietnamese Lunar Calendar.

Contains astronomical algorithms for Julian Day, New Moon, and Sun Longitude calculations.
Based on "Astronomical Algorithms" by Jean Meeus (1998) and adapted from Ho Ngoc Duc.
"""

import math
from functools import lru_cache
from typing import Tuple

from vn_lunar_calendar.constants import DEFAULT_TIMEZONE


def INT(d: float) -> int:
    """Return the integer part of a number (truncate toward zero)."""
    return int(d)


def jd_from_date(dd: int, mm: int, yy: int) -> int:
    """Compute the Julian Day Number for a given Gregorian date.

    Args:
        dd: Day (1-31)
        mm: Month (1-12)
        yy: Year (e.g. 2024)

    Returns:
        The Julian Day Number (int).
    """
    a = (14 - mm) // 12
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + ((153 * m + 2) // 5) + 365 * y + (y // 4) - (y // 100) + (y // 400) - 32045

    if jd < 2299161:
        jd = dd + ((153 * m + 2) // 5) + 365 * y + (y // 4) - 32083

    return jd


def jd_to_date(jd: int) -> Tuple[int, int, int]:
    """Convert a Julian Day Number to a Gregorian date.

    Args:
        jd: Julian Day Number.

    Returns:
        Tuple of (day, month, year).
    """
    if jd > 2299160:
        a = jd + 32044
        b = (4 * a + 3) // 146097
        c = a - (b * 146097) // 4
    else:
        b = 0
        c = jd + 32082

    d = (4 * c + 3) // 1461
    e = c - (1461 * d) // 4
    m = (5 * e + 2) // 153
    day = e - (153 * m + 2) // 5 + 1
    month = m + 3 - 12 * (m // 10)
    year = b * 100 + d - 4800 + (m // 10)

    return day, month, year


@lru_cache(maxsize=1024)
def new_moon(k: int) -> float:
    """Compute the time of the k-th New Moon.

    k is the sequential number of the new moon since 1900-01-01.

    Args:
        k: Integer index of the new moon.

    Returns:
        The Julian Day Number of the New Moon (float).
    """
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180

    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)

    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3

    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 -= 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 -= 0.0004 * math.sin(dr * 3 * Mpr)
    C1 += 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 -= 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 -= 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 += 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))

    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2

    return jd1 + C1 - deltat


def get_new_moon_day(k: int, timezone: float = DEFAULT_TIMEZONE) -> int:
    """Calculate the day (integer JDN) of the k-th New Moon for a given timezone.

    Args:
        k: Index of the new moon.
        timezone: The timezone offset (e.g., 7.0 for Vietnam).

    Returns:
        The integer Julian Day Number of the day containing the New Moon.
    """
    return INT(new_moon(k) + 0.5 + timezone / 24.0)


def sun_longitude(jd: float) -> float:
    """Compute the longitude of the sun at any given time.

    Args:
        jd: Julian Day Number (float).

    Returns:
        Sun longitude in radians [0, 2pi).
    """
    T = (jd - 2451545.0) / 36525.0
    T2 = T * T
    dr = math.pi / 180.0

    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2

    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M)
    DL += 0.000290 * math.sin(dr * 3 * M)

    L = L0 + DL
    L = L * dr
    L = L - 2 * math.pi * int(L / (2 * math.pi))

    # Ensure positive result
    if L < 0:
        L += 2 * math.pi

    return L


def get_sun_longitude(day_number: int, timezone: float = DEFAULT_TIMEZONE) -> int:
    """Compute the Sun Longitude segment (Solar Term index 0-11 for month calc).

    Calculated at midnight of the given day.

    Args:
        day_number: Integer Julian Day Number.
        timezone: Timezone offset.

    Returns:
        Integer from 0 to 11.
    """
    return int(sun_longitude(day_number - 0.5 - timezone / 24.0) / math.pi * 6)
