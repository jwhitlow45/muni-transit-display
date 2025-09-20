import os
import threading
from time import sleep

from dotenv import load_dotenv
from httpx import HTTPStatusError

from models.DisplayInfo import DisplayInfoModel
from modules.display_utils import Colors, get_status_led_colors, get_text_center_x_pos
from modules.logger import logger
from modules.rgbmatrix_configurer import get_rgb_matrix
from modules.rgbmatrix_importer import get_rgb_matrix_imports
from services.OpenData511 import OpenData511Client

load_dotenv(".env")

_api_key_1 = os.getenv("OPEN_DATA_511_API_KEY_1")

OPEN_DATA_511_API_KEY_0 = os.getenv("OPEN_DATA_511_API_KEY_0") or ""
OPEN_DATA_511_API_KEY_1 = _api_key_1 if _api_key_1 and "<" not in _api_key_1 else None
OPEN_DATA_511_AGENCY_ID = os.getenv("OPEN_DATA_511_AGENCY_ID") or ""
OPEN_DATA_511_STOPCODES = os.getenv("OPEN_DATA_511_STOPCODES") or ""

LED_MATRIX_COLS = int(os.getenv("LED_MATRIX_COLS") or -1)
LED_MATRIX_ROWS = int(os.getenv("LED_MATRIX_ROWS") or -1)
LED_MATRIX_CHAIN_LENGTH = int(os.getenv("LED_MATRIX_CHAIN_LENGTH") or -1)
LED_MATRIX_PARALLEL = int(os.getenv("LED_MATRIX_PARALLEL") or -1)
LED_MATRIX_GPIO_SLOWDOWN = int(os.getenv("LED_MATRIX_GPIO_SLOWDOWN") or -1)
LED_MATRIX_HARDWARE_MAPPING = os.getenv("LED_MATRIX_HARDWARE_MAPPING") or ""
LED_MATRIX_MAX_BRIGHTNESS = int(os.getenv("LED_MATRIX_MAX_BRIGHTNESS") or -1)

REFRESH_API_INTERVAL_SECONDS = int(os.getenv("REFRESH_API_INTERVAL_SECONDS") or -1)
REFRESH_DISPLAY_INTERVAL_SECONDS = int(os.getenv("REFRESH_DISPLAY_INTERVAL_SECONDS") or -1)

RGBMatrix_, _, graphics = get_rgb_matrix_imports()

# define globally so it is available to both threads
display_info_dict: dict[str, DisplayInfoModel] | None = None
display_info_lock = threading.Lock()


def main():
    threads = [
        # threading.Thread(target=display_loop),
        threading.Thread(target=api_loop)
    ]
    [thread.start() for thread in threads]

    # unreachable as threads are while True loops, but waiting for their completion keeps the program running
    [thread.join() for thread in threads]


def display_loop():
    global display_info_dict

    # use bottom-right corner of display for status LED
    status_led_xy = (LED_MATRIX_COLS - 1, LED_MATRIX_ROWS - 1)

    # setup font
    font = graphics.Font()
    font.LoadFont("fonts/5x7.bdf")
    font_color = graphics.Color(*Colors.MUNI_ALT_LESS)
    font_color_1 = graphics.Color(*Colors.MUNI_LESS)

    # setup matrix and canvas for drawing to display
    matrix = get_rgb_matrix(
        cols=LED_MATRIX_COLS,
        rows=LED_MATRIX_ROWS,
        chain_length=LED_MATRIX_CHAIN_LENGTH,
        parallel=LED_MATRIX_PARALLEL,
        gpio_slowdown=LED_MATRIX_GPIO_SLOWDOWN,
        hardware_mapping=LED_MATRIX_HARDWARE_MAPPING,
        matrix_brightness=LED_MATRIX_MAX_BRIGHTNESS,
    )
    canvas = matrix.CreateFrameCanvas()

    while True:
        canvas.Clear()
        # display_info_dict = {
        #     "13516": DisplayInfoModel(response_timestamp=datetime.now(), stop_visit_list=[StopVisitModel()]),
        #     "13517": DisplayInfoModel(
        #         response_timestamp=datetime.now(),
        #         stop_visit_list=[
        #             StopVisitModel(
        #                 recorded_at=datetime.now(),
        #             )
        #         ],
        #     ),
        # }
        with display_info_lock:
            if display_info_dict is not None:
                for stopcode, display_info in display_info_dict.items():
                    display_info.stop_visit_list[0]

                canvas.SetPixel(
                    *status_led_xy,
                    *get_status_led_colors(display_info_dict["13516"].response_timestamp, REFRESH_API_INTERVAL_SECONDS),
                )
            else:
                text0 = "123"
                text1 = "123"
                graphics.DrawText(
                    canvas, font, get_text_center_x_pos(text0, 5, LED_MATRIX_COLS), font.height, font_color, text0
                )
                graphics.DrawText(
                    canvas, font, get_text_center_x_pos(text1, 5, LED_MATRIX_COLS), font.height * 2, font_color, text1
                )
                graphics.DrawText(
                    canvas,
                    font,
                    get_text_center_x_pos("48W 12 12", 5, LED_MATRIX_COLS),
                    font.height * 3,
                    font_color,
                    "48OB  9 12",
                )
                graphics.DrawText(
                    canvas,
                    font,
                    get_text_center_x_pos("48W  9 12", 5, LED_MATRIX_COLS),
                    font.height * 4,
                    font_color_1,
                    "48IA  9 12",
                )

            canvas = matrix.SwapOnVSync(canvas)  # draw canvas, set returned canvas as new canvas to prevent flickering

        sleep(REFRESH_DISPLAY_INTERVAL_SECONDS)


def api_loop():
    global display_info_dict

    client_list = [OpenData511Client(OPEN_DATA_511_API_KEY_0)]
    if OPEN_DATA_511_API_KEY_1:
        client_list.append(OpenData511Client(OPEN_DATA_511_API_KEY_1))

    open_data_stopcode_list = [stopcode for stopcode in OPEN_DATA_511_STOPCODES.split(",") if stopcode]

    if len(open_data_stopcode_list) == 0:
        open_data_stop_code_env_var_name = f"{OPEN_DATA_511_STOPCODES=}".split("=")[0]
        raise ValueError(
            f"Environment variable '{open_data_stop_code_env_var_name}' must be set in .env file at project root"
        )

    client_idx = 0

    while True:
        # utilizing a dict to isolate each request such that
        display_info_dict_staged: dict[str, DisplayInfoModel] = {}

        for stopcode in open_data_stopcode_list:
            try:
                display_info_dict_staged[stopcode] = (
                    client_list[client_idx]
                    .get_transit_stop_monitoring(OPEN_DATA_511_AGENCY_ID, stopcode)
                    .convert_to_display_info()
                )
            except HTTPStatusError as err:
                # fail program on 401
                if err.response.status_code == 401:
                    raise err
                logger.error(
                    f"API Request Failed for stopcode {stopcode}: {err.response.status_code} {err.response.text}\n{err.response.json()}"
                )

        with display_info_lock:
            display_info_dict = display_info_dict or {} | display_info_dict_staged

        # round-robin api requests across clients to spread api usage across api keys
        # this could be done smarter to avoid detection of single client using multiple api keys, but since opendata511
        # won't respond to my rate limit increase request I doubt they'll catch this
        client_idx += 1
        if client_idx >= len(client_list):
            client_idx = 0

        sleep(REFRESH_API_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
