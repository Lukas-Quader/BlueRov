import rclpy
import time
from numpy import sin, cos, arccos, pi, round
from math import sin, cos, atan2, sqrt, radians, asin, degrees
from rclpy.node import Node
from std_msgs.msg import String # Übertragene Daten im Format String

gps_str = "Hallo Welt"

# Übertragung des GPS Strings vom GPS_pub
class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'gps_data_topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        global gps_str
        gps_str = str(msg.data)
        #self.get_logger().info('I heard: "%s"' % msg.data)


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
    

def main(args=None):

    global gps_str # globale Variable GPS_String. Beinhaltet die übertragene Nachricht vom GPS_pub
    newPosition = (50.0,10.0)  # aktuelle Position als Tuple (latitude, longitude)
    
    # koppel: Variable zeichnet auf wie lange das System im Koppelnavigationsmodus ist. 0 = keine Koppelnavigation
    koppel = 0 
    while True:
        rclpy.init(args=args)
        minimal_subscriber = MinimalSubscriber() 
        time.sleep(1)
        rclpy.spin_once(minimal_subscriber, executor=None, timeout_sec=0)
        minimal_subscriber.destroy_node()
        rclpy.shutdown()
        gps_data = gps_str.split() # aufteilen des übertragten Strings
        # ist ein GPS-Signal verfügbar
        if gps_data[0] == "timeout":
            koppel += 1
            # Eingabe der Sensorwerte (latitude, longitude, Richtung, km/h, sekunden)
            newPosition = getDestination(newPosition[0], newPosition[1], 90, 20, 1)
            print("No Signal")
            oldPosition = newPosition
        else:
            
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
