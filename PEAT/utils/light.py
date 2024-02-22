import RPi.GPIO as GPIO
import time
#https://robocraze.com/blogs/post/turning-on-an-led-with-your-raspberry-pi-s-gpio-pins 
# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# GPIO pin number
gpio_pin = 13
GPIO.setup(gpio_pin, GPIO.OUT)

def turnOnLight():
    # Setup the GPIO pin as output


    # Turn on the light
    GPIO.output(gpio_pin, GPIO.HIGH)
    print("Light is ON")

    # Wait for some time
    time.sleep(1)  # Adjust the time as needed



def turnOffLight():
    GPIO.output(gpio_pin, GPIO.LOW)
    print("Light is OFF")
