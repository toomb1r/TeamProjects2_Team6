import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO as GPIO
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

def main():
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)
    while True:
        print(f"main {stop}")
        if not stop:
            GPIO.output(20, GPIO.HIGH)
            sleep(1)
            GPIO.output(20, GPIO.LOW)
            #print(f"main {stop}")
            sleep(1)
    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)
    # GPIO.add_event_detect(20, GPIO.FALLING, callback=emergencyStop(), bouncetime=100)

if __name__ == "__main__":
    main()
