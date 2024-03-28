import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO as GPIO

import signal
import sys

from time import sleep

from utils.communications import *
#from utils.actions import *

stop = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(15,GPIO.IN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def emergency_stop(channel):
    global stop
    stop = not stop
    print("stop")

GPIO.add_event_detect(15, GPIO.FALLING, callback=emergency_stop, bouncetime=200)

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
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    # transmit("hi")
    # receive()

    #transmit_and_receive()
    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    signal.signal(signal.SIGINT, signal_handler)
    # This only exists in unix
    # signal.pause()

    while True:
        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.HIGH)
        # GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.LOW)
        # sleep(1)
        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
        # GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.HIGH)
        # sleep(1)

        # print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
        # sleep(0.2)

        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.HIGH)
        # sleep(1)
        signal.signal(signal.SIGINT, signal_handler)
        received_sig = receive().strip()
        if (received_sig == "1"):
            trigger_IMMOBILIZED_LIGHT()
            print("triggered immobilized light")
        elif (received_sig == "3"):
            trigger_OUT_OF_ALGAECIDE_LIGHT(True)
            print("triggered out of algaecide light")
        elif (received_sig == "4"):
            trigger_OUT_OF_ALGAECIDE_LIGHT(False)
            print("Turned algaecide light off")
        # sleep(5)
        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
        # sleep(1)

if __name__ == "__main__":
    main()
