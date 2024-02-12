import RPi.GPIO
import digitalio
import board
import busio
import adafruit_rfm9x
import rsa

GPIO.setmode(GPIO.BOARD)
GPIO.setup(17, INPUT)

def emergencyStop():
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
    GPIO.add_event_detect(17, GPIO.FALLING, callback=emergencyStop(), bouncetime=100)

if __name__ == "__main__":
    main()
