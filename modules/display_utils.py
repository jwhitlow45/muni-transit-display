from datetime import datetime


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


def get_status_led_colors(update_datetime: datetime):
    now = datetime.now()
    difference = now - update_datetime

    if difference.seconds < 2:
        return Colors.GREEN
    if difference.seconds < 4:
        return Colors.YELLOW
    if difference.seconds < 6:
        return Colors.RED

    # return white in case of negative value (update_datetime is somehow in future relative to now), should be impossible
    return Colors.WHITE


def get_text_center_x_pos(text: str, character_width: int, display_width: int):
    text_length = len(text)
    text_width = text_length * character_width
    center_display_pixel = (display_width - 1) // 2  # bias left
    text_offset = text_width // 2  # bias left
    return center_display_pixel - text_offset
