import random
import RPi.GPIO as GPIO
from time import sleep, time

# random.seed()

GPIO.setmode(GPIO.BCM)
# GPIO.setup(13, GPIO.OUT)
# GPIO.setup(20, GPIO.OUT)
# GPIO.setup(21, GPIO.OUT)
# GPIO.setup(24, GPIO.IN)

TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# def turning(direction):
#     """Turns the rudder of PEAT to allow for turning
#     Takes the direction from the input and moves the servo motor to there

#     Args:
#         direction (int): the direction where the rudder will turn (-90 - 90)

#     Returns:
#         None
#     """
#     # This is untested and probably wont work
#     GPIO.output(13, direction)

# def edgeOfPond(rorl):
#     """Turns PEAT if the edge of the pond is detected
#     Determines if the edge of the pond is detected
#     If so it will turn the boat and move it a constant time
#     After moving this constant time it will turn back in the direction it came from

#     Args:
#         rorl (bool) - determines the direction PEAT will turn when the edge of the pond is detected

#     Returns:
#         None
#     """
#     constant = 20

#     # If edge of pond detected
#     if(GPIO.input(24)):

#         # Stop all movement and turn the correct direction
#         GPIO.output(20, GPIO.LOW)
#         GPIO.output(21, GPIO.LOW)
#         if(rorl):
#             turning(90)
#         else:
#             turning(-90)

#         # Move for a constant time
#         GPIO.output(20, GPIO.HIGH)
#         GPIO.output(21, GPIO.LOW)
#         sleep(constant)

#         # Stop all movement and turn the correct direction
#         GPIO.output(20, GPIO.LOW)
#         GPIO.output(21, GPIO.LOW)
#         if(rorl):
#             turning(90)
#         else:
#             turning(-90)

#         # Change the turning direction unless the edge of pond is still in front of PEAT
#         rorl = not rorl
#         if(GPIO.input(24)):
#             rorl = not rorl

#         # Check if the edge of pond is still in front of PEAT
#         edgeOfPond()

# def move():
#     """Begins the movement of the rudder of PEAT
#     Selects a random direction and moves there

#     Args:
#         None

#     Returns:
#         None
#     """
#     turning(random.randrange(-90, 90))
#     GPIO.output(20, GPIO.HIGH)
#     GPIO.output(21, GPIO.LOW)

# Im pretty sure this is needed although I need to figure out how to add it in
# GPIO.cleanup()

# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi
def detect_dist():
    """
    """
    
    # import RPi.GPIO as GPIO
    # import time
    # GPIO.setmode(GPIO.BCM)

    # TRIG = 23
    # ECHO = 24

    print("Distance Measurement In Progress")

    # GPIO.setup(TRIG, GPIO.OUT)
    # GPIO.setup(ECHO, GPIO.IN)

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
    GPIO.cleanup()
    return distance
