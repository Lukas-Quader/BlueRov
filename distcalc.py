import rclpy
import time
from numpy import sin, cos, arccos, pi, round
from math import sin, cos, atan2, sqrt, radians, asin, degrees
from rclpy.node import Node
from std_msgs.msg import String # Übertragene Daten im Format String

gps_str = "Hallo Welt"
dvl_str = []

# Übertragung des GPS Strings vom GPS_pub

'''
class MinimalSubscriber(Node):

    def __init__(self, topic):
        super().__init__('minimal_subscriber')
        if topic == 'gps_data':
            self.subscription_gps = self.create_subscription(
                String,
                topic,
                self.listener_callback_gps,
                10)
            self.subscription_gps  # prevent unused variable warning
        else: 
            self.subscription_dvl = self.create_subscription(
                String,
                topic,
                self.listener_callback_dvl,
                10)
            self.subscription_dvl # prevent unused variable warning

    def listener_callback_gps(self, msg):
        global gps_str        
        gps_str = msg.data

    def listener_callback_dvl(self, msg):
        global dvl_str
        dvl_str = msg.data     
'''

def callback_dvl(msg):
    global dvl_str
    dvl_str = msg.data  
    print('DVL Empfangene Nachricht: ' + msg.data)

def callback_gps(msg):
    global gps_str        
    gps_str = msg.data
    print('GPS Empfangene Nachricht: ' + msg.data)

def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians


# Die Funktion gibt die Entfernung zwischen zwei Koordinaten in Meter zurück
# Quelle: https://de.martech.zone/calculate-great-circle-distance/
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
    R = 6370.693  # Erdradius in km (angepasst)(eigentlich 6371)
    
    # umwandeln von Breitengrad und Längengrad in Radiant
    lat1 = radians(latitude)
    lon1 = radians(longitude)
    
    # umwandeln der Richtung in Radiant
    bearing = radians(bearing)
    
    # umwandeln von km/h zu km/s
    speed = speed / 3600
    
    # distanz berechnen
    distance = speed * time
    
    # berechnen der neuen latitude und longitude
    lat2 = asin(sin(lat1) * cos(distance/R) + cos(lat1) * sin(distance/R) * cos(bearing))
    lon2 = lon1 + atan2(sin(bearing) * sin(distance/R) * cos(lat1), cos(distance/R) - sin(lat1) * sin(lat2))
    
    # zurück zu degrees umwandeln
    lat2 = degrees(lat2)
    lon2 = degrees(lon2)
    
    return (lat2, lon2)

def getTransPosition(latitude, longitude, x, y):
    
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
    d_lat = dy / R
    d_lon = dx / (R * cos(lat_rad))

    # Koordinaten berechnen
    new_lat = lat_rad + d_lat
    new_lon = lon_rad + d_lon

    # zurück zu degree umwandeln
    drlat = degrees(new_lat)
    drlon = degrees(new_lon)

    return (drlat, drlon) 

       

def main(args=None):

    global gps_str # globale Variable GPS_String. Beinhaltet die übertragene Nachricht vom GPS_pub
    newPosition = (50.0,10.0)  # aktuelle Position als Tuple (latitude, longitude)
    rclpy.init(args=args)
    # minimal_subscriber = MinimalSubscriber('gps_data') 
    # dvl_subscriber = MinimalSubscriber('dvl_data')
    time.sleep(1)
    node = rclpy.create_node('distcalc')
    dvl_sub = node.create_subscription(String, 'dvl_data', callback_dvl, 10)
    gps_sub = node.create_subscription(String, 'gps_data', callback_gps, 10)
    # koppel: Variable zeichnet auf wie lange das System im Koppelnavigationsmodus ist. 0 = keine Koppelnavigation
    koppel = 0 
    #gps_exec = rclpy.executors.Executor(context = None)
    #gps_exec.add_node(gps_sub)
    
    while True:
        

        
        #gps_sub.destroy_node()
        
        rclpy.spin_once(gps_sub)
        #dvl_sub.destroy_node()

        
        gps_data = gps_str.split() # aufteilen des übertragten Strings
        # ist ein GPS-Signal verfügbar
        if gps_data[0] == "timeout":
            koppel += 1
            # Eingabe der Sensorwerte (latitude, longitude, Richtung, km/h, sekunden)
            newPosition = getDestination(newPosition[0], newPosition[1], 90, 20, 1)
            print("No Signal")
            oldPosition = newPosition
        else:
            # ist die länge des Strings größer als 
            if len(gps_data) >= 4:
                # lat und lon
                lat1 = float(gps_data[2])
                lon1 = float(gps_data[3])
                newPosition = (lat1, lon1)
                # Gab es vorher eine Koppelnavigation
                if koppel:
                    # Ermitteln der Distanz zwischen dem Letzten Koppelnav. punkt und des ersten GPS-Punkts(Abweichung)
                    distance = getDistance(oldPosition[0], oldPosition[1], newPosition[0], newPosition[1]) 
                    print("Abweichung Koppelnavigation zum realen GPS nach "+ str(koppel) + "sek: " + str(distance) + "m" )
                    koppel = 0                   
        print(newPosition)
         

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
