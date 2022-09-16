import adafruit_gps
import adafruit_mlx90640
import board
import busio
import serial
import sys
import time
import RPi.GPIO as GPIO
import io

#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#

FIRE_TEMPERATURE_THRESHOLD = 36
FIRE_PIXELS_THRESHOLD = 10

#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#

# Universal GPS setup
def init_gps():
    try:
        # Create a serial connection for the GPS connection using default speed and
        # a slightly higher timeout (GPS modules typically update once a second).
        # These are the defaults you should use for the GPS FeatherWing.
        # For other boards set RX = GPS module TX, and TX = GPS module RX pins.
        print("opening serial")
        uart = serial.Serial(port="/dev/serial0", baudrate=9600, timeout=10)

        # Create a GPS module instance.
        print("creating instance")
        gps = adafruit_gps.GPS(uart, debug=False)

        # Turn on the basic GGA and RMC info (what you typically want)
        print("settin default")
        gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

        # Set update rate to once a second (1hz) which is what you typically want.
        print("set update rate")
        gps.send_command(b"PMTK220,1000")

        return gps
    except:
        sys.exit("GPS initialization failed.")

#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#

# Thermal Camera Setup
def init_thermal():
    try:
        i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
        mlx = adafruit_mlx90640.MLX90640(i2c)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ
        return mlx
    except:
        sys.exit("Thermal camera initialization failed.")

# Simple algorithm to detect fire
def frame_has_fire(frame):
    fire_pixels = 0
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            if t > FIRE_TEMPERATURE_THRESHOLD:
                fire_pixels += 1
    
    return fire_pixels > FIRE_PIXELS_THRESHOLD

#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#

# Serial setup
def init_serial():
    ser = serial.Serial(
        port='/dev/ttyAMA2',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1            
    )
    return ser

# Prints to the transmitter
def sprint(ser, *args, **kwargs):
    # temporary print function
    print(*args, **kwargs)
    # sio = io.StringIO()
    # print(*args, **kwargs, file=sio)
    # ser.write(str.encode(sio.getvalue()))

#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------#

def main():
    print("program started!")
    gps = init_gps()
    mlx = init_thermal()
    ser = init_serial()
    frame = [0] * 768

    while True: 
        sprint(ser, "ping")

        gps.update()

        try:
            mlx.getFrame(frame)
        except ValueError:
            # these happen, no biggie - retry
            continue

        fix = gps.has_fix
        fire = frame_has_fire(frame)

        # If there is a fire, report it even if there is no GPS fix
        if fire:
            sprint(ser, "Fire detected!")
            if fix:
                sprint(ser, "GPS fix: ", gps.latitude, gps.longitude)
            else:
                sprint(ser, "No GPS fix.")



if __name__ == "__main__":
    main()
