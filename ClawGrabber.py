from pydexarm import Dexarm
import RPi.GPIO as GPIO
import os
import time
import math

coinPin = 11
gripPin = 12
upPin = 13
downPin = 15
leftPin = 16
rightPin = 18
COLLECTION_HEIGHT = -50
DROP_POSITION = -252, 194, 0
TIME_LIMIT = 30  #seconds allowed before grip timeout

GPIO.setmode(GPIO.BOARD) #Follow individual pin number scheme, versus the older Broadcom mode
#Also invoking pull-up resistors in software, to give IO pins positive Vcc. Pushing button grounds the connection
GPIO.setup(coinPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #'Coin input
GPIO.setup(gripPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 'Grip toggle between suction and release
GPIO.setup(upPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 'Up joystick input
GPIO.setup(downPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #'Down Joystick input
GPIO.setup(leftPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #'Left joystick input
GPIO.setup(rightPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # 'Right joystick input
#This is from the DexArm_API collection and is for python use, no specific platform
'''to find USB, use ls /dev/ttyAC* from command line'''
'''mac & linux -USB for Pi 3- ttyACM0 or ttyACM1'''
dexarm = Dexarm(port="/dev/ttyACM0")

dexarm.go_home()
dexarm.set_module_type(2) #End effector module is the pump/suction tip
dexarm.set_acceleration(200,200,200) #acceleration default is 60 in pydexarm.py

position = dexarm.get_current_position()
#print("Current Position returned:", position)
#print("X = ", position[0])
#print("Y = ", position[1])
#print("Z = ", position[2])
x = position[0]
y = position[1]
z = position[2]
speed = 4

angle, magnitude = math.degrees(math.atan2(y, x)) - 90, math.hypot(x, y)
magnitudeMin = 210
magnitudeMax = 405
angleMin = -45  #arm can go to -90. -45 is our box limit
angleMax =  58  #arm can go to  90.  but 58 is the limit of our box size.

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

while True:
    if GPIO.input(coinPin):
        os.system('echo 1 | sudo dd status=none of=/sys/class/leds/led0/brightness') #LED on
        time.sleep(0.2)
        os.system('echo 0 | sudo dd status=none of=/sys/class/leds/led0/brightness') #LED off
        time.sleep(0.1)
    else:
        dexarm.move_to(getX()+2, getY()+2, z, 0, 6000, "G0") #give a little wiggle to know it's on
        time.sleep(1)
        #Measure Time so the user must activate gripper within TIME_LIMIT seconds, like 30 seconds.
        ExpiredTime = time.time() + TIME_LIMIT
        while (GPIO.input(gripPin)):
            #print("Angle:", angle, "Magnitude:", magnitude)
            #Check the logic here. It can be up or down, left or right. Up + Left also valid.
            if not(GPIO.input(upPin)):
                #print("Up activated")
                if magnitudeMax >= magnitude + speed:
                    magnitude += speed
                else:
                    print("Max Magnitude")
            elif not(GPIO.input(downPin)):
                #print("Down activated")
                if magnitude - speed >= magnitudeMin:
                    magnitude -= speed
                else:
                    print("Min Magnitude")
            elif not(GPIO.input(leftPin)):
                #print("Left activated")
                if angleMax >= angle + speed:
                    angle += speed
                else:
                    print("Max Angle")
            elif not(GPIO.input(rightPin)):
                #print("Right activated")
                if angle - speed >= angleMin:
                    angle -= speed
                else:
                    print("Min Angle")
            else:
                position = dexarm.get_current_position()
                x = position[0]
                y = position[1]
                z = position[2]
                angle, magnitude = math.degrees(math.atan2(y, x)) - 90, math.hypot(x, y)
            dexarm.move_to(getX(), getY(), z, 0, 6000, "G1")
            #print("angle ", angle, "mag ", magnitude, "; X= ",getX(), " Y= ", getY())
            time.sleep(0.15) #Slow down the loop cycles. Smaller than 0.2 causes oscilation
            if time.time() > ExpiredTime:
                break #Break out of while loop if time limit reached

        #End of while gripPin loop - do the gripper thing!
        #print("GRIP activated!!")
        z_minus()
        dexarm.air_picker_pick()
        dexarm.move_to(getX(), getY(), COLLECTION_HEIGHT, 0, 6000, "G1")
        time.sleep(.5) #Pause to ensure we get the object
        dexarm.move_to(getX(), getY(), z, 0, 6000, "G1") #move back to clearance height
        dexarm.move_to(*DROP_POSITION)
        time.sleep(1) #pause to catch up. Maybe add more for drama!
        dexarm.air_picker_place()
        time.sleep(1)
        dexarm.go_home()
        dexarm.air_picker_stop()
        time.sleep(1)
        position = dexarm.get_current_position() #Set up variables for next run (coin)
        x = position[0]
        y = position[1]
        z = position[2]
        angle, magnitude = math.degrees(math.atan2(y, x)) - 90, math.hypot(x, y)
    #End of while true

#Print("Program ending.")
#Cleanup stuff:
dexarm.close()
GPIO.cleanup() #'Garbage collection
