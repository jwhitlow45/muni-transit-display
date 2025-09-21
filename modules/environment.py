# import env vars
import os

from dotenv import load_dotenv

load_dotenv(".env")

OPEN_DATA_511_API_KEY_0 = os.getenv("OPEN_DATA_511_API_KEY_0") or ""
OPEN_DATA_511_API_KEY_1 = os.getenv("OPEN_DATA_511_API_KEY_1") or ""
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

LINE_REFERENCES = os.getenv("LINE_REFERENCES") or ""
LINE_STOPCODES = os.getenv("LINE_STOPCODES") or ""
LINE_SYMBOLS = os.getenv("LINE_SYMBOLS") or ""

# process env vars
OPEN_DATA_511_STOPCODE_LIST = [stopcode for stopcode in OPEN_DATA_511_STOPCODES.split(",") if stopcode]
if len(OPEN_DATA_511_STOPCODE_LIST) == 0:
    open_data_stop_code_env_var_name = f"{OPEN_DATA_511_STOPCODES=}".split("=")[0]
    raise ValueError(
        f"Environment variable '{open_data_stop_code_env_var_name}' must be set in .env file at project root"
    )

LINE_REFERENCE_LIST = LINE_REFERENCES.split(",")
LINE_STOPCODE_LIST = LINE_STOPCODES.split(",")
LINE_SYMBOL_LIST = LINE_SYMBOLS.split(",")
if not len(LINE_REFERENCE_LIST) == len(LINE_STOPCODE_LIST) == len(LINE_SYMBOL_LIST):
    raise ValueError(
        "Environment variables relating to line reference disambiguation must all have the same number of entries"
    )
