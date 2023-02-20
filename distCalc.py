from numpy import sin, cos, arccos, pi, round
from math import sin, cos, atan2, sqrt, radians, asin, degrees

def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians


# Die Funktion gibt die Entfernung zwischen zwei Koordinaten in Meter zurück
def getDistance(latitude1, longitude1, latitude2, longitude2):
    
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
def getDestination(latitude, longitude, bearing, speed, time):
    R = 6370.693  # Erdradius in km
    
    # umwandeln von Breitengrad und Längengrad in Radiant
    lat1 = radians(latitude)
    lon1 = radians(longitude)
    
    # umwandeln der Richtung in Radiant
    bearing = radians(bearing)
    
    # umwandeln von km/h zu km/s
    speed = speed / 3600
    
    # distance berechnen
    distance = speed * time
    
    # berechnen der neuen latitude und longitude
    lat2 = asin(sin(lat1) * cos(distance/R) + cos(lat1) * sin(distance/R) * cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(distance/R) * cos(lat1), cos(distance/R) - sin(lat1) * sin(lat2))
    
    # zurück zu degrees umwandeln
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    
    return (lat2, lon2)
    

def main(args=None):
    lat1 = 53.870004
    lon1 = 10.699840
    newPosition = getDestination(lat1, lon1, 90, 20, 3600)
    lat2 = newPosition[0]
    lon2 = newPosition[1]
    dist = getDistance(lat1, lon1, lat2, lon2)
    
    for x in range(6): 
       newPosition = getDestination(lat1, lon1, 90 + 10 * x, 10 * x, 1) 
       print(newPosition)

    print(str(dist) + ' m')
    print(newPosition)



if __name__ == '__main__':
    main()
