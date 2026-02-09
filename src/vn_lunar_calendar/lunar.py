"""LunarDate class for Vietnamese Lunar Calendar dates."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import TYPE_CHECKING, Any

from vn_lunar_calendar.constants import DEFAULT_TIMEZONE
from vn_lunar_calendar.converter import lunar_to_solar
from vn_lunar_calendar.exceptions import DateNotExistError

if TYPE_CHECKING:
    from vn_lunar_calendar.solar import SolarDate


@dataclass(frozen=True)
class LunarDate:
    """Ngày âm lịch (Vietnamese Lunar Calendar).

    Immutable dataclass representing a Vietnamese lunar calendar date.
    Provides conversion to solar dates, Can Chi lookups, lucky hours,
    and solar term information.

    Attributes:
        day: Lunar day (1-30).
        month: Lunar month (1-12).
        year: Lunar year (e.g. 2024).
        is_leap: Whether this is a leap month (tháng nhuận).
    """

    day: int
    month: int
    year: int
    is_leap: bool = False

    def __post_init__(self) -> None:
        """Validate date."""
        # Simple validation
        if not (1 <= self.month <= 12):
             raise DateNotExistError(f"Invalid lunar month: {self.month}")
        if not (1 <= self.day <= 30):
             raise DateNotExistError(f"Invalid lunar day: {self.day}")

    def to_solar_date(self, timezone: float = DEFAULT_TIMEZONE) -> SolarDate:
        """Convert to SolarDate."""
        from vn_lunar_calendar.solar import SolarDate

        d, m, y = lunar_to_solar(self.day, self.month, self.year, self.is_leap, timezone)
        return SolarDate(d, m, y)

    def to_date(self, timezone: float = DEFAULT_TIMEZONE) -> date:
        """Convert to python datetime.date.

        Args:
            timezone: Timezone offset (default 7.0 for Vietnam).

        Returns:
            Corresponding Gregorian date.
        """
        solar = self.to_solar_date(timezone)
        return solar.to_date()

    @classmethod
    def from_solar_date(cls, solar_date: SolarDate, timezone: float = DEFAULT_TIMEZONE) -> LunarDate:
        """Create from SolarDate."""
        return solar_date.to_lunar_date(timezone)

    @classmethod
    def from_date(cls, d: date, timezone: float = DEFAULT_TIMEZONE) -> LunarDate:
        """Create from python datetime.date."""
        from vn_lunar_calendar.solar import SolarDate
        return SolarDate.from_date(d).to_lunar_date(timezone)

    @classmethod
    def today(cls, timezone: float = DEFAULT_TIMEZONE) -> LunarDate:
        """Create for today."""
        return cls.from_date(date.today(), timezone)

    # --- Can Chi methods ---

    def year_name(self) -> str:
        """Get the Can Chi name for this lunar year.

        Returns:
            Can Chi string, e.g. "Giáp Thìn" for 2024.
        """
        from vn_lunar_calendar.canchi import year_name
        return year_name(self.year)

    def month_name(self) -> str:
        """Get the Can Chi name for this lunar month.

        Returns:
            Can Chi string, e.g. "Bính Dần" for month 1.
        """
        from vn_lunar_calendar.canchi import month_name
        return month_name(self.month, self.year)

    def day_name(self, timezone: float = DEFAULT_TIMEZONE) -> str:
        """Get the Can Chi name for this day.

        Args:
            timezone: Timezone offset for solar conversion.

        Returns:
            Can Chi string, e.g. "Canh Tuất".
        """
        from vn_lunar_calendar.canchi import day_name
        jd = self.to_solar_date(timezone).to_jd()
        return day_name(jd)

    def hour_name(self, timezone: float = DEFAULT_TIMEZONE) -> str:
        """Get the Can Chi name of Giờ Tý for this day.

        Args:
            timezone: Timezone offset for solar conversion.

        Returns:
            Can Chi string, e.g. "Bính Tý".
        """
        from vn_lunar_calendar.canchi import hour_name
        jd = self.to_solar_date(timezone).to_jd()
        return hour_name(jd)

    # --- Solar Term ---

    def solar_term(self, timezone: float = DEFAULT_TIMEZONE) -> str:
        """Get the solar term (Tiết Khí) for this date.

        Args:
            timezone: Timezone offset.

        Returns:
            Vietnamese name of the solar term.
        """
        from vn_lunar_calendar.solar_terms import get_solar_term
        jd = self.to_solar_date(timezone).to_jd()
        return get_solar_term(jd, timezone)

    # --- Lucky Hours ---

    def lucky_hours(self, timezone: float = DEFAULT_TIMEZONE) -> list[dict]:
        """Get the lucky hours (Giờ Hoàng Đạo) for this day.

        Args:
            timezone: Timezone offset for solar conversion.

        Returns:
            List of 12 dicts with keys: name, start, end, is_lucky.
        """
        from vn_lunar_calendar.lucky_hours import get_lucky_hours
        jd = self.to_solar_date(timezone).to_jd()
        return get_lucky_hours(jd)

    # --- Comparison operators ---

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, LunarDate):
            return NotImplemented

        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month

        # Same year and month
        if self.is_leap != other.is_leap:
            return not self.is_leap # False (Regular) < True (Leap)

        return self.day < other.day

    def __le__(self, other: Any) -> bool:
        return self < other or self == other

    def __gt__(self, other: Any) -> bool:
        return not (self <= other)

    def __ge__(self, other: Any) -> bool:
        return not (self < other)

    def __str__(self) -> str:
        leap_str = " (Nhuận)" if self.is_leap else ""
        return f"{self.day:02d}/{self.month:02d}/{self.year}{leap_str}"

    def __repr__(self) -> str:
        return f"LunarDate({self.day}, {self.month}, {self.year}, is_leap={self.is_leap})"
