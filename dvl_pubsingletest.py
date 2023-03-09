import socket
import json
from std_msgs.msg import String

def main(args=None):
    sensor_ip = '192.168.194.95'
    sensor_port = 16171

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sensor_ip, sensor_port))
    decoder = json.JSONDecoder()

    
        
    data = sock.recv(2048)
    data_str = data.decode("utf-8")
    json_data = decoder.raw_decode(data_str[0:])
    msg = String()
    msg.data = json.dumps(json_data)
    print(json_data["format"])

        

if __name__ == '__main__':
    main()
