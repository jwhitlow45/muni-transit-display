from datetime import datetime
from enum import StrEnum
from typing import Annotated, List

from pydantic import BaseModel, BeforeValidator, Field


def boolean_parser(v: bool | str):
    if type(v) is bool:
        return v
    return True if v == "true" or v == "True" else False


class VehicleLocationModel(BaseModel):
    Longitude: str | None = Field(None)
    Latitude: str | None = Field(None)


class MonitoredCallModel(BaseModel):
    StopPointRef: str
    StopPointName: str
    VehicleLocationAtStop: str | None = Field(None)
    VehicleAtStop: Annotated[bool, BeforeValidator(boolean_parser)]
    DestinationDisplay: str | None = Field(None)
    AimedArrivalTime: datetime | None = Field(None)
    ExpectedArrivalTime: datetime | None = Field(None)
    AimedDepartureTime: datetime | None = Field(None)
    ExpectedDepartureTime: datetime | None = Field(None)
    Distances: str | None = Field(None)


class FramedVehicleJourneyRefModel(BaseModel):
    DataFrameRef: datetime
    DatedVehicleJourneyRef: str


class OccupancyEnum(StrEnum):
    FULL = "full"
    SEATS_AVAILABLE = "seatsAvailable"
    STANDING_AVAILABLE = "standingAvailable"


class MonitoredVehicleJourneyModel(BaseModel):
    LineRef: str
    DirectionRef: str
    FramedVehicleJourneyRef: FramedVehicleJourneyRefModel
    PublishedLineName: str
    OperatorRef: str
    OriginRef: str | None = Field(None)
    OriginName: str | None = Field(None)
    DestinationRef: str | None = Field(None)
    DestinationName: str | None = Field(None)
    Monitored: Annotated[bool, BeforeValidator(boolean_parser)]
    InCongestion: Annotated[bool, BeforeValidator(boolean_parser)] | None = Field(None)
    VehicleLocation: VehicleLocationModel | None
    Bearing: float | None = Field(None)
    Occupancy: OccupancyEnum | None = Field(None)
    VehicleRef: str | None = Field(None)
    MonitoredCall: MonitoredCallModel | None


class MonitoredStopVisitModel(BaseModel):
    RecordedAtTime: datetime
    MonitoringRef: str
    MonitoredVehicleJourney: MonitoredVehicleJourneyModel | None


class StopMonitoringDeliveryModel(BaseModel):
    version: str
    ResponseTimestamp: datetime
    Status: bool
    MonitoredStopVisit: List[MonitoredStopVisitModel]
    # NOTE: Intentionally omitting MonitoredStopVisitCancellation, StopLineNotice, and StopLineNoticeCancellation for simplicity


class ServiceDeliveryModel(BaseModel):
    ResponseTimestamp: datetime
    ProducerRef: str
    Status: bool
    StopMonitoringDelivery: StopMonitoringDeliveryModel


class TransitStopMonitoringResponse(BaseModel):
    ServiceDelivery: ServiceDeliveryModel
