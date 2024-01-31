from gps3 import gps3
import RPi.GPIO as GPIO
import random
import digitalio
import board
import busio
import adafruit_rfm9x
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

random.seed()

rorl = True
constant = 20

def turning(direction):
    """
    Turns the rudder of PEAT to allow for turning
    Takes the direction from the input and moves the servo motor to there

    Args:
        direction (int): the direction where the rudder will turn (-90 - 90)

    Returns:
        None
    """
    # This is untested and probably wont work
    GPIO.output(13, direction)

def edgeOfPond():
    """
    Determines if the edge of the pond is detected
    If so it will turn the boat and move it a constant time
    After moving this constant time it will turn back in the direction it came from

    Args:
        None

    Returns:
        None
    """
    # If edge of pond detected
    if(GPIO.input(24)):

        # Stop all movement and turn the correct direction
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        if(rorl):
            turning(90)
        else:
            turning(-90)

        # Move for a constant time
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        sleep(constant)

        # Stop all movement and turn the correct direction
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        if(rorl):
            turning(90)
        else:
            turning(-90)

        # Change the turning direction unless the edge of pond is still in front of PEAT
        rorl = not rorl
        if(GPIO.input(24)):
            rorl = not rorl

        # Check if the edge of pond is still in front of PEAT
        edgeOfPond()

def move():
    """
    This begins the movement of the rudder of PEAT
    It selects a random direction and moves there

    Args:
        None

    Returns:
        None
    """
    turning(random.randrange(-90, 90))
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)

# This is to start the servo motor in the center of the 180 degrees
# To allow -90 and 90 degrees of motion
turning(90)

move()
while(True):
    edgeOfPond()
    move()

# Im pretty sure this is needed although I need to figure out how to add it in
# GPIO.cleanup()
