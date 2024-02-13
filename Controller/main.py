import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO

from utils.communications import *
from utils.actions import *

GPIO.setmode(GPIO.BOARD)

def main():
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """

    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)
    GPIO.add_event_detect(17, GPIO.FALLING, callback=emergencyStop(), bouncetime=100)

if __name__ == "__main__":
    main()
