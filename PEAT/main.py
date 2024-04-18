import RPi.GPIO as GPIO
import signal
import sys
from time import time

GPIO.setmode(GPIO.BCM)

from utils.algaecide import *
from utils.communications import *
from utils.gps import *
from utils.movement import *

def signal_handler(sig, frame):
    """Handles CTRL+C inputs.

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

start_time = time()
distances = [[0, 0], [0, 0], [0, 0], [90, 90]]
stopped = False

def find_distance():
    """
    Gathers GPS data point for the current location and stores it.

    Gathers the current GPS data point and stores it into the distances list.
    If the distances list has 4 items in it, it will remove the first item and add the new location.

    Args:
        None

    Returns:
        None
    """
    global start_time
    global ser

    lat1, lon1 = get_location()
    if lat1 == 0 and lon1 == 0:
        print("Error: Couldnt gather GPS data")
        return

    if len(distances) > 4:
        distances.append([lat1, lon1])
    if len(distances) == 4:
        distances.pop(0)
        distances.append([lat1, lon1])
        print(f"{distances}\n")

def receive_state():
    """
    State in which PEAT will receive signals from the Controller.

    Loops until signal 40 is received (generally every 120 seconds).
    Performs various functions based on other received signals.
    Records a GPS coordinate upon start and after 60 seconds.

    Args:
        None

    Returns:
        None
    """

    start_receive = time()
    zero = False
    sixty = False
    global stopped

    while True:
        received_sig = ""
        if time() - start_receive > 0 and not zero:
            find_distance()
            print("NOT SKIPPING GPS")
            zero = True
        elif time() - start_receive > 60 and not sixty:
            find_distance()
            print("NOT SKIPPING GPS")
            sixty = True
        try:
            received_sig = receive(60.0).strip()
        except:
            print("Error: Receive failed\n")
            continue
        print(received_sig)
        if received_sig == "13":
            print("emergency stop")
            stopped = not stopped
            stop()
            stop_dispense()
        elif (received_sig == "40"):
            break
        elif (received_sig == "50"):
            print("Error: Receive failed (signal 50)")
            continue
        if not stopped:
            if received_sig == "5":
                setHome()
            elif received_sig == "7":
                stop_dispense()
                return_to_home()
            elif received_sig == "9":
                if GPIO.input(in1):
                    stop()
                else:
                    start_up()
            elif received_sig == "11":
                if GPIO.input(auger1):
                    stop_dispense()
                else:
                    dispense_algae()
            elif received_sig == "21":
                change_dispense_speed(100)
            elif received_sig == "22":
                change_dispense_speed(98)
            elif received_sig == "23":
                change_dispense_speed(96)
            elif received_sig == "24":
                change_dispense_speed(94)
            elif received_sig == "25":
                change_dispense_speed(92)
            elif received_sig == "26":
                change_dispense_speed(90)
            elif received_sig == "27":
                change_dispense_speed(88)
            elif received_sig == "28":
                change_dispense_speed(86)
            elif received_sig == "29":
                change_dispense_speed(84)
            elif received_sig == "30":
                change_dispense_speed(82)

def transmit_state():
    """
    State in which PEAT will transmit signals to the Controller.

    Transmits a signal to the Controller to determine which lights to turn on.

    Args:
        None

    Returns:
        None
    """

    global distances
    out_of_algaecide = detect_out()
    print(f"distances: {distances}")
    distance = check_distances(distances)
    print(f"distance measurement: {distance}")
    immobilized = distance < 12

    if not out_of_algaecide and not immobilized:
        try:
            transmit("1")
        except:
            print("Error: Transmit signal 1 failed\n")
    elif not out_of_algaecide and immobilized:
        try:
            stop_dispense()
            stop()
            transmit("2")
        except:
            print("Error: Transmit signal 2 failed\n")
    elif out_of_algaecide and not immobilized:
        try:
            transmit("3")
        except:
            print("Error: Transmit signal 3 failed\n")
    elif out_of_algaecide and immobilized:
        try:
            stop_dispense()
            stop()
            transmit("4")
        except:
            print("Error: Transmit signal 4 failed\n")

def main():
    """
    Executes the main functionality of PEAT.

    Alternates calling PEAT's receive and transmit states.

    Args:
        None

    Returns:
        None
    """

    global start_time
    signal.signal(signal.SIGINT, signal_handler)
    readHome()

    while True:
        start_time = time()
        print(f"starting receive on PEAT. time = {time() - start_time}\n")
        receive_state()
        print(f"finishing receive on PEAT. time = {time() - start_time}\n")
        print(f"starting transmit on PEAT. time = {time() - start_time}\n")
        transmit_state()
        print(f"finishing transmit on PEAT. time = {time() - start_time}\n")

if __name__ == "__main__":
    main()
