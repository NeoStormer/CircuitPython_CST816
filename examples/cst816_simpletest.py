# SPDX-FileCopyrightText: Copyright (c) 2023 NeoStormer
#
# SPDX-License-Identifier: MIT

import time
import board
import busio
import cst816

# Initialize I2C
i2c = busio.I2C(board.GP7, board.GP6)
touch = cst816.CST816(i2c)

# Check if the touch controller is detected
if touch.who_am_i():
    print("CST816 detected.")
else:
    print("CST816 not detected.")

# Read touch data continuously
while True:
    point = touch.get_point()
    gesture = touch.get_gesture()
    press = touch.get_touch()
    distance = touch.get_distance()
    print(
        "Position: {0},{1} - Gesture: {2} - Pressed? {3} - Distance: {4},{5}".format(
            point.x_point,
            point.y_point,
            gesture,
            press,
            distance.x_dist,
            distance.y_dist,
        )
    )
    time.sleep(0.05)
