import RPi.GPIO
from utils.communications import *

GPIO.setup(17, INPUT)

def emergency_stop():
    """
    Sends a signal to PEAT to stop all functions
    Reads in the signal from the emergency stop button
    If the button is pressed it will encrypt and send the message to PEAT

    Args:
        None

    Returns:
        None
    """

    # If the button has been pressed
    # Encrypt the word "stop" and send it
    if(GPIO.input(17)):
        signal = encrypt("stop")
        # Send signal
        return signal
