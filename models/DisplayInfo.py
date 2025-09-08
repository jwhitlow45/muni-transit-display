from datetime import datetime
from typing import List

from pydantic import BaseModel

from models.OpenData511 import OccupancyEnum, TransitStopMonitoringResponse


class DisplayStopVisitModel(BaseModel):
    recorded_at: datetime
    line_reference: str
    line_name: str
    monitored: bool
    in_congestion: bool | None
    occupancy: OccupancyEnum | None
    vehicle_at_stop: bool | None
    aimed_arrival_time: datetime | None
    expected_arrival_time: datetime | None
    aimed_departure_time: datetime | None


class DisplayInfoModel(BaseModel):
    response_timestamp: datetime
    display_stop_visit_list: List[DisplayStopVisitModel]


def convert_transit_stop_monitoring_response_to_display_info_model(
    transit_stop_monitoring_response: TransitStopMonitoringResponse,
):
    stop_monitoring = transit_stop_monitoring_response.ServiceDelivery.StopMonitoringDelivery
    response_timestamp = stop_monitoring.ResponseTimestamp
    display_stop_visit_list = [
        DisplayStopVisitModel(
            recorded_at=stop_visit.RecordedAtTime,
            line_reference=stop_visit.MonitoredVehicleJourney.LineRef,
            line_name=stop_visit.MonitoredVehicleJourney.PublishedLineName,
            monitored=stop_visit.MonitoredVehicleJourney.Monitored,
            in_congestion=stop_visit.MonitoredVehicleJourney.InCongestion,
            occupancy=stop_visit.MonitoredVehicleJourney.Occupancy,
            vehicle_at_stop=stop_visit.MonitoredVehicleJourney.MonitoredCall.VehicleAtStop
            if stop_visit.MonitoredVehicleJourney.MonitoredCall
            else None,
            aimed_arrival_time=stop_visit.MonitoredVehicleJourney.MonitoredCall.AimedArrivalTime
            if stop_visit.MonitoredVehicleJourney.MonitoredCall
            else None,
            expected_arrival_time=stop_visit.MonitoredVehicleJourney.MonitoredCall.ExpectedArrivalTime
            if stop_visit.MonitoredVehicleJourney.MonitoredCall
            else None,
            aimed_departure_time=stop_visit.MonitoredVehicleJourney.MonitoredCall.AimedDepartureTime
            if stop_visit.MonitoredVehicleJourney.MonitoredCall
            else None,
        )
        for stop_visit in stop_monitoring.MonitoredStopVisit
        if stop_visit.MonitoredVehicleJourney  # optional from API so ensure existence
    ]

    return DisplayInfoModel(response_timestamp=response_timestamp, display_stop_visit_list=display_stop_visit_list)
