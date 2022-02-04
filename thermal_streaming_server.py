# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
import busio
import adafruit_mlx90640
import cv2
import serial
import base64
import numpy as np


def main():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

    mlx = adafruit_mlx90640.MLX90640(i2c)
    print("MLX addr detected on I2C")
    print([hex(i) for i in mlx.serial_number])

    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_32_HZ
    with serial.Serial('/dev/serial0', 115200) as ser:
        while True:
            stamp = time.monotonic()
            frame = [0] * 768
            try:
                mlx.getFrame(frame)
            except ValueError:
                # these happen, no biggie - retry
                continue
            print("Read 2 frames in %0.2f s" % (time.monotonic() - stamp))
            mat = np.zeros((24, 32), dtype=np.float32)
            low, high = min(frame), max(frame)
            for h in range(24):
                for w in range(32):
                    t = frame[h * 32 + w]
                    mat[h,w] = (t - low) / (high - low) * 255

            res, enc = cv2.imencode('.jpg', mat)
            enc = base64.b85encode(enc.tobytes())  # ready to be sent via XBee
            print(f'Sending {len(enc) + 1} bytes via serial.')
            ser.write(enc)
            ser.write(b'\n')

if __name__ == '__main__':
    main()
