import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO
import signal
import sys

from utils.communications import *

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
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """

    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)

    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    signal.signal(signal.SIGINT, signal_handler)
    # This only exists in unix
    signal.pause()

if __name__ == "__main__":
    main()
