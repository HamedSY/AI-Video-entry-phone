import os
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
import database
from takePicPage import App
from page2 import App2
import face_recognition
import controller
import RPi.GPIO as GPIO

video_capture = cv2.VideoCapture(database.url)
os.chdir('imgs')
for file in os.listdir():
    if file.endswith('.jpg'):
        this_img = face_recognition.load_image_file(file)
        try:
            database.valid_imgs.append(this_img)
            database.valid_imgs_encodings.append(face_recognition.face_encodings(this_img)[0])
        except IndexError:
            print("this image doesn't have any faces")
            continue


controller.GPIOsetup()
buzz = GPIO.PWM(controller.BuzzerPin,440)
GPIO.add_event_detect(controller.PUSH_BUTTON, GPIO.RISING, callback = lambda x: controller.pushButton(buzz))


class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen, self).__init__()
        loadUi("../welcomeScreen.ui", self)
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
        database.mode = 1
        window.hide()
        self._new_window = App2()
        self._new_window.show()
        print("entered")

    def mode_2Func(self):
        print("mode 2")
        database.mode = 2
        window.hide()
        self._new_window = App2()
        self._new_window.show()
        print("entered")
    def mode_3Func(self):
        print("mode 3")
        database.mode = 3
        window.hide()
        self._new_window = App2()
        self._new_window.show()
        print("entered")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = welcomeScreen()
    window.show()
    sys.exit(app.exec())

