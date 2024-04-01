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
from utils.algaecide import *
from utils.pins import *

GPIO.setmode(GPIO.BCM)

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
    #turnpwm.ChangeDutyCycle(5)
    GPIO.cleanup()
    sys.exit(0)

def main():
    """Executes the main functionality of PEAT

    Args: None

    Returns: None
    """
    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    signal.signal(signal.SIGINT, signal_handler)

    # receive()
    stopped = False
    while True:
        var = receive().strip()
        if var == "13":
            if GPIO.input(get_drive_in1()) or GPIO.input(get_auger_in1()):
                stop()
                stop_dispense()
            else:
                start()
                dispense_algae()
            stopped = not stopped
        if not stopped:
            if var == "9":
                if GPIO.input(get_drive_in1()):
                    stop()
                else:
                    start()
            if var == "11":
                if GPIO.input(get_auger_in1()):
                    stop()
                else:
                    start()
        #sleep(5)


        # transmit_and_receive()

        # This is how to make an interrupt, this is commented out because idk how to get
        # the string from what is being called in from the controller...
        # GPIO.add_event_detect(9, GPIO.FALLING, callback=decrypt())

    # This is to start the servo motor in the center of the 180 degrees
    # To allow -90 and 90 degrees of motion
    #turning(90)

    #move()
    #rorl = True
    #dispense_algae()
    #dispense_algae()
    #change_dispense_speed(100)

    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    # signal.pause()

        # var = receive().strip()
        # if var == "9":
        #     start()
    #dispense_algae()
    #while(True):
    #    if detect_out():
    #        transmit("3")
    #    var = receive().strip()
    #    if var == "11":
    #        if GPIO.input(get_auger_in1()):
    #            stop_dispense()
    #        else:
    #            dispense_algae()
    #    elif var == "21":
    #        change_dispense_speed(90)
    #    elif var =="22":
    #        change_dispense_speed(91)
    #    elif var == "23":
    #        change_dispense_speed(92)
    #    elif var == "24":
    #        change_dispense_speed(93)
    #    elif var == "25":
    #        change_dispense_speed(94)
    #    elif var == "26":
    #        change_dispense_speed(95)
    #    elif var == "27":
    #        change_dispense_speed(96)
    #    elif var == "28":
    #        change_dispense_speed(97)
    #    elif var == "29":
    #        change_dispense_speed(98)
    #    elif var == "30":
    #        change_dispense_speed(99)
    #    sleep(1.5)
        #print("enter new speed")
        #speed = int(input())
        #change_dispense_speed(speed)
        # detect_out()
        #edgeOfPond(rorl)
        #move()

if __name__ == "__main__":
    main()
