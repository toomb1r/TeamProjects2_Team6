import adafruit_rfm9x
import board
import busio
import digitalio
import signal
import sys
from gps3 import gps3

import RPi.GPIO as GPIO

from utils.communications import *
from utils.bg_files.movement import *
#from utils.algaecide import *
# from utils.pins import *

GPIO.setmode(GPIO.BCM)

def signal_handler(sig, frame):
    """
    Handles CTRL+C inputs

    This will clean up GPIO whenever the command CTRL+C is sent
    This will allow us to actually use CTRL+C without erroring next time the code is run

    Args:
        sig: ??
        frame: ??

    Returns:
        None

    Cited: https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
    """
    GPIO.cleanup()
    sys.exit(0)

def main():
    """Executes the main functionality of PEAT

    Args: None

    Returns: None
    """
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        edgeOfPond()
        #var = receive().strip()
        #if var == "9":
        #    if GPIO.input(get_drive_in1()):
        #        stop()
        #        print("Stopped movement")
        #    else:
        #        start()
        #        print("Start movement")
        #elif var == "11":
        #    if GPIO.input(get_auger_in1()):
        #        stop_dispense()
        #    else:
        #        dispense_algae()
        #elif var == "21":
        #    change_dispense_speed(90)
        #elif var =="22":
        #    change_dispense_speed(91)
        #elif var == "23":
        #    change_dispense_speed(92)
        #elif var == "24":
        #    change_dispense_speed(93)
        #elif var == "25":
        #    change_dispense_speed(94)
        #elif var == "26":
        #    change_dispense_speed(95)
        #elif var == "27":
        #    change_dispense_speed(96)
        #elif var == "28":
        #    change_dispense_speed(97)
        #elif var == "29":
        #    change_dispense_speed(98)
        #elif var == "30":
        #    change_dispense_speed(99)

if __name__ == "__main__":
    main()
