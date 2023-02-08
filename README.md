# ClawMachine
Notes on configuring Claw Machine for running on a Raspberry Pi 3 board
Build a Pi 3 with full visual editor and wifi connection 

If we wind up using pyjoystick (maybe?)
In addition to the build, from the command line/window, install pyjoystick by entering:
pip install pyjoystick   (wait a bit, it goes out and downloads 2MB of stuff, 3 progress bars)

In test.py, the connection string is dexarm = Dexarm(port="/dev/ttyACM1") or ACM0 - depends on where plugged in.

By way of troubleshooting, when the rotrics/Dexarm is plugged into a usb port, you can
type lsusb and see a device called STMicroelectronics.  Turn the arm off, that device goes away.

Clawgrabber.py worked 1/19/23 with the following GPIO inputs: 
Left, Right, Up, Down, Grabber, and Coin

Use crontab to build an auto-run script. 
See https://www.dexterindustries.com/howto/auto-run-python-programs-on-the-raspberry-pi/

Libraries needed for Raspberry Pi version:
pydexarm.py  (locate in same directory as ClawGrabber.py)
install pip library with: sudo apt install python3-piop
install serial library with: sudo pip3 install pyserial
make executable with: chmod +x ClawGrabber.py
