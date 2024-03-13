import random
import RPi.GPIO as GPIO
from time import sleep

random.seed()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

def detect_movement():
    # This function detects movement using move func
    # It returns True if movement is detected, False otherwise

    # Perform the movement logi
    move()
    
    time.sleep(5)  # Assuming the robot moves for 5 seconds
    
    # Stop the movement
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)

    # Assuming movement is detected if it reached this point
    return True

# talk to the dudes and see where this logic could go
# try:
#     start_time = time.time()
#     while True:
#         # Check for movement every second
#         movement_detected = detect_movement()
#         print("Movement Detected:", movement_detected)
        
#         # If no movement is detected and 3 minutes have passed, immobilize the robot
#         if not movement_detected and (time.time() - start_time) > 180:
#             print("Robot immobilized.")
#             # Add code here to stop the robot or trigger an immobilization mechanism
#             break
        
#         time.sleep(1)

# except KeyboardInterrupt:
#     GPIO.cleanup()

def turning(direction):
    """Turns the rudder of PEAT to allow for turning
    Takes the direction from the input and moves the servo motor to there

    Args:
        direction (int): the direction where the rudder will turn (-90 - 90)

    Returns:
        None
    """
    # This is untested and probably wont work
    GPIO.output(13, direction)

def edgeOfPond(rorl):
    """Turns PEAT if the edge of the pond is detected
    Determines if the edge of the pond is detected
    If so it will turn the boat and move it a constant time
    After moving this constant time it will turn back in the direction it came from

    Args:
        rorl (bool) - determines the direction PEAT will turn when the edge of the pond is detected

    Returns:
        None
    """
    constant = 20
    
    # If edge of pond detected
    if(GPIO.input(24)):

        # Stop all movement and turn the correct direction
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        if(rorl):
            turning(90)
        else:
            turning(-90)

        # Move for a constant time
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        sleep(constant)

        # Stop all movement and turn the correct direction
        GPIO.output(20, GPIO.LOW)
        GPIO.output(21, GPIO.LOW)
        if(rorl):
            turning(90)
        else:
            turning(-90)

        # Change the turning direction unless the edge of pond is still in front of PEAT
        rorl = not rorl
        if(GPIO.input(24)):
            rorl = not rorl

        # Check if the edge of pond is still in front of PEAT
        edgeOfPond()

def move():
    """Begins the movement of the rudder of PEAT
    Selects a random direction and moves there

    Args:
        None

    Returns:
        None
    """
    turning(random.randrange(-90, 90))
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)

# Im pretty sure this is needed although I need to figure out how to add it in
# GPIO.cleanup()
