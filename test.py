import math
import msvcrt
import sys
import time

import pyjoystick
from pyjoystick.sdl2 import Key, Joystick, run_event_loop

from pydexarm import Dexarm

COLLECTION_HEIGHT = -50
DROP_POSITION = 0, 350, 0

if sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  # Load the arm on Windows
    dexarm = Dexarm("COM8")
else:  # Load the arm on Mac or Linux
    dexarm = Dexarm("/dev/tty.usbmodem3086337A34381")

dexarm.go_home()

x, y, z, *_ = dexarm.get_current_position()
speed = 2

angle, magnitude = math.degrees(math.atan2(y, x)) - 90, math.hypot(x, y)
magnitudeMin = 210
magnitudeMax = 405
angleMin = -90
angleMax = 90

del x
del y


def getX() -> float:
    return magnitude * math.sin(math.radians(-angle))


def getY() -> float:
    return magnitude * math.cos(math.radians(angle))


def z_plus():
    global z
    z += speed


def z_minus():
    global z
    z -= speed


"""def handle_key_event(key):
    print(key, '-', key.keytype, '-', key.number, '-', key.value)

    if key.keytype != Key.HAT:
        return

    if key.value == Key.HAT_UP:
        y_plus()
    elif key.value == Key.HAT_DOWN:
        y_minus()
    if key.value == Key.HAT_LEFT:
        x_minus()
    elif key.value == Key.HAT_UPLEFT:
        x_minus()
        x_plus()
    elif key.value == Key.HAT_DOWNLEFT:
        x_minus()
        y_minus()
    elif key.value == Key.HAT_RIGHT:
        x_plus()
    elif key.value == Key.HAT_UPRIGHT:
        x_plus()
        y_plus()
    elif key.value == Key.HAT_DOWNRIGHT:
        x_plus()
        y_minus()
    dexarm.move_to(x, y, z)
"""

# z = COLLECTION_HEIGHT

while True:
    key: bytes = msvcrt.getch()
    #angle, magnitude = math.degrees(math.atan2(y, x)) - 90, math.hypot(x, y)
    print("Angle:", angle, "Magnitude:", magnitude)
    if key == b"q":
        break

    if key == b"w":
        if magnitudeMax >= magnitude + speed:
            magnitude += speed
        else:
            print("Max Magnitude")
    elif key == b"s":
        if magnitude - speed >= magnitudeMin:
            magnitude -= speed
        else:
            print("Min Magnitude")
    elif key == b"a":
        if angleMax >= angle + speed:
            angle += speed
        else:
            print("Max Angle")
    elif key == b"d":
        if angle - speed >= angleMin:
            angle -= speed
        else:
            print("Min Angle")
    elif key == b"e":
        z_minus()
        dexarm.move_to(getX(), getY(), COLLECTION_HEIGHT)
        dexarm.air_picker_pick()
        dexarm.move_to(getX(), getY(), z)
        dexarm.move_to(*DROP_POSITION)
        dexarm.air_picker_place()
        time.sleep(1)
        dexarm.air_picker_stop()
    else:
        dexarm.go_home()
        x, y, z, *_ = dexarm.get_current_position()
        angle, magnitude = math.degrees(math.atan2(y, x)) - 90, math.hypot(x, y)

    dexarm.move_to(getX(), getY(), z)

    print(dexarm.get_current_position())
    print(getX(), getY(), z)

    """repeater = pyjoystick.HatRepeater(first_repeat_timeout=0.5, repeat_timeout=0.03, check_timeout=0.01)

    mngr = pyjoystick.ThreadEventManager(event_loop=run_event_loop,
                                         handle_key_event=handle_key_event,
                                         button_repeater=repeater)
    mngr.start()"""
