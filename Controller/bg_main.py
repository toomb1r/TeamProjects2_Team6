import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO as GPIO
import signal
import sys
from time import sleep

from utils.communications import *

GPIO.setmode(GPIO.BCM)

def main():
    """Executes the main background functionality of the Controller

    Args: None

    Returns: None
    """

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    while True:
        received_sig = receive().strip()
        if (received_sig == "1"):
            trigger_IMMOBILIZED_LIGHT()
            print("triggered immobilized light")
        elif (received_sig == "3"):
            trigger_OUT_OF_ALGAECIDE_LIGHT()
            print("triggered out of algaecide light")

if __name__ == "__main__":
    main()
