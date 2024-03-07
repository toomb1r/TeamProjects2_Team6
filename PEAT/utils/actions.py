import RPi.GPIO as GPIO

stop = False
# TO FUTURE REGIN:
# Late night Regin wants to test the emergency stop behavior which can be tested now.
# Run code that switches on and off two lights on the controller.
# When the emergency stop button is pressed, turn a boolean to True and go into a while emergency stop boolean is true loop
# Run this loop until emergency stop button's interrupt breaks out of it
# This will turn the emergency stop boolean back off and it will not go into the while loop
def emergency_stop():
    global stop
    stop = not stop
    #boolean
    #if boolean = True
    #while true
    #end