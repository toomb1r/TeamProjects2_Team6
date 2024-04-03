import random
import RPi.GPIO as GPIO
from time import sleep, time
from gpiozero import DistanceSensor

# This is incorrect figure this out before merge
en = 26
in1 = 22
in2 = 6
turn = 13
TRIGl = 12
ECHOl = 19
TRIGr = 23
ECHOr = 24
rth = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(turn, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(TRIGl, GPIO.OUT)
GPIO.setup(ECHOl, GPIO.IN)
GPIO.setup(TRIGr, GPIO.OUT)
GPIO.setup(ECHOr, GPIO.IN)
GPIO.setup(rth, GPIO.OUT)

movepwm=GPIO.PWM(en,1000)
movepwm.start(25)

movepwm.ChangeDutyCycle(100)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(rth, GPIO.HIGH)

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

def reverse():
    """
    Makes the motor move in reverse

    Turns on the output for both inputs of the motor in reverse order, which reverses the motor

    Args:
        None

    Returns:
        None
    """
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

def return_to_home():
    """
    Activates return to home GPIO boolean

    Turns the return to home pin (pin 8) to high

    Args:
        None
    Returns:
        None
    """
    GPIO.output(rth, GPIO.HIGH)