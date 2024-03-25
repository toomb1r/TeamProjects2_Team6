import RPi.GPIO as GPIO
from utils.communications import *
from time import sleep

GPIO.setmode(GPIO.BCM)
#GPIO.setup(20, GPIO.OUT)
#GPIO.setup(21, GPIO.OUT)
#GPIO.setup(15, GPIO.IN)
#GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#stop = False

#def emergency_stop(channel):
 #   global stop

  #  GPIO.output(20, GPIO.HIGH)
   # GPIO.output(21, GPIO.HIGH)
    #stop = not stop
#    if stop:
 #       GPIO.output(20, GPIO.HIGH)
  #      GPIO.output(21, GPIO.HIGH)
   #     while True:
    #        print("hello")
     #       sleep(1)
#    else:
 #       GPIO.output(20, GPIO.LOW)
  #      GPIO.output(21, GPIO.LOW)
   #     print("exit")
    # """
    # Sends a signal to PEAT to stop all functions
    # Reads in the signal from the emergency stop button
    # If the button is pressed it will encrypt and send the message to PEAT

    # Args:
    #     None

    # Returns:
    #     None
    # """

    # # If the button has been pressed
    # # Encrypt the word "stop" and send it
    # if(GPIO.input(17)):
    #     signal = encrypt("stop")
    #     # Send signal
    #     return signal
GPIO.add_event_detect(15,GPIO.FALLING,callback=emergency_stop,bouncetime=200)
