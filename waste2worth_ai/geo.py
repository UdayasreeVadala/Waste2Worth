from math import asin, cos, radians, sin, sqrt


def has_coordinates(location):
    return location.get("latitude") is not None and location.get("longitude") is not None


def distance_km(origin, destination):
    if not has_coordinates(origin) or not has_coordinates(destination):
        return None

    lat1 = radians(float(origin["latitude"]))
    lon1 = radians(float(origin["longitude"]))
    lat2 = radians(float(destination["latitude"]))
    lon2 = radians(float(destination["longitude"]))

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    haversine = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return round(6371 * 2 * asin(sqrt(haversine)), 2)

