# SPDX-FileCopyrightText: Copyright (c) 2023 NeoStormer
#
# SPDX-License-Identifier: MIT
"""
`cst816`
================================================================================

CircuitPython driver for the CST816 capacitive touch screen IC


* Author(s): NeoStormer

Implementation Notes
--------------------

**Hardware:**

* `CST816 High Performance Self-Capacitance Touchchip
  <https://www.buydisplay.com/download/ic/DS-CST816S_DS_V1.3.pdf>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

import time
from micropython import const
from adafruit_bus_device import i2c_device

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/NeoStormer/CircuitPython_CST816.git"

# I2C ADDRESS
_CST816_ADDR = const(0x15)

# Register Addresses
_CST816_GestureID = const(0x01)
_CST816_FingerNum = const(0x02)
_CST816_XposH = const(0x03)
_CST816_XposL = const(0x04)
_CST816_YposH = const(0x05)
_CST816_YposL = const(0x06)

_CST816_ChipID = const(0xA7)
_CST816_ProjID = const(0xA8)
_CST816_FwVersion = const(0xA9)
_CST816_MotionMask = const(0xAA)

_CST816_BPC0H = const(0xB0)
_CST816_BPC0L = const(0xB1)
_CST816_BPC1H = const(0xB2)
_CST816_BPC1L = const(0xB3)

_CST816_IrqPluseWidth = const(0xED)
_CST816_NorScanPer = const(0xEE)
_CST816_MotionSlAngle = const(0xEF)
_CST816_LpScanRaw1H = const(0xF0)
_CST816_LpScanRaw1L = const(0xF1)
_CST816_LpScanRaw2H = const(0xF2)
_CST816_LpScanRaw2L = const(0xF3)
_CST816_LpAutoWakeTime = const(0xF4)
_CST816_LpScanTH = const(0xF5)
_CST816_LpScanWin = const(0xF6)
_CST816_LpScanFreq = const(0xF7)
_CST816_LpScanIdac = const(0xF8)
_CST816_AutoSleepTime = const(0xF9)
_CST816_IrqCtl = const(0xFA)
_CST816_AutoReset = const(0xFB)
_CST816_LongPressTime = const(0xFC)
_CST816_IOCtl = const(0xFD)
_CST816_DisAutoSleep = const(0xFE)

# Modes
_CST816_Point_Mode = const(1)
_CST816_Gesture_Mode = const(2)
_CST816_ALL_Mode = const(3)

# Gestures
_CST816_Gesture_None = const(0)
_CST816_Gesture_Up = const(1)
_CST816_Gesture_Down = const(2)
_CST816_Gesture_Left = const(3)
_CST816_Gesture_Right = const(4)
_CST816_Gesture_Click = const(5)
_CST816_Gesture_Double_Click = const(11)
_CST816_Gesture_Long_Press = const(12)


class CST816:
    """Driver for the CST816 Touchscreen connected over I2C."""

    def __init__(self, i2c):
        self.i2c_device = i2c_device.I2CDevice(i2c, _CST816_ADDR)
        self.prev_x = 0
        self.prev_y = 0
        self.prev_touch = False
        self.x_point = 0
        self.y_point = 0
        self.x_dist = 0
        self.y_dist = 0
        self.mode = 0

    def _i2c_write(self, reg, value):
        """Write to I2C"""
        with self.i2c_device as i2c:
            i2c.write(bytes([reg, value]))

    def _i2c_read(self, reg):
        """Read from I2C"""
        with self.i2c_device as i2c:
            data = bytearray(1)
            i2c.write_then_readinto(bytes([reg]), data)
            return data[0]

    def who_am_i(self):
        """Check the Chip ID"""
        return bool(self._i2c_read(_CST816_ChipID) == 0xB5)

    def reset(self):
        """Make the Chip Reset"""
        self._i2c_write(_CST816_DisAutoSleep, 0x00)
        time.sleep(0.1)
        self._i2c_write(_CST816_DisAutoSleep, 0x01)
        time.sleep(0.1)

    def read_revision(self):
        """Read Firmware Version"""
        return self._i2c_read(_CST816_FwVersion)

    def wake_up(self):
        """Make the Chip Wake Up"""
        self._i2c_write(_CST816_DisAutoSleep, 0x00)
        time.sleep(0.01)
        self._i2c_write(_CST816_DisAutoSleep, 0x01)
        time.sleep(0.05)
        self._i2c_write(_CST816_DisAutoSleep, 0x01)

    def stop_sleep(self):
        """Make the Chip Stop Sleeping"""
        self._i2c_write(_CST816_DisAutoSleep, 0x01)

    def set_mode(self, mode):
        """Set the Behaviour Mode"""
        if mode == _CST816_Point_Mode:
            self._i2c_write(_CST816_IrqCtl, 0x41)
        elif mode == _CST816_Gesture_Mode:
            self._i2c_write(_CST816_IrqCtl, 0x11)
            self._i2c_write(_CST816_MotionMask, 0x01)
        else:
            self._i2c_write(_CST816_IrqCtl, 0x71)
        self.mode = mode

    def get_point(self):
        """Get the Pointer Position"""
        x_point_h = self._i2c_read(_CST816_XposH)
        x_point_l = self._i2c_read(_CST816_XposL)
        y_point_h = self._i2c_read(_CST816_YposH)
        y_point_l = self._i2c_read(_CST816_YposL)
        self.x_point = ((x_point_h & 0x0F) << 8) + x_point_l
        self.y_point = ((y_point_h & 0x0F) << 8) + y_point_l
        return self

    def get_gesture(self):
        """Get the Gesture made by the User"""
        gesture = self._i2c_read(_CST816_GestureID)
        return gesture

    def get_touch(self):
        """Detect User Presence, are they touching the screen?"""
        finger_num = self._i2c_read(_CST816_FingerNum)
        return finger_num > 0

    def get_distance(self):
        """Get the Distance made Between Readings, only while touched"""
        touch_data = self.get_point()
        x = touch_data.x_point
        y = touch_data.y_point
        if self.prev_touch is False and self.get_touch() is True:
            self.x_dist = 0
            self.y_dist = 0
        else:
            self.x_dist = x - self.prev_x
            self.y_dist = y - self.prev_y
        self.prev_touch = self.get_touch()
        self.prev_x = x
        self.prev_y = y
        return self
