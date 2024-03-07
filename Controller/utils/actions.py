import RPi.GPIO as GPIO
from utils.communications import *
from time import sleep

GPIO.setmode(GPIO.BCM)
# GPIO.setup(20, GPIO.OUTPUT)
GPIO.setup(21, GPIO.OUTPUT)

stop = False

def emergency_stop():
    global stop

    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.HIGH)
    stop = not stop
    if stop:
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.HIGH)
        while True:
            sleep(1)
    else:
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
    # """
    # Sends a signal to PEAT to stop all functions
    # Reads in the signal from the emergency stop button
    # If the button is pressed it will encrypt and send the message to PEAT

    # Args:
    #     None

    # Returns:
    #     None
    # """

    # # If the button has been pressed
    # # Encrypt the word "stop" and send it
    # if(GPIO.input(17)):
    #     signal = encrypt("stop")
    #     # Send signal
    #     return signal
