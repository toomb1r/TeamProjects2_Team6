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
    # 1: has algaecide and is moving
    # 2: has algaecide and is not moving
    # 3: has no algaecide and is moving
    # 4: has no algaecide and is not moving

    set_in_transmit_state(False)
    # while True:
    received_sig = ""
    try:
        received_sig = receive(30).strip()
    except:
        print("Error: Receive failed")
        # return
    print(received_sig)
    if received_sig == "1":
        # trigger_IMMOBILIZED_LIGHT()
        # print("triggered immobilized light")
        OUT_OF_ALGAECIDE_LIGHT_off()
        IMMOBILIZED_LIGHT_off()
        print("out of algaecide: off\timmobilized: off\n")
    elif received_sig == "2":
        OUT_OF_ALGAECIDE_LIGHT_off()
        IMMOBILIZED_LIGHT_on()
        print("out of algaecide: off\timmobilized: on\n")
    elif (received_sig == "3"):
        # trigger_OUT_OF_ALGAECIDE_LIGHT(True)
        # print("triggered out of algaecide light")
        OUT_OF_ALGAECIDE_LIGHT_on()
        IMMOBILIZED_LIGHT_off()
        print("out of algaecide: on\timmobilized: off\n")
    elif (received_sig == "4"):
        # trigger_OUT_OF_ALGAECIDE_LIGHT(False)
        # print("Turned algaecide light off")
        OUT_OF_ALGAECIDE_LIGHT_on()
        IMMOBILIZED_LIGHT_on()
        print("out of algaecide: on\timmobilized: on\n")

def transmit_state(start_time):
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
        print(f"starting transmit on controller. time = {time() - start_time}\n")
        transmit_state(start_time)
        print(f"finishing transmit on controller. time = {time() - start_time}\n")
        print(f"starting receive on controller. time = {time() - start_time}\n")
        receive_state()
        print(f"finishing receive on controller. time = {time() - start_time}\n")
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
        #received_sig = receive().strip()
        #if (received_sig == "1"):
        #    trigger_IMMOBILIZED_LIGHT()
        #    print("triggered immobilized light")
        #elif (received_sig == "3"):
        #    trigger_OUT_OF_ALGAECIDE_LIGHT(True)
        #    print("triggered out of algaecide light")
        #elif (received_sig == "4"):
        #    trigger_OUT_OF_ALGAECIDE_LIGHT(False)
        #    print("Turned algaecide light off")
        # sleep(5)
        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
        # sleep(1)

if __name__ == "__main__":
    main()


# controller in transmit state for 120 s                                            PEAT in receive state for 120 s
# 1. controller transmits signal 40 at end and switches to receive                  2. PEAT receives signal 40 at end and switches to transmit
# 2. controller receives what it needs to and switches from receive to transmit     1. PEAT transmits what it needs to and switches from transmit to receive
# controller in transmit state for 120 s                                            PEAT in receive state for 120 s
