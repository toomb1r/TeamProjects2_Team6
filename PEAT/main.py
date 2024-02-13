import adafruit_rfm9x
import board
import busio
import digitalio
import signal
import sys
from gps3 import gps3

from utils.communications import *
from utils.movement import *

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

    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)

    # This is how to make an interrupt, this is commented out because idk how to get
    # the string from what is being called in from the controller...
    # GPIO.add_event_detect(9, GPIO.FALLING, callback=decrypt())

    # This is to start the servo motor in the center of the 180 degrees
    # To allow -90 and 90 degrees of motion
    turning(90)

    move()
    rorl = True

    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    signal.signal(signal.SIGINT, signal_handler)
    # signal.pause()

    while(True):
        edgeOfPond(rorl)
        move()

if __name__ == "__main__":
    main()
