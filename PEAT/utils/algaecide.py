import RPi.GPIO as GPIO
from time import sleep, time

auger_en = 13
auger1 = 1
auger2 = 2
dispenser_en = 14
dispenser1 = 3
dispenser2 = 4
TRIG = 17
ECHO = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(auger1, GPIO.OUT)
GPIO.setup(auger2, GPIO.OUT)
GPIO.setup(dispenser1, GPIO.OUT)
GPIO.setup(dispenser2, GPIO.OUT)

augerpwm=GPIO.PWM(auger_en,1000)
dispenserpwm=GPIO.PWM(dispenser_en,1000)

augerpwm.start(25)
dispenserpwm.start(25)

augerpwm.ChangeDutyCycle(75)
dispenserpwm.ChangeDutyCycle(50)

def ultson_algae():
    """
    Measures algaecide left

    Uses an ultrasonic sensor to measure how much algaecide is left
    Returns the distance from the ultrasonic sensor

    Args:
        None
    Returns:
        distance (int): distance from the ultrasonic sensor
    """
    distance = 0

    print("Distance Measurement In Progress")

    GPIO.output(TRIG, False)
    print("Waiting For Sensor To Settle")
    sleep(2)

    GPIO.output(TRIG, True)
    sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time()
        print("stuck in start")

    while GPIO.input(ECHO) == 1:
        pulse_end = time()
        print("stuck in end")

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150 # speed of sound in air
    # distance = pulse_duration * 75000 # speed of sound in water
    distance = round(distance, 2)
    print(f"Distance: {distance} cm")
    return distance

def detect_out():
    """
    Detects when PEAT is out of algaecide

    Uses an ultrasonic sensor to detect whether it is > 6cm
    If so it returns True

    Args:
        None
    Returns:
        out (boolean): Whether PEAT is out of algaecide
    """
    out = False
    if ultson_algae > 6:
        out = True
        print("Out of algaecide")
    return out

def dispense_algae():
    """
    Starts the dispensing of algaecide

    Turns on the auger and dispenser motors

    Args:
        None
    Returns:
        None
    """
    GPIO.output(auger1, GPIO.HIGH)
    GPIO.output(auger2, GPIO.LOW)
    GPIO.output(dispenser1, GPIO.HIGH)
    GPIO.output(dispenser2, GPIO.LOW)

def stop_dispense():
    """
    Stops the dispensing of algaecide

    Turns off the auger and dispenser motors

    Args:
        None
    Returns:
        None
    """
    GPIO.output(auger1, GPIO.LOW)
    GPIO.output(auger2, GPIO.LOW)
    GPIO.output(dispenser1, GPIO.LOW)
    GPIO.output(dispenser2, GPIO.LOW)

def change_dispense_speed(speed):
    """
    Changes the speed of the dispenser

    Changes the speed of the auger and the dispenser based on the speed argument

    Args:
        speed (double): changes the speed of the auger and dispenser motors
    Returns:
        None
    """
    augerpwm.ChangeDutyCycle(speed)
