import os
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from PyQt5.uic import loadUi
from takePicPage import App
from page2 import App2
import face_recognition
import main
# import face_recognition
# import cv2
# import numpy as np
# import smtplib
# from email.message import EmailMessage
# import ssl
# import RPi.GPIO as GPIO
# from gpiozero import Buzzer

url = "http://192.168.53.142:8080/video"
video_capture = cv2.VideoCapture(url)
os.chdir('imgs')
for file in os.listdir():
    if file.endswith('.jpg'):
        this_img = face_recognition.load_image_file(file)
        try:
            main.valid_imgs.append(this_img)
            main.valid_imgs_encodings.append(face_recognition.face_encodings(this_img)[0])
        except IndexError:
            print("this image doesn't have any faces")
            continue

mod = -1
process_this_frame = True
counter = 0

# main.GPIOsetup()
# buzz = GPIO.PWM(main.BuzzerPin,440)
# GPIO.add_event_detect(main.PUSH_BUTTON, GPIO.RISING, callback = lambda x: main.pushButton(buzz))


class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen, self).__init__()
        loadUi("../welcomeScreen.ui", self)
        mode = -1
        self._new_window = None
        self.member.clicked.connect(self.memberFunc)
        self.mode_1.clicked.connect(self.mode_1Func)
        self.mode_2.clicked.connect(self.mode_2Func)
        self.mode_3.clicked.connect(self.mode_3Func)

    def memberFunc(self):
        print("add member")
        window.hide()
        self._new_window = App()
        self._new_window.show()
        print("Video Played")
    def mode_1Func(self):
        print("mode 1")
        mode = 1
        window.hide()
        self._new_window = App2(mode)
        self._new_window.show()
        print("entered")

    def mode_2Func(self):
        print("mode 2")
        mode = 2
        window.hide()
        self._new_window = App2(mode)
        self._new_window.show()
        print("entered")
    def mode_3Func(self):
        print("mode 3")
        mode = 3
        window.hide()
        self._new_window = App2(mode)
        self._new_window.show()
        print("entered")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = welcomeScreen()
    window.show()
    sys.exit(app.exec())

