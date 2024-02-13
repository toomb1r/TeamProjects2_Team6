from PEAT.GPS import get_gps_data
import RPi.GPIO as GPIO
import random
import digitalio
import board
import busio
import adafruit_rfm9x
import time
import rsa # pip install rsa
from time import sleep
import csv

GPIO.setmode(GPIO.BOARD)
pwm = GPIO.setup(13, GPIO.OUT)
pwm.start(0)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
pwm_frequency = 50  # Hz
pwm_range_min = 1000  # Microseconds (1 ms)
pwm_range_max = 2000  # Microseconds (2 ms)

random.seed()

def turning(direction):
    """Turns the rudder of PEAT to allow for turning
    Takes the direction from the input and moves the servo motor to there

    Args:
        direction (int): the direction where the rudder will turn (-90 - 90)

    Returns:
        None
    """
    # Move the servo back and forth
    set_angle(direction)    # Move to direction degrees

    # This is untested and probably wont work
    GPIO.output(13, direction)

def set_angle(angle):
    """
    Sets the angle that the servo is at

    Arg: 
        Angle - Int

    Returns:
        None
    """
    # Convert the angle to a duty cycle within the specified range
    duty_cycle = (angle / 120.0) * (pwm_range_max - pwm_range_min) + pwm_range_min
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for the servo to reach the desired position


def edgeOfPond(rorl):
    """Turns PEAT if the edge of the pond is detected
    Determines if the edge of the pond is detected
    If so it will turn the boat and move it a constant time
    After moving this constant time it will turn back in the direction it came from

    Args:
        rorl (bool) - determines the direction PEAT will turn when the edge of the pond is detected

    Returns:
        None
    """
    constant = 20
    
    # If edge of pond detected
    if(GPIO.input(24)):

        # Stop all movement and turn the correct direction
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        if(rorl):
            turning(90)
        else:
            turning(-90)

        # Move for a constant time
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        sleep(constant)

        # Stop all movement and turn the correct direction
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        if(rorl):
            turning(90)
        else:
            turning(-90)

        # Change the turning direction unless the edge of pond is still in front of PEAT
        rorl = not rorl
        if(GPIO.input(24)):
            rorl = not rorl

        # Check if the edge of pond is still in front of PEAT
        edgeOfPond()

def move():
    """Begins the movement of the rudder of PEAT
    Selects a random direction and moves there

    Args:
        None

    Returns:
        None
    """
    turning(random.randrange(0, 120))
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)
    pwm.stop() # comment out later?

# Im pretty sure this is needed although I need to figure out how to add it in
# GPIO.cleanup()

def encrypt(msg):
    """Encrypts a message using the controller's public key
    Gets the RSA public key of the controller. Encodes the message in UTF-8 and encrypts it.
    Returns the encrypted message.

    Args:
        msg (str): The message to be encrypted

    Returns:
        bytes: The encrypted message
    """

    # `ssh-keygen` to generate RSA key pairs
    # `ssh-keygen -f /path/to/your/public-key -e -m pem > /path/to/your/public-key{.pem}`
    # to convert the public key into pem format
    fkey = open('/Users/anmolsaini/.ssh/controller.pub.pem','rb') # modify path
    public_key = rsa.PublicKey.load_pkcs1(fkey.read())
    encoded_msg = msg.encode('utf8')
    encrypted_msg = rsa.encrypt(encoded_msg, public_key)
    return encrypted_msg

def decrypt(encrypted_msg):
    """Decrypts a message using PEAT's private key
    Gets the RSA private key of PEAT. Decrypts the message and decodes it from UTF-8.
    Returns the decrypted message.

    Args:
        encrypted_msg (bytes): The message to be decrypted

    Returns:
        str: The decrypted message
    """

    # `ssh-keygen -p -m PEM -f /path/to/your/private-key` to convert the private key into pem format
    fkey = open('/Users/anmolsaini/.ssh/peat', 'rb') # modify path
    private_key = rsa.PrivateKey.load_pkcs1(fkey.read())
    decrypted_msg = rsa.decrypt(encrypted_msg, private_key)
    decoded_msg = decrypted_msg.decode('utf8')
    return decoded_msg

def main():
    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)
    home_csv_path = get_gps_data()

    # This is to start the servo motor in the center of the 180 degrees
    # To allow -90 and 90 degrees of motion
    turning(90)

    move()
    rorl = True
    while(True):
        edgeOfPond(rorl)
        move()

if __name__ == "__main__":
    main()


