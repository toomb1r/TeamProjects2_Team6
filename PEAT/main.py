import adafruit_rfm9x
import board
import busio
import digitalio
import signal
import sys
from gps3 import gps3

from time import sleep, time
import RPi.GPIO as GPIO

from utils.communications import *
from utils.movement import *
from utils.pins import *

#turn = get_turn()
#turnpwm = GPIO.PWM(turn,50)
#turnpwm.start(0)
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
    turnpwm.ChangeDutyCycle(5)
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
        print(f"left distance {left_dist()}")
        print(f"right distance {right_dist()}")
        # var = receive().strip()
        # if var == "9":
        #     start()

if __name__ == "__main__":
    main()
