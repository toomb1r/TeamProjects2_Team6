import adafruit_rfm9x
import board
import busio
import digitalio
import RPi.GPIO

from utils.communications import *

def main():
    """Executes the main functionality of the Controller

    Args: None

    Returns: None
    """

    # enc_msg = encrypt("this is encrypted")
    # dec_msg = decrypt(enc_msg)

    transmit("hi")
    # receive()

    #transmit_and_receive()

    while True:
        GPIO.output(IMMOBILIZED_LIGHT, GPIO.HIGH)
        GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.LOW)
        sleep(1)
        GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
        GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.HIGH)
        sleep(1)

        # print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
        # sleep(0.2)

if __name__ == "__main__":
    main()
