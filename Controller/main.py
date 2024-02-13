import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO

from utils.communications import *

def main():
    """Executes the main functionality of PEAT

    Args: None

    Returns: None
    """

    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)

if __name__ == "__main__":
    main()
