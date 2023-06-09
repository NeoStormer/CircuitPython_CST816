Introduction
============

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/NeoStormer/CircuitPython_CST816/workflows/Build%20CI/badge.svg
    :target: https://github.com/NeoStormer/CircuitPython_CST816/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython driver for the CST816 capacitive touch screen IC

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Usage Example
=============

.. code-block:: python

    import time
    import board
    import busio
    import cst816

    # Initialize I2C
    i2c = busio.I2C(board.GP7,board.GP6)
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
        print("Position: {0},{1} - Gesture: {2} - Pressed? {3} - Distance: {4},{5}".format(point.x_point, point.y_point, gesture, press, distance.x_dist, distance.y_dist))
        time.sleep(0.05)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/NeoStormer/CircuitPython_CST816/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
