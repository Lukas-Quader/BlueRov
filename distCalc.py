from numpy import sin, cos, arccos, pi, round
from math import sin, cos, atan2, sqrt, radians, asin, degrees

def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians
# Die Funktion gibt die Entfernung zwischen zwei Koordinaten in Meter zurück
def getDistanceBetweenPointsNew(latitude1, longitude1, latitude2, longitude2):
    
    theta = longitude1 - longitude2
    
    distance = 60 * 1.1515 * rad2deg(
        arccos(
            (sin(deg2rad(latitude1)) * sin(deg2rad(latitude2))) + 
            (cos(deg2rad(latitude1)) * cos(deg2rad(latitude2)) * cos(deg2rad(theta)))
        )
    )
    return round(distance * 1609.344, 3) 

# Die Funktion gibt ein Tupel mit den Breiten- und Längengraden der Zielkoordinate in Dezimalgrad zurück.
# latitude: die Breitengrad-Koordinate der Startposition in Dezimalgrad
# longitude: die Längengrad-Koordinate der Startposition in Dezimalgrad
# bearing: die Richtung in Grad, in die das Objekt reist (0 Grad ist Norden, 90 Grad ist Osten)
# speed: die Geschwindigkeit des Objekts in km/h
# time: die Zeitdauer, für die das Objekt reist, in Sekunden
def getDestinationCoordinates(latitude, longitude, bearing, speed, time):
    R = 6371  # Earth's radius in km
    
    # convert latitude and longitude to radians
    lat1 = radians(latitude)
    lon1 = radians(longitude)
    
    # convert bearing to radians
    bearing = radians(bearing)
    
    # convert speed to km/s
    speed = speed / 3600
    
    # calculate distance
    distance = speed * time
    
    # calculate new latitude and longitude
    lat2 = asin(sin(lat1) * cos(distance/R) + cos(lat1) * sin(distance/R) * cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(distance/R) * cos(lat1), cos(distance/R) - sin(lat1) * sin(lat2))
    
    # convert back to degrees
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    
    return (lat2, lon2)
    

def main(args=None):
    lat1 = 53.870004
    lat2 = 53.86961705908918
    lon1 = 10.699840
    lon2 = 11.004974481161332
    dist = getDistanceBetweenPointsNew(lat1, lon1, lat2, lon2)
    newPosition = getDestinationCoordinates(lat1, lon1, 90, 20, 3600)


    print(str(dist) + ' m')
    print(newPosition)

if __name__ == '__main__':
    main()
