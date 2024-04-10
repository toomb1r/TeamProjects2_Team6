import RPi.GPIO as GPIO
import signal
import sys

from utils.bg_files.movement import *
from utils.communications import *

GPIO.setmode(GPIO.BCM)

def signal_handler(sig, frame):
    """Handles CTRL+C inputs
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
    """Executes the main functionality of PEAT.
    Repeatedly checks if the edge of the pond is detected.

    Args:
        None

    Returns:
        None
    """

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        edgeOfPond()

if __name__ == "__main__":
    main()
