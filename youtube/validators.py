from datetime import datetime
from typing import Optional, Tuple

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_timestamp_range(
    start_at: Optional[str],
    finish_at: Optional[str]
) -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Validates timestamp range parameters for API requests.

    Args:
        start_at: Start timestamp in ISO format
        finish_at: End timestamp in ISO format

    Returns:
        Tuple of parsed datetime objects (start_datetime, finish_datetime)

    Raises:
        ValidationError: If validation fails
    """
    # Check if both parameters are provided
    if bool(start_at) != bool(finish_at):
        raise ValidationError(
            _("Both start_at and finish_at parameters must be provided together.")
        )

    if not start_at or not finish_at:
        return None, None

    try:
        start_datetime = datetime.fromisoformat(start_at.replace('Z', '+00:00'))
        finish_datetime = datetime.fromisoformat(finish_at.replace('Z', '+00:00'))
    except ValueError:
        raise ValidationError(
            _("Invalid timestamp format. Use ISO 8601 format (e.g., 2025-11-09T00:00:00Z)")
        )

    if start_datetime > finish_datetime:
        raise ValidationError(
            _("start_at cannot be later than finish_at")
        )

    return start_datetime, finish_datetime
