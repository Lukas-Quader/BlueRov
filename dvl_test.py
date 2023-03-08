import socket

def main(args=None):
    sensor_ip = '192.168.178.52'
    sensor_port = 9002

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sensor_ip, sensor_port))

    while True: 
        data = sock.recv(1024)
        print(data)


if __name__ == '__main__':
    main()
