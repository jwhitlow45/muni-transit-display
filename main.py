import os
from pprint import pprint

from dotenv import load_dotenv

from models.DisplayInfo import convert_transit_stop_monitoring_response_to_display_info_model
from services.OpenData511 import OpenData511Client

load_dotenv(".env")

OPEN_DATA_511_API_KEY = os.getenv("OPEN_DATA_511_API_KEY") or ""
OPEN_DATA_511_AGENCY_ID = os.getenv("OPEN_DATA_511_AGENCY_ID") or ""
OPEN_DATA_511_STOPCODES = os.getenv("OPEN_DATA_511_STOPCODES") or ""


def main():
    open_data_511_client = OpenData511Client(OPEN_DATA_511_API_KEY)
    open_data_stopcode_list = [stopcode for stopcode in OPEN_DATA_511_STOPCODES.split(",") if stopcode]

    if len(open_data_stopcode_list) == 0:
        open_data_stop_code_env_var_name = f"{OPEN_DATA_511_STOPCODES=}".split("=")[0]
        raise ValueError(
            f"Environment variable '{open_data_stop_code_env_var_name}' must be set in .env file at project root"
        )

    transit_stop_monitoring_response = open_data_511_client.get_transit_stop_monitoring(
        OPEN_DATA_511_AGENCY_ID, open_data_stopcode_list[0]
    )
    display_info = convert_transit_stop_monitoring_response_to_display_info_model(transit_stop_monitoring_response)

    pprint(display_info.model_dump())
    print(type(display_info))


if __name__ == "__main__":
    main()
