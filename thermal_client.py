import cv2
import serial
import numpy as np
import argparse
import base64


def main():
    parser = argparse.ArgumentParser(description='Thermal Camera Client')
    parser.add_argument('--port', type=str, default='/dev/ttyUSB0',
                        help='serial port to connect to')
    parser.add_argument('--baud', type=int, default=115200,
                        help='baud rate to connect to')
    args = parser.parse_args()


    with serial.Serial(args.port, args.baud) as ser:
        # Throw out the first line
        ser.readline()
        while True:
            line = ser.readline()[:-1]
            try:
                line = base64.b85decode(line)
                img = cv2.imdecode(np.frombuffer(line, dtype=np.uint8), cv2.IMREAD_COLOR)
            except ValueError:
                print('Invalid image received')
                continue

            if img is None:
                continue

            img = cv2.resize(img, (640, 480))
            cv2.imshow('Thermal Camera', img)
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        

if __name__ == '__main__':
    main()
