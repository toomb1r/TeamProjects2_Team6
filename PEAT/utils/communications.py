import rsa # pip install rsa

import time
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
#     # from digitalio import DigitalInOut, Direction, Pull
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
#             time.sleep(1)

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
#         time.sleep(0.1)

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
