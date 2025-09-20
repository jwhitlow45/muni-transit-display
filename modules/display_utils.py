from datetime import datetime, timezone


# Common RGB color values as tuples
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    GRAY = (128, 128, 128)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    BROWN = (165, 42, 42)
    PINK = (255, 192, 203)
    LIME = (0, 255, 0)
    NAVY = (0, 0, 128)
    TEAL = (0, 128, 128)
    OLIVE = (128, 128, 0)
    MAROON = (128, 0, 0)
    SILVER = (192, 192, 192)
    GOLD = (255, 215, 0)
    MUNI = (255, 130, 0)
    MUNI_LESS = (150, 30, 0)
    MUNI_ALT = (100, 0, 180)
    MUNI_ALT_LESS = (60, 0, 140)


def get_status_led_colors(update_datetime: datetime, refresh_interval_seconds: int):
    """Status LED that transitions from green to yellow to red as update_datetime becomes more stale
    Green -> update_datetime is < (refresh_interval_seconds * 2) seconds in the past
    Yellow -> update_datetime is < (refresh_interval_seconds * 4) seconds in the past
    RED -> update_datetime is >= (refresh_interval_seconds * 4) seconds in the past

    Args:
        update_datetime (datetime): time when update was performed
        refresh_interval_seconds (int): refresh interval in seconds

    Returns:
        (int, int, int): tuple representing led color in RGB
    """
    now = datetime.now(timezone.utc)
    difference = now - update_datetime

    if difference.seconds < refresh_interval_seconds * 2:
        return Colors.GREEN
    if difference.seconds < refresh_interval_seconds * 4:
        return Colors.YELLOW

    return Colors.RED  # information is very out of date


def get_text_center_x_pos(text: str, character_width: int, display_width: int):
    """Calculates the x position for centering text on a display

    Args:
        text (str): text to center
        character_width (int): width of a character in the used font
        display_width (int): width of the display to center text on

    Returns:
        int: x position which will center the text on the display
    """
    text_length = len(text)
    text_width = text_length * character_width
    center_display_pixel = (display_width - 1) // 2  # bias left
    text_offset = text_width // 2  # bias left
    return center_display_pixel - text_offset
