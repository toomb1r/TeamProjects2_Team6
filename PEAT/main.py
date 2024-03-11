import adafruit_rfm9x
import board
import busio
import digitalio
from gps3 import gps3

from utils.communications import *
from utils.movement import *
from utils.algaecide import *

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
    dispense_algae()
    change_dispense_speed(100)

    while(True):
        # detect_out()
        edgeOfPond(rorl)
        move()

if __name__ == "__main__":
    main()
