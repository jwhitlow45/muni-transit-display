from datetime import datetime
from typing import List

from pydantic import BaseModel

import models.OpenData511 as OpenData511Models


class DisplayStopVisitModel(BaseModel):
    recorded_at: datetime
    line_reference: str
    line_name: str
    monitored: bool
    in_congestion: bool | None
    occupancy: OpenData511Models.OccupancyEnum | None
    vehicle_at_stop: bool | None
    aimed_arrival_time: datetime | None
    expected_arrival_time: datetime | None
    aimed_departure_time: datetime | None


class DisplayInfoModel(BaseModel):
    response_timestamp: datetime
    display_stop_visit_list: List[DisplayStopVisitModel]
