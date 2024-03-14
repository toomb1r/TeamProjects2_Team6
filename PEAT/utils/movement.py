import random
import RPi.GPIO as GPIO
from time import sleep
from gps3 import gps3

random.seed()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(24, GPIO.IN)

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

def get_gps_data():
    """Gets coordinates at the time of function call.
    Get GPS data from GPS3 socket. 
    It then stores it in a Data stream. 
    After error checking it writes at time coordinates to a CSV file.

    Args: 
        none

    Returns: 
        csv_file_path (string) - file path to the csv 
    """
    #connection to the socket
    gpsd_connection = gps3.GPSDSocket()
    #streaming data from socket
    data_stream = gps3.DataStream()

    csv_file_path = 'gps_data.csv'

    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = ['Latitude', 'Longitude']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            csv_writer.writeheader()

            for new_data in gpsd_connection:
                if new_data:
                    # Parse new GPS data
                    data_stream.unpack(new_data)
                    # Check if GPS data is valid
                    if data_stream.TPV['lat'] and data_stream.TPV['lon']:
                        latitude = data_stream.TPV['lat']
                        longitude = data_stream.TPV['lon']

                        # Write data to CSV file
                        csv_writer.writerow({'Latitude': latitude, 'Longitude': longitude})

                        print(f"Latitude: {latitude}, Longitude: {longitude}")
                # Wait for 1 second
                sleep(1)
    finally:
        return csv_file_path

