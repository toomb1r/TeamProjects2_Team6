import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO as GPIO
import signal
import sys
from time import sleep, time

from utils.communications import *

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

def receive_state():
    # while True:
    received_sig = receive(40.0).strip()
    if (received_sig == "1"):
        trigger_IMMOBILIZED_LIGHT()
        print("triggered immobilized light")
    elif (received_sig == "3"):
        trigger_OUT_OF_ALGAECIDE_LIGHT(True)
        print("triggered out of algaecide light")
    elif (received_sig == "4"):
        trigger_OUT_OF_ALGAECIDE_LIGHT(False)
        print("Turned algaecide light off")

def transmit_state(start_time):
    while True:
        traversed_time = time() - start_time
        if (traversed_time > 120.0):
            transmit("40")
            break

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
        start_time = time()
        transmit_state(start_time)
        receive_state()

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
        
        # sleep(5)
        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
        # sleep(1)

if __name__ == "__main__":
    main()


# controller in transmit state for 120 s                                            PEAT in receive state for 120 s
# 1. controller transmits signal 40 at end and switches to receive                  2. PEAT receives signal 40 at end and switches to transmit
# 2. controller receives what it needs to and switches from receive to transmit     1. PEAT transmits what it needs to and switches from transmit to receive
# controller in transmit state for 120 s                                            PEAT in receive state for 120 s
