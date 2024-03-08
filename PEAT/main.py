import adafruit_rfm9x
import board
import busio
import digitalio
from gps3 import gps3

from utils.communications import *
from utils.movement import *

stop = 20

def emergency_stop():
    GPIO.wait_for_edge(stop, GPIO.FALLING)

GPIO.add_event_detect(stop, GPIO.FALLING, callback=emergency_stop(), bouncetime=200)

def main():
    """Executes the main functionality of PEAT

    Args: None

    Returns: None
    """

    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)

    # This is to start the servo motor in the center of the 180 degrees
    # To allow -90 and 90 degrees of motion
    turning(90)

    move()
    rorl = True
    while(True):
        edgeOfPond(rorl)
        move()

if __name__ == "__main__":
    main()
