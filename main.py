import face_recognition
import cv2
import numpy as np
import time
import os
import smtplib
from email.message import EmailMessage
import ssl
import RPi.GPIO as GPIO
from gpiozero import Buzzer

sender = 'hamed007.saboor@gmail.com'
receiver = 'amir.h.rnn@gmail.com'
subject = 'Knock Knock!'
password = '' #TODO hamed's application password
message = "Hello!\nA Person has just ringed your house!\nHis/Her picture is attached to the mail.\n"
imageFile = "unknown.jpg"

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

def turn_off():
    GPIO.output(BLUE_LED,False)
    GPIO.output(RED_LED,False)

def turn_on(status):
    if status == "blue":
        GPIO.output(BLUE_LED,True)
    elif status == "red":
        GPIO.output(RED_LED,True)
    time.sleep(2)
    turn_off()


def takePicture(img_name):
    video_capture = cv2.VideoCapture('http://172.27.55.203:8080/video')
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, None, fx = 0.3, fy = 0.3)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imshow('img',frame) # display the captured image
    cv2.imwrite(img_name + '.jpg', frame)
           
    video_capture.release()
    cv2.destroyAllWindows()


def updateValidImgs(name):
    this_img = face_recognition.load_image_file(name)
    try:
        valid_imgs_encodings.append(face_recognition.face_encodings(this_img)[0])
        valid_imgs.append(this_img)
        print("your image added successfully!")
    except IndexError:
        print("image " + name + " doesn't have any faces")
        return


def compareFaces(valid_imgs_encodings, frame_img_encoding):
    for result in face_recognition.compare_faces(valid_imgs_encodings, frame_img_encoding):
        if result:
            return True
    return False


def sendEmail():
    email = EmailMessage()
    email['From'] = sender
    email['Subject'] = subject
    email.set_content(message)
    with open(imageFile, 'rb') as fp:
        imgData = fp.read()
    email.add_attachment(imgData, maintype = 'image', subtype = 'png')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, email.as_string())
        print("Email has been sent successfully!")


def pushButton(buzz): #FIXME check if mod and valid_imgs_encodings are need to be passed to function
    if mod == 3:
        return

    os.chdir('..')
    takePicture("unknown")
    buzzer_sound(buzz)
    unknown_face = face_recognition.load_image_file("unknown.jpg")
    unknown_face_encodings = face_recognition.face_encodings(unknown_face)

    if mod == 1:
        for unknown_face_encoding in unknown_face_encodings:
            if compareFaces(valid_imgs_encodings, unknown_face_encoding):
                turn_on("blue")
                return
        turn_on("red")

    elif mod == 2:
        sendEmail()

    os.chdir('imgs')
        
        

video_capture = cv2.VideoCapture('http://172.27.55.203:8080/video')
valid_imgs = []
valid_imgs_encodings = []
os.chdir('imgs')
for file in os.listdir():
    if file.endswith('.jpg'):
        this_img = face_recognition.load_image_file(file)
        try:
            valid_imgs.append(this_img)
            valid_imgs_encodings.append(face_recognition.face_encodings(this_img)[0])
        except IndexError:
            print("this image doesn't have any faces")
            continue

mod = -1
process_this_frame = True

counter = 0

GPIOsetup()
buzz = GPIO.PWM(BuzzerPin,440)
GPIO.add_event_detect(PUSH_BUTTON, GPIO.RISING, callback = lambda x: pushButton(buzz))

while (True):
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, None, fx = 0.3, fy = 0.3)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1)
    if key == ord('c'):
        takePicture(str(len(valid_imgs) + 1))
        updateValidImgs(str(len(valid_imgs) + 1) + ".jpg")
    # elif key == ord('b'): # instead of push button
    #     pushButton()

    elif key == ord('1'):
        mod = 1
        print("Mode has changed successfully: An alone little kid at home!")
    elif key == ord('2'):
        mod = 2
        print("Mode has changed successfully: No one at home!")
    elif key == ord('3'):
        mod = 3
        print("Mode has changed successfully: Automatic mode!")
    elif key == ord('q'):
        print("out of the program ...")
        break


    if mod == 3:
        if counter % 10 == 0:
            if process_this_frame:
                rgb_frame = frame[:, :, ::-1]
                frame_img_encodings = face_recognition.face_encodings(rgb_frame)
                for frame_img_encoding in frame_img_encodings:
                    if compareFaces(valid_imgs_encodings, frame_img_encoding):
                        print("A valid face has been recognized!")
                        mod = -1
                    
            process_this_frame = not process_this_frame
    
    counter += 1
    if counter % 10000 == 0:
        counter = 0