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

TRIGl = 12
GPIO.setup(TRIGl, GPIO.OUT)

ECHOl = 16
GPIO.setup(ECHOl, GPIO.IN)


def left_dist():
    """
    Returns distance of left ultrasonic sensor

    Measures the distance in front of the left ultrasonic sensor
    returns the distance in the form of cms

    Args:
        None
    Returns:
        distance (int): Distance in front of ultrasonic sensor in cm
    """
    distance = 0

    #print("Distance Measurement In Progress")

    GPIO.output(TRIGl, False)
    #print("Waiting For Sensor To Settle")
    sleep(2)

    GPIO.output(TRIGl, True)
    sleep(0.00001)
    GPIO.output(TRIGl, False)

    while GPIO.input(ECHOl) == 0:
        pulse_start = time()
        #print("stuck in start")

    while GPIO.input(ECHOl) == 1:
        pulse_end = time()
        #print("stuck in end")

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # speed of sound in air
    # distance = pulse_duration * 75000 # speed of sound in water
    distance = round(distance, 2)
    print(f"Distance: {distance} cm")
    return distance

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

    while True:
        receive()
    # while True:
    #     if left_dist() < 30:
    #         transmit("1")
    #     sleep(5)
    # #sleep(5)

    # transmit_and_receive()

    # This is how to make an interrupt, this is commented out because idk how to get
    # the string from what is being called in from the controller...
    # GPIO.add_event_detect(9, GPIO.FALLING, callback=decrypt())

    # This is to start the servo motor in the center of the 180 degrees
    # To allow -90 and 90 degrees of motion
    # turning(90)

    # move()
    # rorl = True

    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    signal.signal(signal.SIGINT, signal_handler)
    # signal.pause()

    # while(True):
    #     edgeOfPond(rorl)
    #     move()

if __name__ == "__main__":
    main()
