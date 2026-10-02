# request_service.py
import uuid

from models import CourierRequest, RequestStatus


def create_courier_request(pickup, delivery, parcel_details):
    """
    FR-002: Create a courier request.
    pickup and delivery are tuples (lat, lon).
    Reject the request if any required detail is missing.
    """
    if pickup is None or len(pickup) != 2:
        raise ValueError("Pickup location is required and must include latitude and longitude.")
    if delivery is None or len(delivery) != 2:
        raise ValueError("Delivery location is required and must include latitude and longitude.")
    if not parcel_details or not str(parcel_details).strip():
        raise ValueError("Parcel details are required.")

    pickup_lat, pickup_lon = pickup
    delivery_lat, delivery_lon = delivery

    if pickup_lat is None or pickup_lon is None:
        raise ValueError("Pickup latitude and longitude are required.")
    if delivery_lat is None or delivery_lon is None:
        raise ValueError("Delivery latitude and longitude are required.")

    request_id = f"REQ-{uuid.uuid4().hex[:8].upper()}"
    return CourierRequest(
        request_id=request_id,
        pickup_lat=float(pickup_lat),
        pickup_lon=float(pickup_lon),
        delivery_lat=float(delivery_lat),
        delivery_lon=float(delivery_lon),
        parcel_details=str(parcel_details).strip(),
        status=RequestStatus.Created.value,
    )
