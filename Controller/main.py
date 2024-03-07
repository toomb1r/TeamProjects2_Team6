import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO
from time import sleep

from utils.communications import *
from utils.actions import *

GPIO.setmode(GPIO.BCM)
GPIO.setup(20,GPIO.OUTPUT)
GPIO.add_event_detect(20, GPIO.FALLING, callback=emergency_stop(), bouncetime=100)
def main():
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """
    while True:
        GPIO.output(20, GPIO.HIGH)
        sleep(1)
        GPIO.output(20, GPIO.LOW)
    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)
    # GPIO.add_event_detect(20, GPIO.FALLING, callback=emergencyStop(), bouncetime=100)

if __name__ == "__main__":
    main()
