import face_recognition
import cv2
import numpy as np
import time
import os

def takePicture(img_name):
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, None, fx = 0.3, fy = 0.3)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    cv2.imshow('img',frame) # display the captured image
    cv2.imwrite(img_name + '.jpg', frame)
           
    video_capture.release()
    cv2.destroyAllWindows()

def compare_faces(valid_imgs_encodings):
    unknown_face = face_recognition.load_image_file("unknown.jpg")
    unknown_face_encoding = face_recognition.face_encodings(unknown_face)
    for result in face_recognition.compare_faces(valid_imgs_encodings, unknown_face_encoding):
        if result:
            return True
    return False




valid_imgs = []
valid_imgs_encodings = []
os.chdir('imgs')
for file in os.listdir():
    if file.endswith('.jpg'):
        this_img = face_recognition.load_image_file(file)
        valid_imgs.append(this_img)
        try:
            valid_imgs_encodings.append(face_recognition.face_encodings(this_img)[0])
        except IndexError:
            print("this image doesn't have any faces")
            continue

video_capture = cv2.VideoCapture('http://172.27.55.203:8080/video')

# while True:
    





# takePicture('salam')


