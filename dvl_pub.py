import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import socket

class DvlPublisherNode(Node):
    def __init__(self):
        super().__init__('dvl_publisher')
        self.publisher_ = self.create_publisher(String, 'dvl_data', 10)
        self.timer_ = self.create_timer(0.1, self.timer_callback)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', 16171))

    def timer_callback(self):
        data = self.sock.recv(1024)
        json_data = json.loads(data)
        msg = String()
        msg.data = json.dumps(json_data)
        self.publisher_.publish(msg)
        self.get_logger().info('Published: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    dvl_publisher = DvlPublisherNode()
    rclpy.spin(dvl_publisher)
    dvl_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
