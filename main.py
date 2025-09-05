import os
from pprint import pprint

from services.OpenData511Service import OpenData511Agency, OpenData511Client

OPEN_DATA_511_API_KEY = os.getenv("OPEN_DATA_511_API_KEY") or ""


def main():
    open_data_511_client = OpenData511Client(OPEN_DATA_511_API_KEY)
    pprint(
        open_data_511_client.get_transit_stop_monitoring(
            OpenData511Agency.SFMTA, "13516"
        ).json()
    )  # 26th & De Haro, North
    pprint(
        open_data_511_client.get_transit_stop_monitoring(
            OpenData511Agency.SFMTA, "13516"
        ).json()
    )  # 26th & De Haro, South


if __name__ == "__main__":
    main()
