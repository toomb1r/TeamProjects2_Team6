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
OUT_OF_ALGAECIDE_LIGHT = 20 # signal 3/4
GPIO.setup(IMMOBILIZED_LIGHT, GPIO.OUT)
GPIO.setup(OUT_OF_ALGAECIDE_LIGHT, GPIO.OUT)

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

# def transmit_and_receive():
#     # SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
#     #
#     # SPDX-License-Identifier: MIT

#     """
#     Example for using the RFM9x Radio with Raspberry Pi.

#     Learn Guide: https://learn.adafruit.com/lora-and-lorawan-for-raspberry-pi
#     Author: Brent Rubell for Adafruit Industries
#     """
#     # # Import Python System Libraries
#     # import time
#     # # Import Blinka Libraries
#     # import busio
#     # from digitalio import DigitalInOut
#     # import board
#     # # Import the SSD1306 module.
#     # # import adafruit_ssd1306
#     # # Import RFM9x
#     # import adafruit_rfm9x

#     # # Button A
#     # btnA = DigitalInOut(board.D5)
#     # btnA.direction = Direction.INPUT
#     # btnA.pull = Pull.UP

#     # # Button B
#     # btnB = DigitalInOut(board.D6)
#     # btnB.direction = Direction.INPUT
#     # btnB.pull = Pull.UP

#     # # Button C
#     # btnC = DigitalInOut(board.D12)
#     # btnC.direction = Direction.INPUT
#     # btnC.pull = Pull.UP

#     # Create the I2C interface.
#     # i2c = busio.I2C(board.SCL, board.SDA)

#     # # 128x32 OLED Display
#     # reset_pin = DigitalInOut(board.D4)
#     # display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
#     # # Clear the display.
#     # display.fill(0)
#     # display.show()
#     # width = display.width
#     # height = display.height

#     # Configure LoRa Radio
#     CS = DigitalInOut(board.CE1)
#     RESET = DigitalInOut(board.D25)
#     spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
#     rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
#     rfm9x.tx_power = 23
#     prev_packet = None

#     while True:
#         packet = None
#         # draw a box to clear the image
#         # display.fill(0)
#         # display.text('RasPi LoRa', 35, 0, 1)

#         # check for packet rx
#         packet = rfm9x.receive()
#         if packet is None:
#             # display.show()
#             # display.text('- Waiting for PKT -', 15, 20, 1)
#             print("packet = None")
#         else:
#             # Display the packet text and rssi
#             # display.fill(0)
#             prev_packet = packet
#             packet_text = str(prev_packet, "utf-8")
#             # display.text('RX: ', 0, 0, 1)
#             # display.text(packet_text, 25, 0, 1)
#             print(f"packet = {packet_text}")
#             sleep(1)

#         # if not btnA.value:
#         #     # Send Button A
#         #     display.fill(0)
#         data = bytes("This is data!\r\n","utf-8")
#         rfm9x.send(data)
#         #     display.text('Sent Button A!', 25, 15, 1)
#         # elif not btnB.value:
#         #     # Send Button B
#         #     display.fill(0)
#         #     button_b_data = bytes("Button B!\r\n","utf-8")
#         #     rfm9x.send(button_b_data)
#         #     display.text('Sent Button B!', 25, 15, 1)
#         # elif not btnC.value:
#         #     # Send Button C
#         #     display.fill(0)
#         #     button_c_data = bytes("Button C!\r\n","utf-8")
#         #     rfm9x.send(button_c_data)
#         #     display.text('Sent Button C!', 25, 15, 1)


#         # display.show()
#         sleep(0.1)

def transmit(signal):
    # Configure LoRa Radio
    CS = DigitalInOut(board.CE1)
    RESET = DigitalInOut(board.D25)
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0)
    rfm9x.tx_power = 23
    num_sends = 0

    while num_sends <= 2:
        # data = encrypt("This is data")
        # data = bytes("This is data!\r\n","utf-8")
        data = bytes(f"{signal}\r\n","utf-8")
        # data = bytes("ejiinjaewfiaefiafewihefwahieafwhiefwhifaewhaewhfhbwaefhifaeifaewhefhwabfbahwhabfwefbheiawehwbawfbfbhewafhbfeijafeaijnefwfaehaefwhjaefwjaefwbhjiwaefbhijefwijnwehbjewfakejiwafnjifjnkfwjknfeqwnbjkefqwjknefwqbhjkewjnbkewnjkaefwbnjkewnjjknewrajkbhjkjnkefw\r\n","utf-8")
        rfm9x.send(data)
        num_sends+=1

def receive():
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
            # packet_text = decrypt(prev_packet)
            packet_text = str(prev_packet, "utf-8")
            print(f"packet = {packet_text}")
            return packet_text
            # time.sleep(1)

def trigger_IMMOBILIZED_LIGHT():
    if GPIO.input(IMMOBILIZED_LIGHT):
        GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
    else:
        GPIO.output(IMMOBILIZED_LIGHT, GPIO.HIGH)

def trigger_OUT_OF_ALGAECIDE_LIGHT():
    if GPIO.input(OUT_OF_ALGAECIDE_LIGHT):
        GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.LOW)
    else:
        GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.HIGH)

def set_home_button_pressed_callback(channel):
    #print("Set home button pressed!")
    transmit("5")

def return_to_home_button_pressed_callback(channel):
    #print("Return to home button pressed!")
    transmit("7")

def START_STOP_MOVE_BUTTON_button_pressed_callback(channel):
    #print("Start/Stop move button pressed!")
    transmit("9")

def START_STOP_DISPENSING_BUTTON_button_pressed_callback(channel):
    #print("Start/Stop dispense button pressed!")
    transmit("11")

def EMERGENCY_STOP_BUTTON_button_pressed_callback(channel):
    #print("Emergency stop button pressed!")
    transmit("13")

def DISPENSE_RATE_POTENTIOMETER_button_pressed_callback(channel):
    # Initialize the I2C interface
    i2c = busio.I2C(board.SCL, board.SDA)
    # Create an  ADS1115 object
    ads = ADS.ADS1115(i2c)
    # Define the analog input channel
    cur_channel = AnalogIn(ads, ADS.P0)

    #print("Dispense rate button pressed!")
    # 0.0 - 0.33; 1
    # 0.33 - 0.66; 2
    # 0.66 - 0.99; 3
    # 0.99 - 1.32; 4
    # 1.32 - 1.65; 5
    # 1.65 - 1.98; 6
    # 1.98 - 2.31; 7
    # 2.31 - 2.64; 8
    # 2.64 - 2.97; 9
    # 2.97 - 3.30; 10

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
            transmit(cur_setting_sig)
            break

GPIO.add_event_detect(SET_HOME_BUTTON, GPIO.FALLING, callback=set_home_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(RETURN_TO_HOME_BUTTON, GPIO.FALLING, callback=return_to_home_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(START_STOP_MOVE_BUTTON, GPIO.FALLING, callback=START_STOP_MOVE_BUTTON_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(START_STOP_DISPENSING_BUTTON, GPIO.FALLING, callback=START_STOP_DISPENSING_BUTTON_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(EMERGENCY_STOP_BUTTON, GPIO.FALLING, callback=EMERGENCY_STOP_BUTTON_button_pressed_callback, bouncetime=200)
GPIO.add_event_detect(DISPENSE_RATE_POTENTIOMETER, GPIO.FALLING, callback=DISPENSE_RATE_POTENTIOMETER_button_pressed_callback, bouncetime=200)

    # while True:
    #     GPIO.output(IMMOBILIZED_LIGHT, GPIO.HIGH)
    #     GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.LOW)
    #     sleep(1)
    #     GPIO.output(IMMOBILIZED_LIGHT, GPIO.LOW)
    #     GPIO.output(OUT_OF_ALGAECIDE_LIGHT, GPIO.HIGH)
    #     sleep(1)

    #     print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
    #     sleep(0.2)