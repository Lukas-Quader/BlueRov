import rclpy
from std_msgs.msg import String
from numpy import sin, cos, arccos, pi, round
from math import sin, cos, atan2, sqrt, radians, asin, degrees

gpsDataString = "Hallo GPS"
dvlDataString = "DVL funktiont nicht"

def dvl_callback(msg):
    # globale Sensordaten Variablen
    global dvlDataString 
    dvlDataString = str(msg.data)

    print("Empfangene DVL-Daten: {}".format(msg.data))

def gps_callback(msg):
    # globale Sensordaten Variablen
    global gpsDataString
    gpsDataString = str(msg.data)

    print("Empfangene GPS-Daten: {}".format(msg.data))


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

def getTransPosition(lat, lon, x, y):
    
    # Berechnen einer neuen Koordinate die in x und y länge in metern entfernd ist
    # lat (float): latitude der Referenzkoordinate
    # lon (float): longitude der Referenzkoordinate
    # dx (float): Distanz zur Referenzkoordinate in der ost-west Richtung (DVL)
    # dy (float): Distanz zur Referenzkoordinate in der nord-süd Richtung (DVL)
    # Return:
    # returned die neue Koordinate als Tuple
    
    # Radius der Erde
    R = 6378137.0

    # Umwandeln zu radians
    lat_rad = radians(lat)
    lon_rad = radians(lon)

    # Umwandeln der Distanz in Metern zu radians
    d_lat = 1.0
    d_lat = y / R
    d_lon = x / (R * cos(lat_rad))

    # Koordinaten berechnen
    new_lat = lat_rad + d_lat
    new_lon = lon_rad + d_lon

    # zurück zu degree umwandeln
    drlat = degrees(new_lat)
    drlon = degrees(new_lon)

    return (drlat, drlon)

def main(args=None):

    # globale Sensordaten Variablen
    global dvlDataString
    global gpsDataString

    # Positionsvariable
    newPosition = (50.0, 20.0)

    # Zählervariable für die Koppelnavigation
    koppel = 0

    # Initialisieren von rclpy und erstellen des Nodes
    rclpy.init(args=args)
    subNode = rclpy.create_node('subscriber')

    # Abonieren der DVL Daten
    sub1 = subNode.create_subscription(String, 'dvl_data', dvl_callback, 10)
    # Abonieren der GPS Daten
    sub2 = subNode.create_subscription(String, 'gps_data', gps_callback, 10)

    while True:
        # Abrufen der Sensordaten
        rclpy.spin_once(subNode)
        print('DVL' + dvlDataString)
        print('GPS' + gpsDataString)
        
        # Aufspalten der Sensordaten Strings
        gps_data = gpsDataString.split()
        dvl_data = dvlDataString.split()

        # zwischenvariable für die aktuelle Position
        currentPosition = newPosition

        # Ist das GPS Verfügbar?
        # Wenn Kein GPS Signal da ist wird Koppelnavigation gestartet
        if gps_data[0] == "timeout":
            #print('Koppelbereich')

            # Variable zum Erfassen der Zeit wie lange die Koppelnavigation bisher geht
            koppel += 1

            # eigene Richtungskoppelnavigation            
            newPosition = getDestination(newPosition[0], newPosition[1], 90, 20, 1)

            # DVL Koppelnavigation
            #print(currentPosition[0], currentPosition[1])

            # Werden DVL-Daten empfangen?
            if not dvl_data[0] == "DVL":
                #print(dvl_data[1])
                #print(dvl_data[3])

                # Übersetzen der DVL Abweichung von Refernzkoordinate zu aktueller Koordinate
                print(currentPosition[0], currentPosition[1], dvl_data[1], dvl_data[3])
                newDVLPosition = getTransPosition(currentPosition[0], currentPosition[1], float(dvl_data[1]), float(dvl_data[3]))
                print('DVL Position: ')
                print(newDVLPosition)
                print("Kein GPS Signal")
                oldPosition = newPosition
            else:
                print("Das DVL sendet nicht")
                print(dvl_data)
        else:
            if len(gps_data) >= 4:
                print(gps_data)
                # lat und lon aus der gps_data liste extarhieren
                lat1 = float(gps_data[2])
                lon1 = float(gps_data[3])
                # aktualisieren der newPosition mit den aktuellen Koordinaten
                newPosition = (lat1, lon1)
                if koppel:
                    distance = getDistance(oldPosition[0], oldPosition[1], newPosition[0], newPosition[1]) 
                    dvl_distance = getDistance(newDVLPosition[0], newDVLPosition[1], newPosition[0], newPosition[1])
                    print("Abweichung DVL Koppelnavigation zum realen GPS nach "+ str(koppel) + "sek: " + str(dvl_distance) + "m" )
                    print("Abweichung eigene Koppelnavigation zum realen GPS nach "+ str(koppel) + "sek: " + str(distance) + "m" )
                    koppel = 0    

    # Clean up
    subNode.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
