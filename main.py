import json
import os

from dotenv import load_dotenv

from services.OpenData511Service import OpenData511Client

load_dotenv(".env")

OPEN_DATA_511_API_KEY = os.getenv("OPEN_DATA_511_API_KEY") or ""
OPEN_DATA_511_AGENCY_ID = os.getenv("OPEN_DATA_511_AGENCY_ID") or ""
OPEN_DATA_511_STOPCODES = os.getenv("OPEN_DATA_511_STOPCODES") or ""


def main():
    open_data_511_client = OpenData511Client(OPEN_DATA_511_API_KEY)
    open_data_stopcode_list = OPEN_DATA_511_STOPCODES.split(",")
    if len(open_data_stopcode_list) == 0:
        raise ValueError("Environment variable 'OPEN_DATA_511_STOPCODES' must be set in .env file at project root")

    with open("out.json", "w") as f:
        response = open_data_511_client.get_transit_stop_monitoring(
            OPEN_DATA_511_AGENCY_ID, ",".join(open_data_stopcode_list)
        )
        json.dump(response.json(), f)


if __name__ == "__main__":
    main()
