import face_recognition
import cv2
import time
import smtplib
from email.message import EmailMessage
import ssl
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QMessageBox

url = 'http://192.168.1.4:8080/video'
sender = 'amirrn13821382@gmail.com'
receiver = 'amir.h.rnn@gmail.com'
subject = 'Knock Knock!'
password = 'rqbndsjuhanxutkh'
message = "Hello!\nA Person has just ringed your house!\nHis/Her picture is attached to the mail.\n"
imageFile = "unknown.jpg"
qtStack = None

RED_LED = 12
BLUE_LED = 16
PUSH_BUTTON = 22
BUZZER_PIN = 13
SPEED = 2

notes = {
    'B0': 31,
    'C1': 33, 'CS1': 35,
    'D1': 37, 'DS1': 39,
    'EB1': 39,
    'E1': 41,
    'F1': 44, 'FS1': 46,
    'G1': 49, 'GS1': 52,
    'A1': 55, 'AS1': 58,
    'BB1': 58,
    'B1': 62,
    'C2': 65, 'CS2': 69,
    'D2': 73, 'DS2': 78,
    'EB2': 78,
    'E2': 82,
    'F2': 87, 'FS2': 93,
    'G2': 98, 'GS2': 104,
    'A2': 110, 'AS2': 117,
    'BB2': 123,
    'B2': 123,
    'C3': 131, 'CS3': 139,
    'D3': 147, 'DS3': 156,
    'EB3': 156,
    'E3': 165,
    'F3': 175, 'FS3': 185,
    'G3': 196, 'GS3': 208,
    'A3': 220, 'AS3': 233,
    'BB3': 233,
    'B3': 247,
    'C4': 262, 'CS4': 277,
    'D4': 294, 'DS4': 311,
    'EB4': 311,
    'E4': 330,
    'F4': 349, 'FS4': 370,
    'G4': 392, 'GS4': 415,
    'A4': 440, 'AS4': 466,
    'BB4': 466,
    'B4': 494,
    'C5': 523, 'CS5': 554,
    'D5': 587, 'DS5': 622,
    'EB5': 622,
    'E5': 659,
    'F5': 698, 'FS5': 740,
    'G5': 784, 'GS5': 831,
    'A5': 880, 'AS5': 932,
    'BB5': 932,
    'B5': 988,
    'C6': 1047, 'CS6': 1109,
    'D6': 1175, 'DS6': 1245,
    'EB6': 1245,
    'E6': 1319,
    'F6': 1397, 'FS6': 1480,
    'G6': 1568, 'GS6': 1661,
    'A6': 1760, 'AS6': 1865,
    'BB6': 1865,
    'B6': 1976,
    'C7': 2093, 'CS7': 2217,
    'D7': 2349, 'DS7': 2489,
    'EB7': 2489,
    'E7': 2637,
    'F7': 2794, 'FS7': 2960,
    'G7': 3136, 'GS7': 3322,
    'A7': 3520, 'AS7': 3729,
    'BB7': 3729,
    'B7': 3951,
    'C8': 4186, 'CS8': 4435,
    'D8': 4699, 'DS8': 4978
}
popcorn_melody = [
    notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'],
    notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'],
    notes['A4'], notes['B4'], notes['C5'], notes['B4'], notes['C5'], notes['A4'], notes['B4'], notes['A4'], notes['B4'], notes['G4'],
    notes['A4'], notes['G4'], notes['A4'], notes['F4'], notes['A4'],
]
popcorn_tempo = [
    8, 8, 8, 8, 8, 8, 4,
    8, 8, 8, 8, 8, 8, 4,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 4,

]
manaderna_melody = [
    notes['E4'], notes['E4'], notes['F4'], notes['G4'],
    notes['G4'], notes['F4'], notes['E4'], notes['D4'],
    notes['C4'], notes['C4'], notes['D4'], notes['E4'],
    notes['E4'], 0, notes['D4'], notes['D4'], 0,
    notes['E4'], notes['E4'], notes['F4'], notes['G4'],
    notes['G4'], notes['F4'], notes['E4'], notes['D4'],
    notes['C4'], notes['C4'], notes['D4'], notes['E4'],
    notes['D4'], 0, notes['C4'], notes['C4'],
]

manaderna_tempo = [
    2, 2, 2, 2,
    2, 2, 2, 2,
    2, 2, 2, 2,
    2, 4, 4, 2, 4,
    2, 2, 2, 2,
    2, 2, 2, 2,
    2, 2, 2, 2,
    2, 4, 4, 2, 4,
]

mysong = [
    notes["E5"], notes["EB5"],
    notes["E5"], notes["EB5"], notes["E5"], notes["B4"], notes["D5"], notes["C5"],
    notes["A4"], 0, notes["C4"], notes["E4"], notes["A4"],
    notes["B4"], 0, notes["E4"], notes["AB4"], notes["B4"],
    notes["C5"], 0, notes["E4"], notes["E5"], notes["EB5"],
    notes["E5"], notes["EB5"], notes["E5"], notes["B4"], notes["D5"], notes["C5"],
    notes["A4"], 0, notes["C4"], notes["E4"], notes["A4"],
    notes["B4"], 0, notes["E4"], notes["C5"], notes["B4"], notes["A4"]
]
mysong_tempo = [
    16, 16,
    16, 16, 16, 16, 16, 16,
    8, 16, 16, 16, 16,
    8, 16, 16, 16, 16,
    8, 16, 16, 16, 16,
    16, 16, 16, 16, 16, 16,
    8, 16, 16, 16, 16,
    8, 16, 16, 16, 16, 4
]


def GPIOsetup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(BUZZER_PIN, GPIO.IN)
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.setup(BLUE_LED, GPIO.OUT)
    GPIO.setup(PUSH_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(PUSH_BUTTON, GPIO.RISING,
                          callback=lambda x: pushButton())


def destroy():
    GPIO.cleanup()


def turn_off():
    GPIO.output(BLUE_LED, False)
    GPIO.output(RED_LED, False)


def turn_on(status, displayTime: int):
    if status == "blue":
        GPIO.output(BLUE_LED, True)
    elif status == "red":
        GPIO.output(RED_LED, True)

    if displayTime != -1:
        time.sleep(displayTime)
        turn_off()


def buzz(frequency, length):

    if (frequency == 0):
        time.sleep(length)
        return
    period = 1.0 / (frequency * SPEED)
    delayValue = period / 2
    numCycles = int(length * frequency)

    for i in range(numCycles):
        GPIO.output(BUZZER_PIN, True)
        time.sleep(delayValue)
        GPIO.output(BUZZER_PIN, False)
        time.sleep(delayValue)


def play(melody, tempo, pause, pace=0.800):

    for i in range(0, len(melody)):

        noteDuration = pace/tempo[i]
        buzz(melody[i], noteDuration)

        pauseBetweenNotes = noteDuration * pause
        time.sleep(pauseBetweenNotes)


def takePicture(img_name):
    video_capture = cv2.VideoCapture(url)
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, None, fx=0.3, fy=0.3)
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(img_name + '.jpg', frame)
    video_capture.release()
    cv2.destroyAllWindows()


def updateValidImgs(name):
    this_img = face_recognition.load_image_file(name)
    try:
        valid_imgs_encodings.append(
            face_recognition.face_encodings(this_img)[0])
        valid_imgs.append(this_img)
        showMessage(name + " added successfully as a valid image!")
    except IndexError:
        showMessage("image " + name + " doesn't have any faces")
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
        email.add_attachment(imgData, maintype='image', subtype='jpg')

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, email.as_string())
        showMessage("Email has been sent successfully!")


def pushButton():
    if mode == 3:
        return

    takePicture("unknown")
    unknown_face = face_recognition.load_image_file("unknown.jpg")
    unknown_face_encodings = face_recognition.face_encodings(unknown_face)

    if mode == 1:
        print("Playing : Manaderna (Symphony No. 9) Melody")
        play(manaderna_melody, manaderna_tempo, 0.30)
        for unknown_face_encoding in unknown_face_encodings:
            if compareFaces(valid_imgs_encodings, unknown_face_encoding):
                showMessage("Face recognized.")
                turn_on("blue", 2)
                return
        showMessage("Face didn't recognize!")
        turn_on("red", 2)

    elif mode == 2:
        turn_on("blue", -1)
        turn_on("red", -1)
        print("Playing : Popcorn Melody")
        play(popcorn_melody, popcorn_tempo, 0.50, 1.000)
        print("Sending email to house")
        sendEmail()
        turn_off()


def showMessage(info):
    # error_dialog = QtWidgets.QErrorMessage()
    # error_dialog.showMessage(msg)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(info)
    msg.setWindowTitle("Message")
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()


valid_imgs = []
valid_imgs_encodings = []
mode = -1
counter = 0

#
# while (True):
#     # ret, frame = video_capture.read()
#     # frame = cv2.resize(frame, None, None, fx=0.3, fy=0.3)
#     # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
#     # cv2.imshow('Webcam', frame)
#
#     key = cv2.waitKey(1)
#     if key == ord('c'):
#         takePicture(str(len(valid_imgs) + 1))
#         updateValidImgs(str(len(valid_imgs) + 1) + ".jpg")
#
#     elif key == ord('1'):
#         turn_off()
#         mode = 1
#         print("Mode has changed successfully: An alone little kid at home!")
#     elif key == ord('2'):
#         turn_off()
#         mode = 2
#         print("Mode has changed successfully: No one at home!")
#     elif key == ord('3'):
#         turn_off()
#         mode = 3
#         turn_on("red", -1)
#         print("Mode has changed successfully: Automatic mode!")
#     elif key == ord('q'):
#         print("out of the program ...")
#         destroy()
#         quit()
#
#     if mode == 3:
#         counter += 1
#         if counter % 20 != 0:
#             continue
#
#         for frame_img_encoding in face_recognition.face_encodings(frame):
#             if compareFaces(valid_imgs_encodings, frame_img_encoding):
#                 print("A valid face has been recognized!")
#                 turn_off()
#                 turn_on("blue", 3)
#                 turn_on("red", -1)
#
#     if counter % 10000 == 0:
#         counter = 0