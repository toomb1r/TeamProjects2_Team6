import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)

pin = 11
pwm=GPIO.PWM(pin,50)
pwm.start(0)

pwm.ChangeDutyCycle(5)
sleep(1)
pwm.ChangeDutyCycle(7.5)
sleep(1)
pwm.ChangeDutyCycle(10)
sleep(1)

pwm.stop()
GPIO.cleanup()
#def SetAngle(angle):
#	duty = angle / 18 +2
#	GPIO.output(pin, True)
#	pwm.ChangeDutyCycle(duty)
#	sleep(5)
#	GPIO.output(pin, False)
#	pwm.ChangeDutyCycle(0)

#SetAngle(45)
#pwm.stop()
#GPIO.cleanup()
