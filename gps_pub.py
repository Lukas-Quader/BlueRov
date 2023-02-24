import rclpy
import serial
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'gps_data_topic', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        ser = serial.Serial()
        ser.baudrate = 57600
        ser.port = '/dev/serial/by-id/usb-Emlid_ReachM2_8243BC05A02E4C66-if02'
        ser.timeout = 1
        ser.open()
        ser.flushInput() # flushen um veraltete Daten zu löschen

        msg = String()
        msg.data = ser.readline().decode('utf-8').strip()
        if not msg.data:
            msg.data = 'timeout'
        self.publisher_.publish(msg)
        self.get_logger().info(msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
