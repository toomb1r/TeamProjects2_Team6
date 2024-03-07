import RPi.GPIO as GPIO
auger_en = 13
auger1 = 1
auger2 = 2
dispenser_en = 14
dispenser1 = 3
dispenser2 = 4

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
dispenserpwm.ChangeDutyCycle(75)

def dispense_algae():
    """
    Starts the dispensing of algaecide
    
    Turns on the auger and dispenser motor

    Args:
        None
    Returns:
        None
    """
    GPIO.output(auger1, GPIO.HIGH)
    GPIO.output(auger2, GPIO.LOW)
    GPIO.output(dispenser1, GPIO.HIGH)
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
    dispenserpwm.ChangeDutyCycle(speed)