import serial
import time


def main(args=None):
    ser = serial.Serial()
    ser.baudrate = 57600
    ser.port = '/dev/serial/by-id/usb-Emlid_ReachM2_8243BC05A02E4C66-if02'
    ser.open()
    ser.flushInput()
    while True:
        print(ser.readline())
        time.sleep(1)


if __name__ == '__main__':
    main()
