import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

algae_trig = 2
algae_echo = 3
auger_en = 4
drive_in2 = 6
left_trig = 12
turn = 13
rx_gps = 14
tx_gps = 15
left_echo = 16
auger_in1 = 17
dispenser_en = 18
dispenser_in1 = 20
dispenser_in2 = 21
drive_in1 = 22
right_trig = 23
right_echo = 24
drive_en = 26
auger_in2 = 27

GPIO.setup(algae_trig, GPIO.OUT)
GPIO.setup(algae_echo, GPIO.IN)
GPIO.setup(auger_en, GPIO.OUT)
GPIO.setup(drive_in2, GPIO.OUT)
GPIO.setup(left_trig, GPIO.OUT)
GPIO.setup(turn, GPIO.OUT)
GPIO.setup(rx_gps, GPIO.IN)
GPIO.setup(tx_gps, GPIO.OUT)
GPIO.setup(left_echo, GPIO.IN)
GPIO.setup(auger_in1, GPIO.OUT)
GPIO.setup(dispenser_en, GPIO.OUT)
GPIO.setup(dispenser_in1, GPIO.OUT)
GPIO.setup(dispenser_in2, GPIO.OUT)
GPIO.setup(drive_in1, GPIO.OUT)
GPIO.setup(right_trig, GPIO.OUT)
GPIO.setup(right_echo, GPIO.IN)
GPIO.setup(drive_en, GPIO.OUT)
GPIO.setup(auger_in2, GPIO.OUT)

def get_algae_trig():
    return algae_trig

def get_algae_echo():
    return algae_echo

def get_auger_en():
    return auger_en

def get_drive_in2():
    return drive_in2

def get_left_trig():
    return left_trig

def get_turn():
    return turn

def get_rx_gps():
    return rx_gps

def get_tx_gps():
    return tx_gps

def get_left_echo():
    return left_echo

def get_auger_in1():
    return auger_in1

def get_dispenser_en():
    return dispenser_en

def get_dispenser_in1():
    return dispenser_in1

def get_dispenser_in2():
    return dispenser_in2

def get_drive_in1():
    return drive_in1

def get_right_trig():
    return right_trig

def get_right_echo():
    return right_echo

def get_drive_en():
    return drive_en

def get_auger_in2():
    return auger_in2
