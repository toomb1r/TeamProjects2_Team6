import RPi.GPIO as GPIO
from time import sleep, time

auger_en = 4
auger1 = 17
auger2 = 27
dispenser_en = 18
dispenser1 = 20
dispenser2 = 21
TRIG = 2
ECHO = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(auger1, GPIO.OUT)
GPIO.setup(auger2, GPIO.OUT)
GPIO.setup(auger_en, GPIO.OUT)
GPIO.setup(dispenser1, GPIO.OUT)
GPIO.setup(dispenser2, GPIO.OUT)
GPIO.setup(dispenser_en, GPIO.OUT)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def dispense_algae():
    """
    Starts the dispensing of algaecide

    Turns on the auger and dispenser motors

    Args:
        None
    Returns:
        None
    """
    GPIO.output(auger1, GPIO.HIGH)
    GPIO.output(auger2, GPIO.LOW)
    GPIO.output(dispenser1, GPIO.HIGH)
    GPIO.output(dispenser2, GPIO.LOW)

def stop_dispense():
    """
    Stops the dispensing of algaecide

    Turns off the auger and dispenser motors

    Args:
        None
    Returns:
        None
    """
    print("STOPPING ALGACIDE")
    GPIO.output(auger1, GPIO.LOW)
    GPIO.output(auger2, GPIO.LOW)
    GPIO.output(dispenser1, GPIO.LOW)
    GPIO.output(dispenser2, GPIO.LOW)
