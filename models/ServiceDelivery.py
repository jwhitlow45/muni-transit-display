from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class VehicleLocationType(BaseModel):
    Longitude: str | None = Field(None)
    Latitude: str | None = Field(None)


class MonitoredCallType(BaseModel):
    StopPointRef: str | None = Field(None)
    StopPointName: str | None = Field(None)
    VehicleLocationAtStop: str | None = Field(None)
    VehicleAtStop: str | None = Field(None)
    DestinationDisplay: str | None = Field(None)
    AimedArrivalTime: datetime | None = Field(None)
    ExpectedArrivalTime: datetime | None = Field(None)
    AimedDepartureTime: datetime | None = Field(None)
    ExpectedDepartureTime: str | None = Field(None)
    Distances: str | None = Field(None)


class FramedVehicleJourneyRefType(BaseModel):
    DataFrameRef: date | None = Field(None)
    DatedVehicleJourneyRef: str | None = Field(None)


class MonitoredVehicleJourneyType(BaseModel):
    LineRef: str | None = Field(None)
    DirectionRef: str | None = Field(None)
    FramedVehicleJourneyRef: FramedVehicleJourneyRefType
    PublishedLineName: str | None = Field(None)
    OperatorRef: str | None = Field(None)
    OriginRef: str | None = Field(None)
    OriginName: str | None = Field(None)
    DestinationRef: str | None = Field(None)
    DestinationName: str | None = Field(None)
    Monitored: bool | None = Field(None)
    InCongestion: bool | None = Field(None)
    VehicleLocation: VehicleLocationType
    Bearing: str | None = Field(None)
    Occupancy: str | None = Field(None)
    VehicleRef: str | None = Field(None)
    MonitoredCall: MonitoredCallType


class MonitoredStopVisitType(BaseModel):
    RecordedAtTime: datetime
    MonitoringRef: str
    MonitoredVehicleJourney: MonitoredVehicleJourneyType


class StopMonitoringDeliveryType(BaseModel):
    version: str
    ResponseTimestamp: datetime
    Status: bool
    MonitoredStopVisit: List[MonitoredStopVisitType]


class ServiceDeliveryType(BaseModel):
    ResponseTimestamp: datetime
    ProducerRef: str
    Status: bool
    StopMonitoringDelivery: StopMonitoringDeliveryType


class ServiceDeliveryModel(BaseModel):
    ServiceDelivery: ServiceDeliveryType


__all__ = ["ServiceDeliveryModel"]
