import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO as GPIO

from time import sleep

from utils.communications import *

GPIO.setmode(GPIO.BCM)

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

    while True:
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
        received_sig = receive().strip()
        if (received_sig == "1"):
            trigger_IMMOBILIZED_LIGHT()
            print("triggered immobilized light")
        elif (received_sig == "3"):
            trigger_OUT_OF_ALGAECIDE_LIGHT()
            print("triggered out of algaecide light")
        # sleep(5)
        # GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
        # sleep(1)


if __name__ == "__main__":
    main()
