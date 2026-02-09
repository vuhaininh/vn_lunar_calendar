"""Can Chi (Sexagenary Cycle / Thiên Can Địa Chi) calculations.

Provides functions to compute the Can Chi name for:
- Year (năm)
- Month (tháng)
- Day (ngày)
- Hour (giờ) — both Giờ Tý and any specific clock hour

Based on the algorithm in docs/PRD/02_Algorithm_Design.md §2.6.
"""

from typing import Dict, List

from vn_lunar_calendar.constants import CAN, CHI, GIO_HOANG_DAO

# 12 double-hour periods (canh) with start/end times
HOUR_RANGES: List[Dict] = [
    {"chi": "Tý", "start": "23:00", "end": "01:00"},
    {"chi": "Sửu", "start": "01:00", "end": "03:00"},
    {"chi": "Dần", "start": "03:00", "end": "05:00"},
    {"chi": "Mão", "start": "05:00", "end": "07:00"},
    {"chi": "Thìn", "start": "07:00", "end": "09:00"},
    {"chi": "Tỵ", "start": "09:00", "end": "11:00"},
    {"chi": "Ngọ", "start": "11:00", "end": "13:00"},
    {"chi": "Mùi", "start": "13:00", "end": "15:00"},
    {"chi": "Thân", "start": "15:00", "end": "17:00"},
    {"chi": "Dậu", "start": "17:00", "end": "19:00"},
    {"chi": "Tuất", "start": "19:00", "end": "21:00"},
    {"chi": "Hợi", "start": "21:00", "end": "23:00"},
]


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


def hour_chi_index(hour: int) -> int:
    """Map a clock hour (0-23) to the Chi (Earthly Branch) index (0-11).

    The Vietnamese traditional day is divided into 12 double-hours:
        Tý (0): 23:00-01:00, Sửu (1): 01:00-03:00, Dần (2): 03:00-05:00,
        Mão (3): 05:00-07:00, Thìn (4): 07:00-09:00, Tỵ (5): 09:00-11:00,
        Ngọ (6): 11:00-13:00, Mùi (7): 13:00-15:00, Thân (8): 15:00-17:00,
        Dậu (9): 17:00-19:00, Tuất (10): 19:00-21:00, Hợi (11): 21:00-23:00.

    Args:
        hour: Clock hour (0-23).

    Returns:
        Chi index 0-11.

    Examples:
        >>> hour_chi_index(3)   # 3 AM = Giờ Dần
        2
        >>> hour_chi_index(23)  # 11 PM = Giờ Tý
        0
    """
    if not 0 <= hour <= 23:
        raise ValueError(f"Hour must be 0-23, got {hour}")
    return ((hour + 1) // 2) % 12


def get_hour_info(hour: int, dd: int, mm: int, yy: int) -> Dict:
    """Get full Can Chi information for a specific clock hour on a date.

    This handles the midnight crossing of Giờ Tý correctly:
    hours 23:00-23:59 belong to the Tý hour of the NEXT day's cycle.

    Args:
        hour: Clock hour (0-23).
        dd: Solar day.
        mm: Solar month.
        yy: Solar year.

    Returns:
        Dict with keys:
            - 'can': Heavenly Stem name (e.g. "Nhâm")
            - 'chi': Earthly Branch name (e.g. "Dần")
            - 'name': Full Can Chi name (e.g. "Nhâm Dần")
            - 'start': Start time string (e.g. "03:00")
            - 'end': End time string (e.g. "05:00")
            - 'is_lucky': Whether this is a lucky hour (Giờ Hoàng Đạo)

    Examples:
        >>> get_hour_info(3, 11, 7, 1989)
        {'can': 'Nhâm', 'chi': 'Dần', 'name': 'Nhâm Dần', ...}
    """
    from vn_lunar_calendar.utils import jd_from_date

    if not 0 <= hour <= 23:
        raise ValueError(f"Hour must be 0-23, got {hour}")

    jd = jd_from_date(dd, mm, yy)

    # Giờ Tý (23:00-01:00) spans midnight.
    # 23:00+ belongs to the next day's cycle in the traditional system.
    if hour >= 23:
        jd += 1

    chi_idx = hour_chi_index(hour)

    # Can of Giờ Tý for this day
    ty_can_idx = ((jd - 1) * 2) % 10
    # Can advances by 1 for each subsequent Chi
    can_idx = (ty_can_idx + chi_idx) % 10

    # Lucky hour check
    day_chi_idx = (jd + 1) % 12
    pattern_idx = day_chi_idx % 6
    pattern = GIO_HOANG_DAO[pattern_idx]
    is_lucky = pattern[chi_idx] == '1'

    hr = HOUR_RANGES[chi_idx]

    return {
        'can': CAN[can_idx],
        'chi': CHI[chi_idx],
        'name': f"{CAN[can_idx]} {CHI[chi_idx]}",
        'start': hr['start'],
        'end': hr['end'],
        'is_lucky': is_lucky,
    }
