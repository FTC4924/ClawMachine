# ClawMachine
![Pandas playing Claw Machine](https://github.com/user-attachments/assets/33424587-ca2d-4be4-841d-025a88052999)
We use a DexArm 3-axis arm with a joystick (binary switches in 4 directions plus a center "fire" button), and an additional switch to detect a coin inserted.

The program allows the arm to initialize when a coin is inserted.  The player then has 30 seconds to move the arm in a constrained space and try to position over some target object.
When the player hits the "fire" button, the arm lowers ~3cm and engages the suction pump to try to pick up an object.  Whether it connects with an object or not, the arm then moves to the prize shoot, releases the vacuum suction holding the prize, pauses, then returns to the home position to await the next player (coin activation).

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

Libraries needed for Raspberry Pi version: <br>
pydexarm.py  (locate in same directory as ClawGrabber.py) <br>
install pip library with: sudo apt install python3-pip <br>
install serial library with: sudo pip3 install pyserial <br>
make executable with: chmod +x ClawGrabber.py <br>
