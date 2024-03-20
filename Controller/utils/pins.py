import RPI.GPIO as GPIO

start_stop_move = 8
return_home = 14
emergency_stop = 15
set_home = 18
out_of_algaecide = 20
immobilized = 21
change_algaecide = 23
start_stop_algaecide = 24

GPIO.setup(start_stop_move, GPIO.IN)
GPIO.setup(return_home, GPIO.IN)
GPIO.setup(emergency_stop, GPIO.IN)
GPIO.setup(set_home, GPIO.IN)
GPIO.setup(out_of_algaecide, GPIO.OUT)
GPIO.setup(immobilized, GPIO.OUT)
GPIO.setup(change_algaecide, GPIO.IN)
GPIO.setup(start_stop_algaecide, GPIO.IN)

def get_stop_start_move():
    return start_stop_move

def get_return_home():
    return return_home

def get_emergency_stop():
    return emergency_stop

def get_set_home():
    return set_home

def get_out_of_algaecide():
    return out_of_algaecide

def get_immobilized():
    return immobilized

def get_change_algaecide():
    return change_algaecide

def get_start_stop_algaecide():
    return start_stop_algaecide
