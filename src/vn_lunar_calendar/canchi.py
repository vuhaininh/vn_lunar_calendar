"""Can Chi (Sexagenary Cycle / Thiên Can Địa Chi) calculations.

Provides functions to compute the Can Chi name for:
- Year (năm)
- Month (tháng)
- Day (ngày)
- Hour (giờ, specifically Giờ Tý - first hour of day)

Based on the algorithm in docs/PRD/02_Algorithm_Design.md §2.6.
"""

from vn_lunar_calendar.constants import CAN, CHI


def year_name(year: int) -> str:
    """Get the Can Chi name for a lunar year.

    Args:
        year: Lunar year (e.g. 2024).

    Returns:
        Can Chi string, e.g. "Giáp Thìn".

    Examples:
        >>> year_name(2024)
        'Giáp Thìn'
        >>> year_name(2023)
        'Quý Mão'
    """
    can = CAN[(year + 6) % 10]
    chi = CHI[(year + 8) % 12]
    return f"{can} {chi}"


def month_name(month: int, year: int) -> str:
    """Get the Can Chi name for a lunar month.

    Args:
        month: Lunar month (1-12).
        year: Lunar year.

    Returns:
        Can Chi string, e.g. "Bính Dần" for month 1.

    Examples:
        >>> month_name(1, 2024)
        'Bính Dần'
    """
    can = CAN[(year * 12 + month + 3) % 10]
    chi = CHI[(month + 1) % 12]
    return f"{can} {chi}"


def day_name(jd: int) -> str:
    """Get the Can Chi name for a day given its Julian Day Number.

    Args:
        jd: Julian Day Number.

    Returns:
        Can Chi string, e.g. "Canh Tuất".
    """
    can = CAN[(jd + 9) % 10]
    chi = CHI[(jd + 1) % 12]
    return f"{can} {chi}"


def hour_name(jd: int) -> str:
    """Get the Can Chi name of Giờ Tý (first double-hour) for the day.

    The Vietnamese traditional hour system divides the day into 12
    double-hours (Canh). This returns the Can Chi of Giờ Tý (23:00-01:00),
    the first double-hour of the day.

    Args:
        jd: Julian Day Number.

    Returns:
        Can Chi string, e.g. "Bính Tý".
    """
    can = CAN[((jd - 1) * 2) % 10]
    chi = CHI[0]  # Tý
    return f"{can} {chi}"
