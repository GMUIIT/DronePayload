# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_mlx90640
import serial
import adafruit_gps

#--------------------------------------------------------------------------

# Universal GPS setup

# Create a serial connection for the GPS connection using default speed and
# a slightly higher timeout (GPS modules typically update once a second).
# These are the defaults you should use for the GPS FeatherWing.
# For other boards set RX = GPS module TX, and TX = GPS module RX pins.
uart = serial.Serial("/dev/ttyAMA1", baudrate=9600, timeout=10)

# Create a GPS module instance.
gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command(b"PMTK220,1000")

#-------------------------------------------------------------------------

# Thermal Camera Setup
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C")
print([hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_4_HZ
frame = [0] * 768

#--------------------------------------------------------------------------

# DEBUG variable. 0 removes any unnecessary print statements. 
DEBUG = 1

#--------------------------------------------------------------------------

# Driver code.

while True:
    stamp = time.monotonic()
    try:
        mlx.getFrame(frame)
    except ValueError:
        # these happen, no biggie - retry
        continue
    if DEBUG == 1:    
        print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
    for h in range(24):
        for w in range(32):
            t = frame[h * 32 + w]
            cnt = 0
            for t in frame:
                #if temperature is above the number, add to the count of pixels on fire.
                if t > 200:
                    # Solely a debug map. This should point out hot areas. (untested)
                    if DEBUG == 1:
                        # pylint: disable=multiple-statements
                        print("#")
                        # pylint: enable=multiple-statements
                    cnt = cnt + 1
                else:
                    # Solely a debug map. This should point out "cold" areas. (untested)
                    if DEBUG == 1:
                        # pylint: disable=multiple-statements
                        print(" ")
                        # pylint: enable=multiple-statements
            # If there are more than enough pixels on fire, 
            # relay the location of the drone and reset the count of pixels.
            if cnt > 15:
                        print("=" * 40)  # Print a separator line.
                        # Print out the current location.
                        print("Latitude: {0:.6f} degrees".format(gps.latitude))
                        print("Longitude: {0:.6f} degrees".format(gps.longitude))
                        print("Fix quality: {}".format(gps.fix_quality))
                        # Resets the amount of pixels counted.
                        cnt = 0                   

        print()
    print()
