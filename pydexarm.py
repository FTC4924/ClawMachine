#import serial
import re
import pyb

class Dexarm:

    def __init__(self, port):
        #self.ser = serial.Serial(port, 115200, timeout=None)
        #self.is_open = self.ser.isOpen()
        self.ser = pyb.USB_VCP()
        self.is_open = self.ser.isconnected()
        if self.is_open:
            print('pydexarm: %s open' % 0)
        else:
            print('Failed to open serial port')

    def _send_cmd(self, data):
        self.ser.write(data.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("ok") > -1:
                    # print("read ok")
                    break
                else:
                    print("read：", str)

    def go_home(self):
        self._send_cmd("M1112\r")

    def set_workorigin(self):
        self._send_cmd("G92 X0 Y0 Z0 E0\r")

    def set_acceleration(self, acceleration, travel_acceleration, retract_acceleration=60):
        cmd = "M204" + "P" + str(acceleration) + "T" + str(travel_acceleration) + "T" + str(
            retract_acceleration) + "\r\n"
        self._send_cmd(cmd)

    def set_module_kind(self, kind):
        self._send_cmd("M888 P" + str(kind) + "\r")

    def get_module_kind(self):
        self.ser.write('M888\r'.encode())
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("PEN") > -1:
                    module_kind = 'PEN'
                if str.find("LASER") > -1:
                    module_kind = 'LASER'
                if str.find("PUMP") > -1:
                    module_kind = 'PUMP'
                if str.find("3D") > -1:
                    module_kind = '3D'
            if len(str) > 0:
                if str.find("ok") > -1:
                    return module_kind

    def move_to(self, x, y, z, feedrate=2000):
        cmd = "G1" + "F" + str(feedrate) + "X" + str(x) + "Y" + str(y) + "Z" + str(z) + "\r\n"
        self._send_cmd(cmd)

    def fast_move_to(self, x, y, z, feedrate=2000):
        cmd = "G0" + "F" + str(feedrate) + "X" + str(x) + "Y" + str(y) + "Z" + str(z) + "\r\n"
        self._send_cmd(cmd)

    """
    :returns x, y, z, e, a, b, c
    """
    def get_current_position(self):
        self.ser.write('M114\r'.encode())
        x, y, z, e, a, b, c = None, None, None, None, None, None, None
        while True:
            str = self.ser.readline().decode("utf-8")
            if len(str) > 0:
                if str.find("X:") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    x = float(temp[0])
                    y = float(temp[1])
                    z = float(temp[2])
                    e = float(temp[3])
            if len(str) > 0:
                if str.find("DEXARM Theta") > -1:
                    temp = re.findall(r"[-+]?\d*\.\d+|\d+", str)
                    a = float(temp[0])
                    b = float(temp[1])
                    c = float(temp[2])
            if len(str) > 0:
                if str.find("ok") > -1:
                    return x, y, z, e, a, b, c

    """Delay"""

    def dealy_ms(self, value):
        self._send_cmd("G4 P" + str(value) + '\r')

    def dealy_s(self, value):
        self._send_cmd("G4 S" + str(value) + '\r')

    """SoftGripper & AirPicker"""

    def soft_gripper_pick(self):
        self._send_cmd("M1001\r")

    def soft_gripper_place(self):
        self._send_cmd("M1000\r")

    def soft_gripper_nature(self):
        self._send_cmd("M1002\r")

    def soft_gripper_stop(self):
        self._send_cmd("M1003\r")

    def air_picker_pick(self):
        self._send_cmd("M1000\r")

    def air_picker_place(self):
        self._send_cmd("M1001\r")

    def air_picker_nature(self):
        self._send_cmd("M1002\r")

    def air_picker_stop(self):
        self._send_cmd("M1003\r")

    """Laser"""

    def laser_on(self, value=0):
        self._send_cmd("M3 S" + str(value) + '\r')

    def laser_off(self):
        self._send_cmd("M5\r")

    """Conveyor Belt"""

    def conveyor_belt_forward(self, speed=0):
        self._send_cmd("M2012 S" + str(speed) + 'D0\r')

    def conveyor_belt_backward(self, speed=0):
        self._send_cmd("M2012 S" + str(speed) + 'D1\r')

    def conveyor_belt_stop(self, speed=0):
        self._send_cmd("M2013\r")


if __name__ == '__main__':
    import sys
    if "_machine" in dir(sys.implementation) and sys.implementation._machine.contains("Pico"):
        print(sys.implementation._machine)
        dexarm = Dexarm(0)
    elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):  # Load the arm on Windows
        dexarm = Dexarm("COM8")
    else:  # Load the arm on Mac or Linux
        dexarm = Dexarm("/dev/tty.usbmodem3086337A34381")

    dexarm.go_home()

    dexarm.move_to(50, 300, 0)


    dexarm.move_to(50, 300, -50)
    dexarm.air_picker_pick()
    dexarm.move_to(50, 300, 0)
    dexarm.move_to(-50, 300, 0)
    dexarm.move_to(-50, 300, -50)
    dexarm.air_picker_place()


    dexarm.go_home()
    dexarm.air_picker_stop()