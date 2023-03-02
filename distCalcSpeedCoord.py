import math

def getDestinationCoordinates(latitude, longitude, speed_x, speed_y, time):
    radius = 6371  # radius of the Earth in km

    # convert latitude and longitude to radians
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)

    # calculate speed and bearing from components
    speed = math.sqrt(speed_x ** 2 + speed_y ** 2)
    bearing = math.atan2(speed_y, speed_x)

    # convert speed from m/s to km/h
    speed_kmh = speed * 3.6

    # calculate the distance traveled in km
    distance = speed_kmh * (time / 3600)

    # calculate the new coordinates
    lat2 = math.asin(math.sin(lat1) * math.cos(distance / radius) +
                     math.cos(lat1) * math.sin(distance / radius) * math.cos(bearing))

    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / radius) * math.cos(lat1),
                             math.cos(distance / radius) - math.sin(lat1) * math.sin(lat2))

    # convert new coordinates to degrees
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return lat2, lon2
