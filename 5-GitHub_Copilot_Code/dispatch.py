# dispatch.py
from matching import find_nearest_rider
from models import RequestStatus


def rider_accept(request):
    """FR-003: rider accepts the request and the sender is notified."""
    request.status = RequestStatus.Accepted.value
    return f"Notification sent to sender for request {request.request_id}."


def rider_reject(request, riders=None):
    """
    FR-003: rider rejects the request.
    Records the rejecting rider, clears the assignment and starts reassignment
    to the next nearest eligible rider. Never reassigns to a rider who rejected.
    """
    if request.assigned_rider_id is not None and request.assigned_rider_id not in request.rejected_rider_ids:
        request.rejected_rider_ids.append(request.assigned_rider_id)
    request.assigned_rider_id = None

    if not riders:
        request.status = RequestStatus.Unassigned.value
        return None
    return find_nearest_rider(request, riders)
