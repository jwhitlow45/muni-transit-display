from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class VehicleLocationModel(BaseModel):
    Longitude: str | None = Field(None)
    Latitude: str | None = Field(None)


class MonitoredCallModel(BaseModel):
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


class FramedVehicleJourneyRefModel(BaseModel):
    DataFrameRef: date | None = Field(None)
    DatedVehicleJourneyRef: str | None = Field(None)


class MonitoredVehicleJourneyModel(BaseModel):
    LineRef: str | None = Field(None)
    DirectionRef: str | None = Field(None)
    FramedVehicleJourneyRef: FramedVehicleJourneyRefModel
    PublishedLineName: str | None = Field(None)
    OperatorRef: str | None = Field(None)
    OriginRef: str | None = Field(None)
    OriginName: str | None = Field(None)
    DestinationRef: str | None = Field(None)
    DestinationName: str | None = Field(None)
    Monitored: bool | None = Field(None)
    InCongestion: bool | None = Field(None)
    VehicleLocation: VehicleLocationModel
    Bearing: str | None = Field(None)
    Occupancy: str | None = Field(None)
    VehicleRef: str | None = Field(None)
    MonitoredCall: MonitoredCallModel


class MonitoredStopVisitModel(BaseModel):
    RecordedAtTime: datetime
    MonitoringRef: str
    MonitoredVehicleJourney: MonitoredVehicleJourneyModel


class StopMonitoringDeliveryModel(BaseModel):
    version: str
    ResponseTimestamp: datetime
    Status: bool
    MonitoredStopVisit: List[MonitoredStopVisitModel]


class ServiceDeliveryModel(BaseModel):
    ResponseTimestamp: datetime
    ProducerRef: str
    Status: bool
    StopMonitoringDelivery: StopMonitoringDeliveryModel


class TransitStopMonitoringResponse(BaseModel):
    ServiceDelivery: ServiceDeliveryModel
