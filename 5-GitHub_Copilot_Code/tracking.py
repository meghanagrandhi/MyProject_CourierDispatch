# tracking.py
import time
from datetime import datetime, timezone


class TrackingUpdate:
    def __init__(self, request_id, rider_lat, rider_lon, status):
        self.request_id = request_id
        self.rider_lat = rider_lat
        self.rider_lon = rider_lon
        self.status = status
        self.timestamp = datetime.now(timezone.utc)


def update_status_and_location(request, rider_lat, rider_lon):
    """
    NFR-001:
    Record a timestamped status and location update for the request.
    """
    update = TrackingUpdate(
        request_id=request.request_id,
        rider_lat=rider_lat,
        rider_lon=rider_lon,
        status=request.status,
    )
    request.last_update = update
    return update


def send_to_sender(update):
    """NFR-001: deliver the update to the sender as a payload."""
    return {
        "request_id": update.request_id,
        "rider_lat": update.rider_lat,
        "rider_lon": update.rider_lon,
        "status": update.status,
        "timestamp": update.timestamp.isoformat(),
    }


def measure_update_latency_seconds(fn, *args, **kwargs):
    """
    NFR-001: measure how long an update takes to process, to check it is under 2 seconds.
    Returns (elapsed_seconds, result).
    """
    start = time.perf_counter()
    result = fn(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return elapsed, result
