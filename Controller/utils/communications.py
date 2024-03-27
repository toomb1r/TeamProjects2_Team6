import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_rfm9x
import board
import busio
from digitalio import DigitalInOut
import rsa # pip install rsa
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

IMMOBILIZED_LIGHT = 21 # signal 1/2
GPIO.setup(IMMOBILIZED_LIGHT, GPIO.OUT)
GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)

OUT_OF_ALGAECIDE_LIGHT = 20 # signal 3/4
GPIO.setup(OUT_OF_ALGAECIDE_LIGHT, GPIO.OUT)
GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.LOW)

SET_HOME_BUTTON = 18 # signal 5/6
GPIO.setup(SET_HOME_BUTTON, GPIO.IN)
GPIO.setup(SET_HOME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

RETURN_TO_HOME_BUTTON = 14 # signal 7/8
GPIO.setup(RETURN_TO_HOME_BUTTON, GPIO.IN)
GPIO.setup(RETURN_TO_HOME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

START_STOP_MOVE_BUTTON = 16 # signal 9/10
GPIO.setup(START_STOP_MOVE_BUTTON, GPIO.IN)
GPIO.setup(START_STOP_MOVE_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

START_STOP_DISPENSING_BUTTON = 24 # signal 11/12
GPIO.setup(START_STOP_DISPENSING_BUTTON, GPIO.IN)
GPIO.setup(START_STOP_DISPENSING_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

EMERGENCY_STOP_BUTTON = 15 # signal 13/14
GPIO.setup(EMERGENCY_STOP_BUTTON, GPIO.IN)
GPIO.setup(EMERGENCY_STOP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DISPENSE_RATE_POTENTIOMETER = 23
GPIO.setup(DISPENSE_RATE_POTENTIOMETER, GPIO.IN)
GPIO.setup(DISPENSE_RATE_POTENTIOMETER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
# Create an  ADS1115 object
ads = ADS.ADS1115(i2c)
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)

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
    fkey = open('/home/Controller/.ssh/peat.pub.pem','rb')
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
    fkey = open('/home/Controller/.ssh/controller', 'rb')
    private_key = rsa.PrivateKey.load_pkcs1(fkey.read())
    decrypted_msg = rsa.decrypt(encrypted_msg, private_key)
    decoded_msg = decrypted_msg.decode('utf8')
    return decoded_msg

def transmit(signal):
    """Transmits a signal using the transciever
    Converts a signal into bytes. Transmits this signal 3 times (to ensure receipt).

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
    #num_sends = 0

    data = encrypt(signal)
    # https://www.geeksforgeeks.org/python-split-string-in-groups-of-n-consecutive-characters/
    data_list = [(data[i:i+200]) for i in range(0, len(data), 200)]
    # data_list[-1] = data_list[-1] + "\n"
    data_list.append(b"\n")
    #print(data_list)
    for seg in data_list:
        num_sends = 0
        print(f"{seg} Numsends: {num_sends}\n")
        while num_sends <= 5:
            # print("hi")
            # data = bytes(f"{signal}\r\n","utf-8")
            # rfm9x.send(data)
            rfm9x.send(seg)
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

def trigger_IMMOBILIZED_LIGHT():
    """Triggers light signaling immobilized status
    Turns the immobilized light on if it is off.
    Turns the immobilized light off if it is on.

    Args:
        None

    Returns:
        None
    """

    if GPIO.input(IMMOBILIZED_LIGHT):
        GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
    else:
        GPIO.output(IMMOBILIZED_LIGHT, GPIO.HIGH)

def trigger_OUT_OF_ALGAECIDE_LIGHT():
    """Triggers light signaling out of algaecide status
    Turns the out of algaecide light on if it is off.
    Turns the out of algaecide light off if it is on.

    Args:
        None

    Returns:
        None
    """

    if GPIO.input(OUT_OF_ALGAECIDE_LIGHT):
        GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.LOW)
    else:
        GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.HIGH)

def SET_HOME_BUTTON_pressed_callback(channel):
    """Callback for the set home button
    Transmits a signal to trigger PEAT's set home point functionality

    Args:
        None

    Returns:
        None
    """

    transmit("5")

def RETURN_TO_HOME_BUTTON_pressed_callback(channel):
    """Callback for the return to home button
    Transmits a signal to trigger PEAT'S return to home functionality

    Args:
        None

    Returns:
        None
    """

    transmit("7")

def START_STOP_MOVE_BUTTON_pressed_callback(channel):
    """Callback for the start and stop move button
    Transmits a signal to trigger PEAT's start and stop movement functionality

    Args:
        None
    
    Returns:
        None
    """

    transmit("9")

def START_STOP_DISPENSING_BUTTON_pressed_callback(channel):
    """Callback for the start and stop algaecide dispensing button
    Transmits a signal to trigger PEAT's start and stop dispensing functionality

    Args:
        None
    
    Returns:
        None
    """

    transmit("11")

def EMERGENCY_STOP_BUTTON_pressed_callback(channel):
    """Callback for the emergency stop button
    Transmits a signal to trigger PEAT's emergency stop functionality

    Args:
        None

    Returns:
        None
    """

    transmit("13")

def DISPENSE_RATE_POTENTIOMETER_button_pressed_callback(channel):
    """Callback for the button setting the algaecide dispensing rate
    Divides the max voltage into 10 distinct dispense rate settings.
    Determines the setting corresponding to the current measured voltage.
    Determines the signal to be sent based on this setting.
    Transmits this signal.

    Args:
        channel:

    Returns:
        None
    """
    
    # Initialize the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create an  ADS1115 object
    ads = ADS.ADS1115(i2c)
    # Define the analog input channel
    cur_channel = AnalogIn(ads, ADS.P0)

    max_voltage = 3.3
    num_settings = 10
    voltage_boundary = max_voltage / num_settings
    cur_voltage = cur_channel.voltage
    cur_setting = 1
    cur_voltage_setting_boundary = voltage_boundary

    while True:
        if cur_voltage_setting_boundary < cur_voltage:
            cur_voltage_setting_boundary += voltage_boundary
            cur_setting += 1
        else:
            cur_setting_sig = cur_setting + 20
            transmit(str(cur_setting_sig))
            break

GPIO.add_event_detect(SET_HOME_BUTTON, GPIO.FALLING, callback=SET_HOME_BUTTON_pressed_callback, bouncetime=8000)
GPIO.add_event_detect(RETURN_TO_HOME_BUTTON, GPIO.FALLING, callback=RETURN_TO_HOME_BUTTON_pressed_callback, bouncetime=8000)
GPIO.add_event_detect(START_STOP_MOVE_BUTTON, GPIO.FALLING, callback=START_STOP_MOVE_BUTTON_pressed_callback, bouncetime=8000)
GPIO.add_event_detect(START_STOP_DISPENSING_BUTTON, GPIO.FALLING, callback=START_STOP_DISPENSING_BUTTON_pressed_callback, bouncetime=8000)
GPIO.add_event_detect(EMERGENCY_STOP_BUTTON, GPIO.FALLING, callback=EMERGENCY_STOP_BUTTON_pressed_callback, bouncetime=8000)
GPIO.add_event_detect(DISPENSE_RATE_POTENTIOMETER, GPIO.FALLING, callback=DISPENSE_RATE_POTENTIOMETER_button_pressed_callback, bouncetime=8000)
