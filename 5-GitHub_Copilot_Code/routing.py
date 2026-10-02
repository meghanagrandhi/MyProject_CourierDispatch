# routing.py
import math


def optimize_route(stops, start=None):
    """
    FR-004: order stops with the nearest-neighbour heuristic.
    If start (the rider's location) is given, the nearest stop to it goes first.
    No stop may be missing.
    """
    if not stops:
        return []

    remaining = list(stops)
    ordered = []
    if start is None:
        current = remaining.pop(0)
        ordered.append(current)
    else:
        current = start

    while remaining:
        nearest = min(remaining, key=lambda stop: distance_km(current, stop))
        ordered.append(nearest)
        remaining.remove(nearest)
        current = nearest

    return ordered


def plan_route(rider_location, stops):
    """
    FR-004: returns an ordered route that starts at the rider and includes
    every assigned stop, optimized with nearest-neighbour ordering.
    """
    if rider_location is None:
        raise ValueError("Rider location is required.")
    if not stops:
        return [rider_location]
    return [rider_location] + optimize_route(stops, start=rider_location)


def distance_km(point_a, point_b):
    lat1, lon1 = point_a
    lat2, lon2 = point_b
    radius = 6371.0

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c
