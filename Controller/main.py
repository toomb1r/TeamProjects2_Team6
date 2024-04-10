import RPi.GPIO as GPIO
import signal
import sys
from time import time

GPIO.setmode(GPIO.BCM)

from utils.communications import *

def signal_handler(sig, frame):
    """
    Handles CTRL+C inputs.

    This will clean up GPIO whenever the command CTRL+C is sent.
    This will allow us to actually use CTRL+C without erroring next time the code is run.

    Args:
        sig: ??
        frame: ??

    Returns:
        None

    Citation:
        https://roboticsbackend.com/raspberry-pi-gpio-interrupts-tutorial/
    """

    GPIO.cleanup()
    sys.exit(0)

def receive_state():
    """
    State in which the Controller will receive signals from PEAT.

    Receives a signal from PEAT to determine which lights to turn on.

    Args:
        None

    Returns:
        None
    """

    set_in_transmit_state(False)
    received_sig = ""
    try:
        received_sig = receive(30).strip()
    except:
        print("Error: Receive failed")
    print(received_sig)

    if received_sig == "1":
        OUT_OF_ALGAECIDE_LIGHT_off()
        IMMOBILIZED_LIGHT_off()
        print("out of algaecide: off\timmobilized: off\n")
    elif received_sig == "2":
        OUT_OF_ALGAECIDE_LIGHT_off()
        IMMOBILIZED_LIGHT_on()
        print("out of algaecide: off\timmobilized: on\n")
    elif (received_sig == "3"):
        OUT_OF_ALGAECIDE_LIGHT_on()
        IMMOBILIZED_LIGHT_off()
        print("out of algaecide: on\timmobilized: off\n")
    elif (received_sig == "4"):
        OUT_OF_ALGAECIDE_LIGHT_on()
        IMMOBILIZED_LIGHT_on()
        print("out of algaecide: on\timmobilized: on\n")
    elif (received_sig == "50"):
        print("Error: Receive failed (signal 50)")

def transmit_state(start_time):
    """
    State in which the Controller will transmit signals to PEAT.

    Loops for 120 seconds before transmitting signal 40 and exiting.
    Buttons on the Controller can be pressed during this time.

    Args:
        start_time (float): The time at which this round of transmit and receive states began

    Returns:
        None
    """

    set_in_transmit_state(True)
    while True:
        traversed_time = time() - start_time
        if (traversed_time > 120.0):
            try:
                transmit("40")
            except:
                print("Error: Transmit signal 40 failed\n")
                continue
            break

def main():
    """
    Executes the main functionality of the Controller.
    
    Alternates calling the Controller's transmit and receive states.

    Args:
        None

    Returns:
        None
    """

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        start_time = time()
        print(f"starting transmit on controller. time = {time() - start_time}\n")
        transmit_state(start_time)
        print(f"finishing transmit on controller. time = {time() - start_time}\n")
        print(f"starting receive on controller. time = {time() - start_time}\n")
        receive_state()
        print(f"finishing receive on controller. time = {time() - start_time}\n")

if __name__ == "__main__":
    main()
