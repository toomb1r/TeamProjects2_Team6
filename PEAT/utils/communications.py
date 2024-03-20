import rsa # pip install rsa

# import time
import busio
from digitalio import DigitalInOut
import board
import adafruit_rfm9x
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

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
    fkey = open('/home/PEAT/.ssh/controller.pub.pem','rb')
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
    fkey = open('/home/PEAT/.ssh/peat', 'rb')
    private_key = rsa.PrivateKey.load_pkcs1(fkey.read())
    decrypted_msg = rsa.decrypt(encrypted_msg, private_key)
    decoded_msg = decrypted_msg.decode('utf8')
    return decoded_msg

def emergency_stop(stop):
    """
    Takes in a boolean variable to return the opposite

    Args:
        stop (bool): variable to stop all functionality

    Returns:
        stop (bool): variable to stop all functionality
    """
    return not stop

def transmit(signal):
    """Transmits a signal using the transciever
    Converts a signal into bytes and transmits it 3 times (to ensure receipt)

    Args:
        signal (Any): The signal to be sent

    Returns:
        None
    """

    # Configure LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.tx_power = 23
    num_sends = 0

    while num_sends <= 2:
        data = bytes(f"{signal}\r\n","utf-8")
        rfm9x.send(data)
        num_sends+=1

def receive():
    """Receives a signal using the transciever
    Listens for a signal until one is recieved. Converts this signal into a string.
    Returns this string signal to the calling method

    Args:
        None

    Returns:
        packet_text (string): The data received
    """

    # Configure LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.tx_power = 23
    prev_packet = None

    while True:
        packet = rfm9x.receive()
        if packet is None:
            print("packet = None")
        else:
            prev_packet = packet
            packet_text = str(prev_packet, "utf-8")
            print(f"packet = {packet_text}")
            return packet_text
