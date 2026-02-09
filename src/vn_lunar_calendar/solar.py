"""SolarDate class for Gregorian calendar dates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Any

from vn_lunar_calendar.constants import DEFAULT_TIMEZONE
from vn_lunar_calendar.converter import solar_to_lunar
from vn_lunar_calendar.exceptions import DateNotExistError
from vn_lunar_calendar.utils import jd_from_date, jd_to_date

if TYPE_CHECKING:
    from vn_lunar_calendar.lunar import LunarDate


@dataclass(frozen=True)
class SolarDate:
    """Ngày dương lịch (Gregorian Calendar).

    Immutable dataclass representing a solar (Gregorian) calendar date.
    Provides conversion to lunar dates, Julian Day Numbers, and
    Can Chi / Solar Term lookups.

    Attributes:
        day: Day of the month (1-31).
        month: Month (1-12).
        year: Year (e.g. 2024).
    """

    day: int
    month: int
    year: int

    def __post_init__(self) -> None:
        """Validate date."""
        if not self.is_valid(self.day, self.month, self.year):
             raise DateNotExistError(f"Invalid solar date: {self.day}/{self.month}/{self.year}")

    @staticmethod
    def is_valid(day: int, month: int, year: int) -> bool:
        """Check if a date is valid."""
        if month < 1 or month > 12:
            return False
        if day < 1:
            return False

        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if SolarDate.is_leap_year(year):
            days_in_month[2] = 29

        return day <= days_in_month[month]

    @staticmethod
    def is_leap_year(year: int) -> bool:
        """Check if a year is a leap year (Gregorian)."""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    @classmethod
    def from_date(cls, d: date) -> SolarDate:
        """Create from python datetime.date."""
        return cls(d.day, d.month, d.year)

    @classmethod
    def from_jd(cls, jd: int) -> SolarDate:
        """Create from Julian Day Number."""
        d, m, y = jd_to_date(jd)
        return cls(d, m, y)

    @classmethod
    def from_jdn(cls, jd: int) -> SolarDate:
        """Create from Julian Day Number (alias for from_jd)."""
        return cls.from_jd(jd)

    @classmethod
    def today(cls) -> SolarDate:
        """Create for today."""
        return cls.from_date(date.today())

    def to_date(self) -> date:
        """Convert to python datetime.date."""
        return date(self.year, self.month, self.day)

    def to_jd(self) -> int:
        """Convert to Julian Day Number."""
        return jd_from_date(self.day, self.month, self.year)

    def to_jdn(self) -> int:
        """Convert to Julian Day Number (alias for to_jd)."""
        return self.to_jd()

    def get_hour_info(self, hour: int) -> dict:
        """Get full Can Chi info for a specific hour on this date.

        Args:
            hour: Clock hour (0-23).

        Returns:
            Dict with 'can', 'chi', 'name', 'start', 'end', 'is_lucky'.
        """
        from vn_lunar_calendar.canchi import get_hour_info
        return get_hour_info(hour, self.day, self.month, self.year)


    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, SolarDate):
            return NotImplemented
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        return self.day < other.day

    def __le__(self, other: Any) -> bool:
        return self < other or self == other

    def __gt__(self, other: Any) -> bool:
        return not (self <= other)

    def __ge__(self, other: Any) -> bool:
        return not (self < other)

    def to_lunar_date(self, timezone: float = DEFAULT_TIMEZONE) -> LunarDate:
        """Convert to LunarDate."""
        from vn_lunar_calendar.lunar import LunarDate

        day, month, year, leap = solar_to_lunar(self.day, self.month, self.year, timezone)
        return LunarDate(day, month, year, leap)

    def to_lunar(self, timezone: float = DEFAULT_TIMEZONE) -> LunarDate:
        """Convert to LunarDate (alias for to_lunar_date)."""
        return self.to_lunar_date(timezone)

    def solar_term(self, timezone: float = DEFAULT_TIMEZONE) -> str:
        """Get the solar term (Tiết Khí) for this date.

        Args:
            timezone: Timezone offset (default 7.0 for Vietnam).

        Returns:
            Vietnamese name of the solar term, e.g. "Đông chí".
        """
        from vn_lunar_calendar.solar_terms import get_solar_term
        return get_solar_term(self.to_jd(), timezone)

    def day_canchi(self) -> str:
        """Get the Can Chi name for this day.

        Returns:
            Can Chi string, e.g. "Canh Tuất".
        """
        from vn_lunar_calendar.canchi import day_name
        return day_name(self.to_jd())

    def hour_canchi(self) -> str:
        """Get the Can Chi name of Giờ Tý for this day.

        Returns:
            Can Chi string, e.g. "Bính Tý".
        """
        from vn_lunar_calendar.canchi import hour_name
        return hour_name(self.to_jd())

    def __str__(self) -> str:
        return f"{self.day:02d}/{self.month:02d}/{self.year}"

    def __repr__(self) -> str:
        return f"SolarDate({self.day}, {self.month}, {self.year})"
