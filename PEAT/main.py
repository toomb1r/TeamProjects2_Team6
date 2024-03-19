import adafruit_rfm9x
import board
import busio
import digitalio
import signal
import sys
from gps3 import gps3

from time import sleep, time

from utils.communications import *
from utils.movement import *

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

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)
    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    # signal.pause()
    signal.signal(signal.SIGINT, signal_handler)
    # receive()
    while True:
        if left_dist() < 30:
            transmit("1")
        sleep(5)

if __name__ == "__main__":
    main()
