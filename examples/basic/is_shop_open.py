# Generated from: is_shop_open.rune

VALID_DAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
WEEKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}


def is_shop_open(hour: int, day: str) -> bool:
    """
    Determines if a shop is open based on the current hour and day of the week.
    Business hours are Monday through Friday, 9:00 AM to 6:00 PM (18:00).

    Args:
        hour: Integer between 0 and 23.
        day: Capitalized English weekday name.

    Returns:
        True if the shop is open, False otherwise.

    Raises:
        ValueError: If hour is out of range or day is invalid.
    """
    if not isinstance(hour, int) or hour < 0 or hour > 23:
        raise ValueError(f"Hour must be an integer between 0 and 23, got {hour}")
    if day not in VALID_DAYS:
        raise ValueError(f"Invalid day: '{day}'. Must be a capitalized English weekday name")

    return day in WEEKDAYS and 9 <= hour < 18
