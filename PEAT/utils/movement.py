import RPi.GPIO as GPIO

en = 26
in1 = 22
in2 = 6
turn = 13
TRIGl = 12
ECHOl = 19
TRIGr = 23
ECHOr = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(en, GPIO.OUT)
GPIO.setup(turn, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(TRIGl, GPIO.OUT)
GPIO.setup(ECHOl, GPIO.IN)
GPIO.setup(TRIGr, GPIO.OUT)
GPIO.setup(ECHOr, GPIO.IN)

movepwm=GPIO.PWM(en,1000)
movepwm.start(25)

movepwm.ChangeDutyCycle(100)

def stop():
    """
    Turns off movement motors.

    Turns off the output for both inputs of the motor, which turns the motor off.

    Args:
        None

    Returns:
        None
    """

    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)

def start_up():
    """
    Turns on movement motors.

    Turns on the output for both inputs of the motor, which turns the motor on and stops return to home functionality.

    Args:
        None

    Returns:
        None
    """

    with open("returntohome.txt", "w") as file:
        file.write("notStopped")
        file.close()

    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)

def start():
    """
    Turns on movement motors.

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

def return_to_home():
    """
    Turns on return to home functionality.

    Writes to the returntohome.txt file to allow PEAT to use return to home functionality.

    Args:
        None

    Returns:
        None
    """

    with open("returntohome.txt", "w") as file:
        file.write("home")
        file.close()
        print(f"Returning to home")
