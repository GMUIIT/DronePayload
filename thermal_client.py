import cv2
import socket
import numpy as np
import argparse
import base64


def main():
    parser = argparse.ArgumentParser(description='Thermal Camera Client')
    parser.add_argument('ip_address', type=str,
            help='ip address to connect to')
    parser.add_argument('--port', type=int, default=1729,
            help='socket port to connect to')
    args = parser.parse_args()
    
    client = socket.create_connection((args.ip_address, args.port))

    with client:
        while True:
            line = b''
            while not line.endswith(b'\n'):
                line += client.recv(1)
            line = line[:-1]

            try:
                line = base64.b85decode(line)
                img = cv2.imdecode(np.frombuffer(line, dtype=np.uint8), cv2.IMREAD_COLOR)
            except ValueError:
                print(f'Invalid image received: {line}')
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
