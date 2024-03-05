import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO as GPIO
from time import sleep

from utils.communications import *

GPIO.setmode(GPIO.BCM)

IMMOBILIZED = 20
OUT_OF_ALGAECIDE = 21
GPIO.setup(IMMOBILIZED, GPIO.OUT)
GPIO.setup(OUT_OF_ALGAECIDE, GPIO.OUT)

SET_HOME_BUTTON = 18
GPIO.setup(SET_HOME_BUTTON, GPIO.IN)
GPIO.setup(SET_HOME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

RETURN_TO_HOME_BUTTON = 14
GPIO.setup(RETURN_TO_HOME_BUTTON, GPIO.IN)
GPIO.setup(RETURN_TO_HOME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

START_STOP_MOVE = 8
GPIO.setup(START_STOP_MOVE, GPIO.IN)
GPIO.setup(START_STOP_MOVE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

START_STOP_DISPENSING = 24
GPIO.setup(START_STOP_DISPENSING, GPIO.IN)
GPIO.setup(START_STOP_DISPENSING, GPIO.IN, pull_up_down=GPIO.PUD_UP)

EMERGENCY_STOP = 15
GPIO.setup(EMERGENCY_STOP, GPIO.IN)
GPIO.setup(EMERGENCY_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DISPENSE_RATE = 23
GPIO.setup(DISPENSE_RATE, GPIO.IN)
GPIO.setup(DISPENSE_RATE, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def set_home_button_pressed_callback(channel):
    print("Set home button pressed!")

def return_to_home_button_pressed_callback(channel):
    print("Return to home button pressed!")

def start_stop_move_button_pressed_callback(channel):
    print("Start/Stop move button pressed!")

def start_stop_dispensing_button_pressed_callback(channel):
    print("Start/Stop dispense button pressed!")

def emergency_stop_button_pressed_callback(channel):
    print("Emergency stop button pressed!")

def dispense_rate_button_pressed_callback(channel):
    print("Dispense rate button pressed!")



def main():
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    GPIO.add_event_detect(SET_HOME_BUTTON, GPIO.FALLING, callback=set_home_button_pressed_callback, bouncetime=200)
    GPIO.add_event_detect(RETURN_TO_HOME_BUTTON, GPIO.FALLING, callback=return_to_home_button_pressed_callback, bouncetime=200)
    # GPIO.add_event_detect(START_STOP_MOVE, GPIO.FALLING, callback=start_stop_move_button_pressed_callback, bouncetime=200)
    GPIO.add_event_detect(START_STOP_DISPENSING, GPIO.FALLING, callback=start_stop_dispensing_button_pressed_callback, bouncetime=200)
    GPIO.add_event_detect(EMERGENCY_STOP, GPIO.FALLING, callback=emergency_stop_button_pressed_callback, bouncetime=200)
    GPIO.add_event_detect(DISPENSE_RATE, GPIO.FALLING, callback=dispense_rate_button_pressed_callback, bouncetime=200)

    while True:
        GPIO.output(IMMOBILIZED, GPIO.HIGH)
        GPIO.output(OUT_OF_ALGAECIDE, GPIO.LOW)
        sleep(1)
        GPIO.output(IMMOBILIZED, GPIO.LOW)
        GPIO.output(OUT_OF_ALGAECIDE, GPIO.HIGH)
        sleep(1)

if __name__ == "__main__":
    main()
