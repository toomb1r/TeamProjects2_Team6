import adafruit_rfm9x
import board
import busio
import digitalio
import signal
import sys
from gps3 import gps3

from time import sleep, time

from utils.communications import *
# from utils.movement import *

GPIO.setmode(GPIO.BCM)

def main():
    """Executes the main background functionality of PEAT

    Args: None

    Returns: None
    """

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)
    while True:
        receive()
        # if statements here

if __name__ == "__main__":
    main()
