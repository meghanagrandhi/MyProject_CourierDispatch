# test_courier.py
import pytest

from delivery import complete_delivery, generate_otp
from dispatch import rider_accept, rider_reject
from matching import find_nearest_rider
from models import Rider, RequestStatus
from request_service import create_courier_request
from routing import optimize_route, plan_route
from tracking import measure_update_latency_seconds, send_to_sender, update_status_and_location


def new_request():
    return create_courier_request(
        pickup=(12.9716, 77.5946),
        delivery=(12.9800, 77.6000),
        parcel_details="Books"
    )


# ---------- FR-002: create courier request ----------
def test_create_request_success():
    request = new_request()
    assert request.request_id.startswith("REQ-")
    assert request.status == RequestStatus.Created.value


def test_create_request_rejects_missing_details():
    with pytest.raises(ValueError):
        create_courier_request(pickup=(12.9716, 77.5946), delivery=None, parcel_details="Books")

    with pytest.raises(ValueError):
        create_courier_request(pickup=(12.9716, 77.5946), delivery=(12.9800, 77.6000), parcel_details="")


# ---------- FR-001: nearest active rider within 3 km ----------
def test_find_nearest_active_rider_within_3_km():
    request = new_request()
    riders = [
        Rider("R1", "Alice", 12.9722, 77.5950, True),
        Rider("R2", "Bob", 12.9900, 77.6100, True),
        Rider("R3", "Charlie", 12.9716, 77.5946, False),
    ]
    nearest = find_nearest_rider(request, riders, radius_km=3)
    assert nearest is not None
    assert nearest.id == "R1"


def test_find_nearest_rider_returns_none_when_no_active_rider_close_enough():
    request = new_request()
    riders = [
        Rider("R1", "Alice", 13.5000, 78.0000, True),
        Rider("R2", "Bob", 13.6000, 78.1000, False),
    ]
    nearest = find_nearest_rider(request, riders, radius_km=3)
    assert nearest is None
    assert request.status == RequestStatus.Unassigned.value


# ---------- FR-003: accept / reject ----------
def test_rider_accept_sets_status_accepted():
    request = new_request()
    rider_accept(request)
    assert request.status == "Accepted"


def test_reject_reassigns_to_next_rider_not_same_rider():
    request = new_request()
    riders = [
        Rider("R1", "Alice", 12.9722, 77.5950, True),
        Rider("R2", "Bob", 12.9900, 77.6100, True),
    ]
    assert find_nearest_rider(request, riders).id == "R1"
    second = rider_reject(request, riders)
    assert second.id == "R2"
    assert request.assigned_rider_id == "R2"
    assert "R1" in request.rejected_rider_ids


def test_reject_with_no_other_rider_leaves_request_unassigned():
    request = new_request()
    riders = [Rider("R1", "Alice", 12.9722, 77.5950, True)]
    find_nearest_rider(request, riders)
    assert rider_reject(request, riders) is None
    assert request.assigned_rider_id is None
    assert request.status == "Unassigned"


# ---------- FR-004: route planning and optimization ----------
def test_route_includes_all_stops_and_uses_ordered_nearest_neighbour():
    rider_location = (12.9716, 77.5946)
    stops = [(12.9770, 77.6000), (12.9800, 77.6100), (12.9750, 77.5980)]
    route = plan_route(rider_location, stops)
    assert len(route) == len(stops) + 1
    assert rider_location in route
    for stop in stops:
        assert stop in route

    optimized = optimize_route(stops)
    assert len(optimized) == len(stops)
    for stop in stops:
        assert stop in optimized


def test_plan_route_orders_stops_nearest_first():
    rider = (12.9716, 77.5946)
    far, near = (12.9800, 77.6100), (12.9720, 77.5950)
    route = plan_route(rider, [far, near])
    assert route == [rider, near, far]


# ---------- FR-005: OTP verification ----------
def test_generate_otp_is_4_digits():
    otp = generate_otp()
    assert len(otp) == 4
    assert otp.isdigit()


def test_complete_delivery_requires_correct_otp():
    request = new_request()
    request.otp = "1234"
    assert complete_delivery(request, "0000") is False
    assert request.status != "Delivered"

    assert complete_delivery(request, "1234") is True
    assert request.status == "Delivered"


# ---------- NFR-001: tracking and latency ----------
def test_tracking_update_records_timestamp_and_payload():
    request = new_request()
    request.status = "InTransit"
    update = update_status_and_location(request, 12.9720, 77.5950)
    payload = send_to_sender(update)
    assert payload["request_id"] == request.request_id
    assert payload["rider_lat"] == 12.9720
    assert payload["rider_lon"] == 77.5950
    assert "timestamp" in payload


def test_latency_measurement_reports_under_2_seconds():
    request = new_request()
    request.status = "InTransit"

    def fake_update():
        update_status_and_location(request, 12.9720, 77.5950)
        return "ok"

    latency, result = measure_update_latency_seconds(fake_update)
    assert result == "ok"
    assert latency < 2.0
