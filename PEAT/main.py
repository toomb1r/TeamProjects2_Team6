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
from utils.gps import *
#from utils.pins import *

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

def receive_state():
    while True:
        received_sig = receive(120.0).strip()
        print(received_sig)
        if received_sig == "9":
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
        elif received_sig =="22":
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


def transmit_state(distances):
    # 1: has algaecide and is moving
    # 2: has algaecide and is not moving
    # 3: has no algaecide and is moving
    # 4: has no algaecide and is not moving

    out_of_algaecide = detect_out()
    distance = check_distances(distances)
    immobilized = distance < 12
    # edgeOfPond()
    if not out_of_algaecide and not immobilized:
        transmit("1")
    elif not out_of_algaecide and immobilized:
        transmit("2")
    elif out_of_algaecide and not immobilized:
        transmit("3")
    elif out_of_algaecide and immobilized:
        transmit("4")

def main():
    """Executes the main functionality of PEAT

    Args: None

    Returns: None
    """

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    #sleep(5)

    #slee

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

    signal.signal(signal.SIGINT, signal_handler)
    #start_time = time()
    distances = [[0, 0], [0, 0], [0, 0], [0, 0]]
    # receive()
    #start()
    # lat1, lon1 = get_location()
    # lat2, lon2 = get_location()
    # meters = convert_to_meters(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
    # print(f"meters different {meters} \ncoords 1: {lat1} {lon1} \ncoords 2: {lat2} {lon2}\n\n\n")
    # distances.append(meters)
    start()
    while True:
        # edgeOfPond()
        start_time = time()
        print(f"starting receive on PEAT. time = {time() - start_time}\n")
        receive_state()
        print(f"finishing receive on PEAT. time = {time() - start_time}\n")
        print(f"starting transmit on PEAT. time = {time() - start_time}\n")
        transmit_state(distances)
        print(f"finishing transmit on PEAT. time = {time() - start_time}\n")
        #if time() - start_time == 60:
            #lat1, lon1 = get_location()
            #lat2, lon2 = get_location()
            #meters = convert_to_meters(lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
            #print(f"meters different {meters} \ncoords 1: {lat1} {lon1} \ncoords 2: {lat2} {lon2}\n\n\n")
            #if len(distances) > 4:
                #distances.append(meters)
            #if len(distances) == 4:
                #distances.pop(0)
                #distances.append(meters)
                #if check_distances(distances) > 12:
                    # do the immobilized stuff here
                    #pass


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
