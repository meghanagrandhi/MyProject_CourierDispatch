"""
Data models for the Hyperlocal Courier Dispatch & Tracking Engine.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List
from datetime import datetime


class RequestStatus(Enum):
    """Enumeration of possible courier request statuses."""
    CREATED = "Created"
    UNASSIGNED = "Unassigned"
    ASSIGNED = "Assigned"
    ACCEPTED = "Accepted"
    IN_TRANSIT = "InTransit"
    DELIVERED = "Delivered"


@dataclass
class Rider:
    """Represents a courier rider."""
    id: str
    name: str
    lat: float
    lon: float
    is_active: bool = True

    def __repr__(self) -> str:
        return f"Rider(id={self.id}, name={self.name}, lat={self.lat}, lon={self.lon}, is_active={self.is_active})"


@dataclass
class Location:
    """Represents a geographic location."""
    latitude: float
    longitude: float

    def __repr__(self) -> str:
        return f"Location(lat={self.latitude}, lon={self.longitude})"


@dataclass
class CourierRequest:
    """Represents a courier delivery request."""
    request_id: str
    pickup_location: Location
    delivery_location: Location
    parcel_details: str
    status: RequestStatus = RequestStatus.CREATED
    assigned_rider_id: Optional[str] = None
    otp: Optional[str] = None
    rejected_rider_ids: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return (
            f"CourierRequest(request_id={self.request_id}, "
            f"pickup={self.pickup_location}, delivery={self.delivery_location}, "
            f"parcel={self.parcel_details}, status={self.status.value}, "
            f"rider_id={self.assigned_rider_id}, otp={self.otp})"
        )


@dataclass
class StatusUpdate:
    """Represents a timestamped location and status update."""
    request_id: str
    rider_id: str
    latitude: float
    longitude: float
    status: RequestStatus
    timestamp: datetime = field(default_factory=datetime.now)

    def __repr__(self) -> str:
        return (
            f"StatusUpdate(request_id={self.request_id}, rider_id={self.rider_id}, "
            f"lat={self.latitude}, lon={self.longitude}, status={self.status.value}, "
            f"timestamp={self.timestamp})"
        )
