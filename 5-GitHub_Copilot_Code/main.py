# main.py
from delivery import complete_delivery, generate_otp
from dispatch import rider_accept, rider_reject
from matching import find_nearest_rider
from models import Rider
from request_service import create_courier_request
from routing import optimize_route, plan_route
from tracking import measure_update_latency_seconds, send_to_sender, update_status_and_location


def main():
    riders = [
        Rider(id="R1", name="Alice", lat=12.9716, lon=77.5946, is_active=True),
        Rider(id="R2", name="Bob", lat=12.9750, lon=77.6010, is_active=True),
        Rider(id="R3", name="Charlie", lat=12.9850, lon=77.6200, is_active=False),
    ]

    # FR-002: sender creates a courier request
    request = create_courier_request(
        pickup=(12.9719, 77.5940),
        delivery=(12.9800, 77.6100),
        parcel_details="Electronics parcel",
    )
    print("Request created:", request.request_id, "| status:", request.status)

    # FR-001: match the nearest active rider within 3 km
    first = find_nearest_rider(request, riders)
    print("Nearest rider:", first)

    # FR-003: the first rider rejects, so the request is reassigned
    nearest = rider_reject(request, riders)
    print("After rejection, reassigned to:", nearest)

    if nearest:
        print(rider_accept(request))
        print("Request status:", request.status)

        # FR-004: plan and optimize the route
        stops = [(12.9720, 77.5945), (12.9780, 77.6050), (12.9800, 77.6100)]
        route = plan_route((nearest.lat, nearest.lon), stops)
        print("Planned route:", route)
        print("Optimized stops:", optimize_route(stops))

        # FR-005: generate the OTP for the delivery
        request.otp = generate_otp()
        print("Generated OTP:", request.otp)

        # NFR-001: tracking update and latency
        update = update_status_and_location(request, nearest.lat, nearest.lon)
        print("Tracking payload:", send_to_sender(update))
        latency, _ = measure_update_latency_seconds(
            update_status_and_location, request, nearest.lat, nearest.lon
        )
        print("Update latency (seconds):", latency)
        print("Latency under 2s:", latency < 2)

        # FR-005: complete delivery with the OTP
        completed = complete_delivery(request, request.otp)
        print("Delivery completed:", completed)
        print("Final status:", request.status)
    else:
        print("No rider available. Request status:", request.status)


if __name__ == "__main__":
    main()
