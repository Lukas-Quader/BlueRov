import rclpy
import socket
import json
from rclpy.node import Node
from std_msgs.msg import String # Übertragung der Daten im Format String




def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('dvl_pub')
    dvl_pub = node.create_publisher(String, 'dvl_data', 10)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind and listen
    serverSocket.bind(('192.168.194.95', 16171))
    serverSocket.listen()
    (clientConnected, clientAddress) = serverSocket.accept()
    msg = String()

    while True:     
        dataFromClient = clientConnected.recv(2048)
                        
        try:            
            decoder = json.JSONDecoder()
            if dataFromClient:
                decode_data = decoder.raw_decode(dataFromClient.decode())
                if 'ts' in decode_data[0]:                    
                    msg.data = "x: " + str(decode_data[0]["x"]) +" y: " + str(decode_data[0]["y"]) + " z: " + str(decode_data[0]["z"])
                    dvl_pub.publish(msg)
        except json.JSONDecodeError as e:
            print("FAILED" + dataFromClient.decode())
            continue

if __name__ == '__main__':
    main()
