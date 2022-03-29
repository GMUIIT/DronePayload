import pygame
import argparse
import time
import serial

# Map sbus channels to joystick axes
SBUS_CHANNELS = [
        {'joystick_axis': 5, 'channel': 0, 'min': -1.0, 'max': 1.0},  # Throttle
        {'joystick_axis': 0, 'channel': 1, 'min': -1.0, 'max': 1.0, 'dead_zone': 0.1},  # L/R
        {'joystick_axis': 1, 'channel': 2, 'min': -1.0, 'max': 1.0, 'dead_zone': 0.07},  # F/B
        {'joystick_axis': 3, 'channel': 3, 'min': -1.0, 'max': 1.0, 'dead_zone': 0.07},  # Yaw
        # joystick axis 4 (right stick up/down) is drifing and shouldn't be used
]


def main():
    parser = argparse.ArgumentParser(description='Companion program to write joystick data to the serial port')
    parser.add_argument('--port', '-p', default='/dev/ttyACM0', help='Serial port to use')
    parser.add_argument('--baud', '-b', default=115200, type=int, help='Baud rate to use')
    parser.add_argument('--joystick', '-j', default=0, type=int, help='Joystick to use')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    # Initialize the joysticks and pygame
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(args.joystick)
    joystick.init()

    # Initialize serial port
    ser = serial.Serial(args.port, args.baud)

    while True:
        # Process events
        if pygame.event.get():
            # Send data to the serial port
            # channel_outputs = [0] * 16
            # This is illegal but it's fine as a hack rn
            channel_outputs = [0] * 4
            for channel in SBUS_CHANNELS:
                axis = joystick.get_axis(channel['joystick_axis'])
                if 'dead_zone' in channel and abs(axis) < channel['dead_zone']:
                    # anything in the dead zone just gets set to 0
                    axis = 0
                axis = (axis - channel['min']) / (channel['max'] - channel['min'])
                axis = int(axis * (2 ** 11 - 1))
                channel_outputs[channel['channel']] = axis
            if args.debug:
                print("Sending: {}".format(channel_outputs))
            ser.write(str(channel_outputs).replace('[', '').replace(']', '').encode())
            ser.write(b'\n')
            if args.debug:
                print("Sent")
            if args.debug and ser.in_waiting > 0:
                print("Received: {}".format(ser.read(ser.in_waiting).decode()))
        time.sleep(0.003)

    pygame.quit()


if __name__ == "__main__":
    main()
