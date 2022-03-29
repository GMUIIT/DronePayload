# Micropython script
import machine
import micropython
from machine import UART, Pin
import time


# SBUS uses an inverted serial port
ser = UART(0, baudrate=100000, tx=Pin(0), rx=Pin(1), invert=UART.INV_TX | UART.INV_RX, parity=0, stop=2)
channels = [0] * 16
n = 0

def write_sbus_frame(_=None):
    global channels, n
    """
    Write a SBUS frame to the serial port.
    """
    # SBUS frame format:
    # 0: header byte, 0x0F
    # 1-22: 16 servo channels, 11 bits each
    # 23:
    #   bit 7: digital channel 17
    #   bit 6: digital channel 18
    #   bit 5: frame lost
    #   bit 4: failsafe activated
    #   bit 3-0: unused
    # 24: end byte, 0x00
    n += 1
    ser.write(b'\x0F')
    channels_int = 0
    for i, channel in enumerate(channels):
        channel &= 0x7FF
        channels_int |= channel << (11 * i)
    ser.write(channels_int.to_bytes(4, 'big'))
    ser.write(b'\x00')
    ser.write(b'\x00')


def main():
    global channels
    timer = machine.Timer(period=9, mode=machine.Timer.PERIODIC, callback=lambda x: micropython.schedule(write_sbus_frame, 0))

    while True:
        # read input from stdin
        line = input()
        # split input into channels
        try:
            inputs = [int(x.strip()) for x in line.strip().split(',')]
        except ValueError as e:
            print("Error parsing input", e)
            continue
        if len(inputs) >= 16:
            print("Too many channels")
            continue
        elif len(inputs) < 16:
            inputs += [0] * (16 - len(inputs))
        # set channels
        channels = inputs
        # write frame
        write_sbus_frame()
        print(n, "frames sent")


if __name__ == '__main__':
    main()
