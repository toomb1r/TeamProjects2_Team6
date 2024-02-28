import random
import RPi.GPIO as GPIO
from time import sleep

random.seed()

# This is incorrect figure this out before merge
en = 4
in1 = 20
in2 = 21
turn = 13
GPIO.setmode(GPIO.BCM)
GPIO.setup(turn, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

turnpwm=GPIO.PWM(turn,50)
movepwm=GPIO.PWM(en,1000)
movepwm.start(25)
turnpwm.start(0)

turnpwm.ChangeDutyCycle(5)
movepwm.ChangeDutyCycle(75)

# This code probably should be in the main method although this will probably be run first so it doesnt matter?
# Consult with team
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

def turning(direction):
    """Turns the rudder of PEAT to allow for turning
    Takes the direction from the input and moves the servo motor to there

    Args:
        direction (int): the direction where the rudder will turn (-90 - 90)

    Returns:
        None
    """

    turnpwm.ChangeDutyCycle(direction)

def stop():
    """
    Ceases motion for the movement motors
    Turns off the output for both inputs of the motor, which turns the motor off

    Args:
        None

    Returns:
        None
    """
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def start():
    """
    Beings motion for the movement motors
    Turns on the output for both inputs of the motor, which turns the motor on

    Args:
        None

    Returns:
        None
    """
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

def edgeOfPond(rorl):
    """Turns PEAT if the edge of the pond is detected
    Determines if the edge of the pond is detected
    If so it will turn the boat and move it a constant time
    After moving this constant time it will turn back in the direction it came from

    Args:
        rorl (bool) - determines the direction PEAT will turn when the edge of the pond is detected

    Returns:
        None
    """

    # During testing we can determine whether or not this is needed
    # constant = 20

    # If edge of pond detected
    # consult Anmol about progress on the ultrasonic sensor code
    if(GPIO.input(24)):

        # Stop all movement and turn the correct direction
        stop()
        if(rorl):
            turning(10)
        else:
            turning(0)

        # Move for a constant time
        start()

        # Uncomment this if constant is needed
        # sleep(constant)

        # Stop all movement and turn the correct direction
        stop()
        turning(5)
        # if(rorl):
        #     turning(10)
        # else:
        #     turning(0)

        # Change the turning direction unless the edge of pond is still in front of PEAT
        rorl = not rorl
        if(GPIO.input(24)):
            rorl = not rorl

        # Check if the edge of pond is still in front of PEAT
        edgeOfPond()

def move():
    """Begins the movement of the rudder of PEAT
    Selects a random direction and moves there

    Args:
        None

    Returns:
        None
    """
    turning(round(random.uniform(0, 10), 1))
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
