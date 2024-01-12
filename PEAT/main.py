from gps3 import gps3
import RPi.GPIO
import random
import digitalio
import board
import busio
import adafruit_rfm9x

def move():
    return random.randrange(-90, 90)

print("hello world")
random.seed()
direction = move()

print(direction)
