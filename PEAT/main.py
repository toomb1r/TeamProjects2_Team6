import adafruit_rfm9x
import board
import busio
import digitalio
import signal
import sys
from gps3 import gps3

from time import sleep, time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

from utils.communications import *
from utils.bg_movement import *
from utils.bg_files.algaecide import *
from utils.gps import *
from utils.pins import *

GPIO.setmode(GPIO.BCM)

stopped = False
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

start_time = time()
distances = [[0, 0], [0, 0], [0, 0], [0, 0]]

def find_distance():
    global start_time
    global ser
    #print(f"Start time: {start_time}\n Current time: {time()}\n")
    # if time() - start_time == 60:
    #print("inside if")
    lat1, lon1 = get_location()
    # lat2, lon2 = get_location()
    # meters = convert_to_meters(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
    #print(f"coords 1: {lat1} {lon1}\n\n\n")
    if len(distances) > 4:
        distances.append([lat1, lon1])
    if len(distances) == 4:
        distances.pop(0)
        distances.append([lat1, lon1])
        print(f"{distances}\n")

def receive_state():
    global stopped
    start_receive = time()
    zero = False
    sixty = False
    while True:
        print("while loop")
        received_sig = ""
        if time() - start_receive > 0 and not zero:
            find_distance()
            zero = True
        elif time() - start_receive > 60 and not sixty:
            find_distance()
            sixty = True
        try:
            print("trying to receive")
            received_sig = receive(60.0).strip()
        except:
            print("Error: Receive failed\n")
            continue
        print(received_sig)
        if received_sig == "13":
            if GPIO.input(get_drive_in1()) or GPIO.input(get_auger_in1()):
                stop()
                stop_dispense()
            else:
                start()
                dispense_algae()
            stopped = not stopped
        if not stopped:
            if received_sig == "5":
                setHome()
            elif received_sig == "9":
                if GPIO.input(in1):
                    stop()
                else:
                    start()
            elif received_sig == "11":
                if GPIO.input(auger1):
                    stop_dispense()
                else:
                    dispense_algae()
            elif received_sig == "21":
                change_dispense_speed(90)
            elif received_sig == "22":
                change_dispense_speed(91)
            elif received_sig == "23":
                change_dispense_speed(92)
            elif received_sig == "24":
                change_dispense_speed(93)
            elif received_sig == "25":
                change_dispense_speed(94)
            elif received_sig == "26":
                change_dispense_speed(95)
            elif received_sig == "27":
                change_dispense_speed(96)
            elif received_sig == "28":
                change_dispense_speed(97)
            elif received_sig == "29":
                change_dispense_speed(98)
            elif received_sig == "30":
                change_dispense_speed(99)
            elif (received_sig == "40"):
                break
            elif (received_sig == "50"):
                print("Error: Receive failed (signal 50)")
                continue
    # while True:
    #     received_sig = receive(40.0).strip()
    #     if (received_sig == "1"):
    #         trigger_IMMOBILIZED_LIGHT()
    #         print("triggered immobilized light")
    #     elif (received_sig == "3"):
    #         trigger_OUT_OF_ALGAECIDE_LIGHT(True)
    #         print("triggered out of algaecide light")
    #     elif (received_sig == "4"):
    #         trigger_OUT_OF_ALGAECIDE_LIGHT(False)
    #         print("Turned algaecide light off")

    #     traversed_time = time() - start_time
    #     if (traversed_time > 40.0):
    #         break


def transmit_state():
    global distances
    # 1: has algaecide and is moving
    # 2: has algaecide and is not moving
    # 3: has no algaecide and is moving
    # 4: has no algaecide and is not moving

    out_of_algaecide = detect_out()
    print(f"distances: {distances}")
    distance = check_distances(distances)
    print(f"distance measurement: {distance}")
    immobilized = distance < 12
    # edgeOfPond()
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
    """Executes the main functionality of PEAT

    Args: None

    Returns: None
    """
    global start_time
    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    #sleep(5)

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

    signal.signal(signal.SIGINT, signal_handler)
    # find_distance()
    #start_time = time()
    # receive()
    readHome()
    #start()
    # lat1, lon1 = get_location()
    # lat2, lon2 = get_location()
    # meters = convert_to_meters(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
    # print(f"meters different {meters} \ncoords 1: {lat1} {lon1} \ncoords 2: {lat2} {lon2}\n\n\n")
    # distances.append(meters)
    # start()
    # if time() - start_time == 60:
    #     lat1, lon1 = get_location()
    #     lat2, lon2 = get_location()
    #     meters = convert_to_meters(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
    #     print(f"meters different {meters} \ncoords 1: {lat1} {lon1} \ncoords 2: {lat2} {lon2}\n\n\n")
    #     if len(distances) > 4:
    #         distances.append(meters)
    #     if len(distances) == 4:
    #         distances.pop(0)
    #         distances.append(meters)
    #         if check_distances(distances) > 12:
    #             # do the immobilized stuff here
    #             pass
    # find_distance_start()
    while True:
        # edgeOfPond()
        start_time = time()
        print(f"starting receive on PEAT. time = {time() - start_time}\n")
        receive_state()
        print(f"finishing receive on PEAT. time = {time() - start_time}\n")
        print(f"starting transmit on PEAT. time = {time() - start_time}\n")
        transmit_state()
        print(f"finishing transmit on PEAT. time = {time() - start_time}\n")
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



# controller in transmit state for 120 s                                            PEAT in receive state for 120 s
# 1. controller transmits signal 40 at end and switches to receive                  2. PEAT receives signal 40 at end and switches to transmit
# 2. controller receives what it needs to and switches from receive to transmit     1. PEAT transmits what it needs to and switches from transmit to receive
# controller in transmit state for 120 s                                            PEAT in receive state for 120 s
