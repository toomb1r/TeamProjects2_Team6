import RPi.GPIO
import digitalio
import board
import busio
import adafruit_rfm9x
import signal
import sys
import rsa

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

def encrypt(msg):
    """Encrypts a message using PEAT's public key
    Gets the RSA public key of PEAT. Encodes the message in UTF-8 and encrypts it.
    Returns the encrypted message.

    Args:
        msg (str): The message to be encrypted

    Returns:
        bytes: The encrypted message
    """

    # `ssh-keygen` to generate RSA key pairs
    # `ssh-keygen -f /path/to/your/public-key -e -m pem > /path/to/your/public-key{.pem}`
    # to convert the public key into pem format
    fkey = open('/Users/anmolsaini/.ssh/peat.pub.pem','rb') # modify path
    public_key = rsa.PublicKey.load_pkcs1(fkey.read())
    encoded_msg = msg.encode('utf8')
    encrypted_msg = rsa.encrypt(encoded_msg, public_key)
    return encrypted_msg

def decrypt(encrypted_msg):
    """Decrypts a message using the controller's private key
    Gets the RSA private key of the controller. Decrypts the message and decodes it from UTF-8.
    Returns the decrypted message.

    Args:
        encrypted_msg (bytes): The message to be decrypted

    Returns:
        str: The decrypted message
    """

    # `ssh-keygen -p -m PEM -f /path/to/your/private-key` to convert the private key into pem format
    fkey = open('/Users/anmolsaini/.ssh/controller', 'rb') # modify path
    private_key = rsa.PrivateKey.load_pkcs1(fkey.read())
    decrypted_msg = rsa.decrypt(encrypted_msg, private_key)
    decoded_msg = decrypted_msg.decode('utf8')
    return decoded_msg

def main():
    enc_msg = encrypt("this is encrypted")
    dec_msg = decrypt(enc_msg)

    # This handles CTRL+C stuff and signal.pause pauses the main method (think while(true) loop)
    signal.signal(signal.SIGINT, signal_handler)
    # This only exists in unix
    signal.pause()

if __name__ == "__main__":
    main()
