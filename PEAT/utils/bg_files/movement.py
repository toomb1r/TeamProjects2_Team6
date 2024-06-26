import random
import RPi.GPIO as GPIO
from time import sleep, time

en = 26
in1 = 22
in2 = 6
turn = 13
TRIGl = 12
ECHOl = 19
TRIGr = 23
ECHOr = 24
GPIO.setup(en, GPIO.OUT)
GPIO.setup(turn, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(TRIGl, GPIO.OUT)
GPIO.setup(ECHOl, GPIO.IN)
GPIO.setup(TRIGr, GPIO.OUT)
GPIO.setup(ECHOr, GPIO.IN)

turnpwm=GPIO.PWM(turn,50)
movepwm=GPIO.PWM(en,1000)
movepwm.start(25)
turnpwm.start(0)

movepwm.ChangeDutyCycle(100)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

def left_dist():
    """
    Returns distance of left ultrasonic sensor.

    Measures the distance in front of the left ultrasonic sensor.
    returns the distance in the form of cms.

    Args:
        None

    Returns:
        distance (float): Distance in front of ultrasonic sensor in cm

    Citation:
        https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
    """

    distance = 0

    GPIO.output(TRIGl, False)
    sleep(0.05)

    GPIO.output(TRIGl, True)
    sleep(0.00001)
    GPIO.output(TRIGl, False)

    while GPIO.input(ECHOl) == 0:
        pulse_start = time()

    while GPIO.input(ECHOl) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # speed of sound in air
    # distance = pulse_duration * 75000 # speed of sound in water
    distance = round(distance, 2)
    return distance

def right_dist():
    """
    Returns distance of right ultrasonic sensor.

    Measures the distance in front of the right ultrasonic sensor.
    returns the distance in the form of cms.

    Args:
        None

    Returns:
        distance (float): Distance in front of ultrasonic sensor in cm

    Citation:
        https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
    """

    distance = 0

    GPIO.output(TRIGr, False)
    sleep(0.05)

    GPIO.output(TRIGr, True)
    sleep(0.00001)
    GPIO.output(TRIGr, False)

    while GPIO.input(ECHOr) == 0:
        pulse_start = time()

    while GPIO.input(ECHOr) == 1:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # speed of sound in air
    # distance = pulse_duration * 75000 # speed of sound in water
    distance = round(distance, 2)
    return distance

def stop():
    """
    Ceases motion for the movement motors.

    Turns off the output for both inputs of the motor, which turns the motor off.

    Args:
        None

    Returns:
        None
    """

    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def start():
    """
    Beings motion for the movement motors.

    Turns on the output for both inputs of the motor, which turns the motor on.

    Args:
        None

    Returns:
        None
    """

    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

def reverse():
    """
    Makes the motor move in reverse.

    Turns on the output for both inputs of the motor in reverse order, which reverses the motor.

    Args:
        None

    Returns:
        None
    """

    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)

def turn_left():
    """
    Turns PEAT to the left.

    Moves the rudder so PEAT can move to the left.

    Args:
        None

    Returns:
        None
    """

    print("turn left")
    reverse()
    sleep(5)
    start()
    turnpwm.ChangeDutyCycle(7.5)
    sleep_time = random.randint(5,10)
    print(f"Sleep time left: {sleep_time}")
    sleep(sleep_time)
    turnpwm.ChangeDutyCycle(5)

def turn_right():
    """
    Turns PEAT to the right.

    Moves the rudder so PEAT can move to the right.

    Args:
        None

    Returns:
        None
    """

    print("turn right")
    reverse()
    sleep(5)
    start()
    turnpwm.ChangeDutyCycle(2.5)
    sleep_time = random.randint(5,10)
    print(f"Sleep time right: {sleep_time}")
    sleep(sleep_time)
    turnpwm.ChangeDutyCycle(5)

def edgeOfPond():
    """
    Turns PEAT if the edge of the pond is detected.

    Determines if the edge of the pond is detected.
    If so, it will turn the boat and move it a constant time.
    After moving this constant time, it will turn back in the direction it came from.

    Args:
        None

    Returns:
        None
    """

    if GPIO.input(in1):
        data = ""

        with open("returntohome.txt", "r") as file:
            data = file.read().strip()
            file.close()

        working = data == "home"
        print(f"working? {working}")

        left = left_dist()
        if(left <= 25 and left > 5):
            if data == "home":
                stop()
            else:
                turn_left()

        right = right_dist()
        if(right <= 25 and right > 5):
            if data == "home":
                stop()
            else:
                turn_right()
