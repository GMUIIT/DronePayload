#!/usr/bin/env python3
import serial


def main():
    try:
        ser = serial.Serial("/dev/serial0", 9600)

        # actual code
    finally:
        # IMPORTANT!
        ser.close()

if __name__ == '__main__':
    main()
