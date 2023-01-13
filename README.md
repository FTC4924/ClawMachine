# ClawMachine
Notes on configuring Claw Machine for running on a Raspberry Pi 3 board
Build a Pi 3 with full visual editor and wifi connection 
In addition to the build, from the command line/window, install pyjoystick by entering:
pip install pyjoystick   (wait a bit, it goes out and downloads 2MB of stuff, 3 progress bars)

In test.py, the connection string is dexarm = Dexarm(port="/dev/ttyACM1")

By way of troubleshooting, when the rotrics/Dexarm is plugged into a usb port, you can
type lsusb and see a devise called STMicroelectronics.  Turn the arm off, that device goes away.
