import rclpy
#import flags.py
import socket
import json
import time
from rclpy.node import Node
from std_msgs.msg import String # Übertragung der Daten im Format String

MSG_COUNT = False
MSG_XYZ = False
MSG_RAW_TS = False
MSG_RAW = True


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('dvl_pub')
    dvl_pub = node.create_publisher(String, 'dvl_data', 10)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind and listen
    
    serverSocket.connect(("192.168.194.95", 16171))
    
    msg = String()
    counter = 0

    while True:     
        dataFromClient = serverSocket.recv(2048)
        #print(flags.test)
        try:            
            decoder = json.JSONDecoder()
            if dataFromClient:
                decode_data = decoder.raw_decode(dataFromClient.decode())
                if MSG_RAW: 
                    msg.data = str(decode_data)
                    dvl_pub.publish(msg)
                    print(msg)
                elif 'ts' in decode_data[0]:                    
                    counter += 1
                    if MSG_XYZ:
                        msg.data = "x: " + str(decode_data[0]["x"]) +" y: " + str(decode_data[0]["y"]) + " z: " + str(decode_data[0]["z"]) 
                    if MSG_COUNT:
                        msg.data += ' Counter: ' + str(counter) 
                    if MSG_RAW_TS:
                        msg.data = str(decode_data)
                    dvl_pub.publish(msg)
                    print(msg)
                    #time.sleep(1)
            else: 
                msg.data = 'dvl_timeout'
                dvl_pub.publish(msg)
                print('sendet:' + msg)
        except json.JSONDecodeError as e:
            print("FAILED" + dataFromClient.decode())
            continue
        
if __name__ == '__main__':
    main()
