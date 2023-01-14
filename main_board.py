import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer
SPEED = 1.5
RED_LED = 12
BLUE_LED = 16
BuzzerPin = 13
PUSH_BUTTON = 22

TONES = {
        "c6":1047,
        "b5":988,
        "a5":888,
        "g5":784,
        "f5":698,
        "e5":659,
        "eb5":622,
        "d5":587,
        "c5":523,
        "b4":494,
        "a4":440,
        "ab4":415,
        "g4":392,
        "f4":349,
        "e4":330,
        "d4":294,
        "c4":262,
        }
SONG = [
        ["e5",16],["eb5",16],
        ["e5",16],["eb5",16],["e5",16],["b4",16],["d5",16],["c5",16],
        ["a4",8],["p",16],["c4",16],["e4",16],["a4",16],
        ["b4",8],["p",16],["e4",16],["ab4",16],["b4",16],
        ["c5",8],["p",16],["e4",16],["e5",16],["eb5",16],
        ["e5",16],["eb5",16],["e5",16],["b4",16],["d5",16],["c5",16],
        ["a4",8],["p",16],["c4",16],["e4",16],["a4",16],
        ["b4",8],["p",16],["e4",16],["c5",16],["b4",16],["a4",4]
       ]   
        


def GPIOsetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(BuzzerPin, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(BLUE_LED, GPIO.OUT)
    GPIO.setup(PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    

def play_tone(p,tone):
    duration = 1./(tone[1]*0.25*SPEED)
    if tone[0] == 'p':
        time.sleep(duration)
    else:
        frequency = TONES[tone[0]]
        p.ChangeFrequency(frequency)
        p.start(0.5)
        time.sleep(duration)
        p.stop()
        
def buzzer_sound(buzz):
    for t in SONG:
        play_tone(buzz,t)
        
def turn_on(status):
    if status:
        GPIO.output(BLUE_LED,True)
    else:
        GPIO.output(RED_LED,True)

def turn_off():
    GPIO.output(BLUE_LED,False)
    GPIO.output(RED_LED,False)

GPIOsetup()
buzz = GPIO.PWM(BuzzerPin,440)
GPIO.add_event_detect(PUSH_BUTTON,GPIO.RISING,callback=lambda x: buzzer_sound(buzz))

while True:
    command = input()
    if command == 'buz':
        buzzer_sound(buzz)
    elif command == 'blu':
        turn_on(True)
    elif command == 'red':
        turn_on(False)
    elif command == 'off':
        turn_off()
    else:
        break

GPIO.output(BuzzerPin, GPIO.HIGH)        
GPIO.cleanup()


