import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import socket
import time

class DvlPublisherNode(Node):
    def __init__(self):
        super().__init__('dvl_publisher')
        self.publisher_ = self.create_publisher(String, 'dvl_data', 10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('192.168.194.95', 16171))

    def timer_callback(self):
        
       
        data = self.sock.recv(2048)
        decoder = json.JSONDecoder()
        try:
            if data:

                decode_data = decoder.raw_decode(data.decode())[0]
                time.sleep(1)
                print(decode_data)
                #if 2 < 1:
                if type(decode_data) is tuple:

                    if 'ts' in decode_data:
                        msg = String()
                        msg.data = "DVL," + str(decode_data["x"]) + "," + str(decode_data["y"]) + "," + str(decode_data["z"])
                        self.publisher_.publish(msg)
                        self.get_logger().info('Published: "%s"' % msg.data)

        except json.JSONDecodeError as e:
            self.get_logger().info("JSONDecodeError")

    
        

def main(args=None):
    rclpy.init(args=args)
    dvl_publisher = DvlPublisherNode()
    rclpy.spin(dvl_publisher)
    dvl_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
