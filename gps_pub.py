import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import String # Übertragung der Daten im Format String




def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('gps_pub')
    gps_pub = node.create_publisher(String, 'gps_data', 10)
    #node = rclpy.create_node('gps_pub2')
    gps_pub2 = node.create_publisher(String, 'gps_data2', 10)
    

    ser = serial.Serial()
    ser.baudrate = 57600
    ser.port = '/dev/serial/by-id/usb-Emlid_ReachM2_8243BC05A02E4C66-if02'
    msg = String()
    ser.open()
    ser.flushInput() # flushen um veraltete Daten zu löschen

    while True:        
        msg.data = ser.readline().decode('utf-8').strip()
        if not msg.data:
            msg.data = 'timeout'
        gps_pub.publish(msg)
        print('sende:' + msg.data)
        #gps_pub.get_logger().info(msg.data)
        #rclpy.spin_once(gps_pub) 
        #rclpy.shutdown()

    

if __name__ == '__main__':
    main()
