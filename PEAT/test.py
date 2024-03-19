import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
import utils.pins as pin
auger_en = pin.get_auger_en()
auger_in1 = pin.get_auger_in1()
auger_in2 = pin.get_auger_in2()

pwm = GPIO.PWM(auger_en,1000)
pwm.start(25)

pwm.ChangeDutyCycle(75)
GPIO.output(auger_in1, GPIO.HIGH)
GPIO.output(auger_in2, GPIO.LOW)
sleep(1)
GPIO.output(auger_in1, GPIO.LOW)
GPIO.output(auger_in2, GPIO.LOW)
GPIO.cleanup()
