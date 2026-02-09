"""Lucky Hours (Giờ Hoàng Đạo) calculation.

Determines the 6 lucky (Hoàng Đạo) and 6 unlucky (Hắc Đạo) double-hours
of a day based on the day's Earthly Branch (Địa Chi).

Based on the algorithm in docs/PRD/02_Algorithm_Design.md §2.8.
"""

from typing import Dict, List

from vn_lunar_calendar.constants import CHI, GIO_HOANG_DAO

# Hour ranges for the 12 double-hours (Canh)
_HOUR_RANGES = [
    (23, 1),   # Tý
    (1, 3),    # Sửu
    (3, 5),    # Dần
    (5, 7),    # Mão
    (7, 9),    # Thìn
    (9, 11),   # Tỵ
    (11, 13),  # Ngọ
    (13, 15),  # Mùi
    (15, 17),  # Thân
    (17, 19),  # Dậu
    (19, 21),  # Tuất
    (21, 23),  # Hợi
]


def get_lucky_hours(jd: int) -> List[Dict]:
    """Get the lucky hours (Giờ Hoàng Đạo) for a day.

    Each day is divided into 12 double-hours named after the 12 Earthly
    Branches (Địa Chi). Based on the day's own Chi, 6 of these are
    considered auspicious (Hoàng Đạo) and 6 inauspicious (Hắc Đạo).

    Args:
        jd: Julian Day Number.

    Returns:
        List of 12 dicts, each with:
        - 'name': Earthly Branch name (str, e.g. "Tý")
        - 'start': Start hour (int, 0-23)
        - 'end': End hour (int, 1-23)
        - 'is_lucky': Whether this is a Hoàng Đạo hour (bool)

    Examples:
        >>> hours = get_lucky_hours(2460310)
        >>> len(hours)
        12
        >>> sum(1 for h in hours if h['is_lucky'])
        6
    """
    chi_of_day = (jd + 1) % 12
    pattern = GIO_HOANG_DAO[chi_of_day % 6]

    hours: List[Dict] = []
    for i in range(12):
        start, end = _HOUR_RANGES[i]
        hours.append({
            'name': CHI[i],
            'start': start,
            'end': end,
            'is_lucky': pattern[i] == '1',
        })

    return hours


def get_lucky_hour_names(jd: int) -> List[str]:
    """Get just the names of the lucky hours for a day.

    Args:
        jd: Julian Day Number.

    Returns:
        List of 6 Chi names that are lucky, e.g. ["Tý", "Sửu", ...].
    """
    return [h['name'] for h in get_lucky_hours(jd) if h['is_lucky']]
