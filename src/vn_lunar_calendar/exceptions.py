"""Custom exceptions for vn_lunar_calendar."""


class LunarCalendarError(Exception):
    """Base exception for vn_lunar_calendar."""


class DateNotExistError(LunarCalendarError):
    """Raised when a date does not exist.

    Examples:
        - Solar: February 30 (never exists)
        - Lunar: A leap month that doesn't occur in the given year
    """


class OutOfRangeError(LunarCalendarError):
    """Raised when a date is outside the supported calculation range."""
