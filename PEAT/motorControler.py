import RPi.GPIO as GPIO          
from time import sleep

in1 = 17
in2 = 27
butt = 21
en = 4
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

stopped = False
def stop(channel):
	global stopped
	if not stopped:
		GPIO.output(in1,GPIO.LOW)
		GPIO.output(in2,GPIO.LOW)
		stopped = True
	else:
		GPIO.output(in1,GPIO.HIGH)
		GPIO.output(in2,GPIO.LOW)
		stopped = False
GPIO.add_event_detect(21,GPIO.FALLING,callback=stop,bouncetime=200)

while(1):

    x=input()
    
    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='set1':
        print("low1")
        p.ChangeDutyCycle(50)
        x='z'

    elif x=='set2':
        print("low2")
        p.ChangeDutyCycle(55)
        x='z'

    elif x=='set3':
        print("low1")
        p.ChangeDutyCycle(60)
        x='z'

    elif x=='set4':
        print("medium1")
        p.ChangeDutyCycle(65)
        x='z'

    elif x=='set5':
        print("medium2")
        p.ChangeDutyCycle(70)
        x='z'

    elif x=='set6':
        print("medium3")
        p.ChangeDutyCycle(75)
        x='z'

    elif x=='set7':
        print("high1")
        p.ChangeDutyCycle(80)
        x='z'

    elif x=='set8':
        print("high2")
        p.ChangeDutyCycle(85)
        x='z'

    elif x=='set9':
        print("high3")
        p.ChangeDutyCycle(90)
        x='z'

    elif x=='set10':
        print("MAXIMUM OVERDRIVE")
        p.ChangeDutyCycle(100)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")
