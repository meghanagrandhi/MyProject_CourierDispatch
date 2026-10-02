# matching.py
import math

from models import RequestStatus


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_nearest_rider(request, riders, radius_km=3):
    """
    FR-001:
    Return the nearest active rider within radius_km of the pickup location.
    Riders who already rejected this request are skipped (FR-003).
    If no rider is available, set the status to Unassigned and return None.
    """
    candidates = []
    for rider in riders:
        if not rider.is_active:
            continue
        if rider.id in request.rejected_rider_ids:
            continue
        distance = haversine_km(request.pickup_lat, request.pickup_lon, rider.lat, rider.lon)
        if distance <= radius_km:
            candidates.append((distance, rider))

    if not candidates:
        request.status = RequestStatus.Unassigned.value
        return None

    candidates.sort(key=lambda x: x[0])
    nearest = candidates[0][1]
    request.assigned_rider_id = nearest.id
    request.status = RequestStatus.Assigned.value
    return nearest
