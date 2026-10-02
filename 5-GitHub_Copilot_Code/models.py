# models.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class RequestStatus(str, Enum):
    Created = "Created"
    Unassigned = "Unassigned"
    Assigned = "Assigned"
    Accepted = "Accepted"
    InTransit = "InTransit"
    Delivered = "Delivered"


@dataclass
class Rider:
    id: str
    name: str
    lat: float
    lon: float
    is_active: bool = True


@dataclass
class CourierRequest:
    request_id: str
    pickup_lat: float
    pickup_lon: float
    delivery_lat: float
    delivery_lon: float
    parcel_details: str
    status: str = RequestStatus.Created.value
    assigned_rider_id: Optional[str] = None
    otp: Optional[str] = None
    rejected_rider_ids: List[str] = field(default_factory=list)
