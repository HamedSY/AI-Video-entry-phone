import face_recognition
import cv2
import numpy as np
import time
import os

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
    # unknown_face = face_recognition.load_image_file("unknown.jpg")
    # unknown_face_encoding = face_recognition.face_encodings(unknown_face)
    for result in face_recognition.compare_faces(valid_imgs_encodings, frame_img_encoding):
        if result:
            return True
    return False



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

while (True):
    ret, frame = video_capture.read()
    frame = cv2.resize(frame, None, None, fx = 0.3, fy = 0.3)
    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imshow('Webcam', frame)

    key = cv2.waitKey(1)
    if key == ord('c'):
        takePicture(str(len(valid_imgs) + 1))
        updateValidImgs(str(len(valid_imgs) + 1) + ".jpg")
    elif key == ord('b'): # instead of push button
        if mod == 1:
            os.chdir('..')
            takePicture("unknown")
            unknown_face = face_recognition.load_image_file("unknown.jpg")
            unknown_face_encodings = face_recognition.face_encodings(unknown_face)
            os.chdir('imgs')
            for unknown_face_encoding in unknown_face_encodings:
                if compareFaces(valid_imgs_encodings, unknown_face_encoding):
                    print("Open!")
        elif mod == 2:
            

    elif key == ord('1'):
        mod = 1
        print("Mode has changed successfully to 1")
    elif key == ord('2'):
        mod = 2
        print("Mode has changed successfully to 2")
    elif key == ord('3'):
        mod = 3
        print("Mode has changed successfully to 3")
    elif key == ord('q'):
        print("out of the program ...")
        break


    if mod == 3:
        if int(time.time()) % 2 == 0:
            if process_this_frame:
                rgb_frame = frame[:, :, ::-1]
                frame_img_encodings = face_recognition.face_encodings(rgb_frame)
                for frame_img_encoding in frame_img_encodings:
                    if compareFaces(valid_imgs_encodings, frame_img_encoding):
                        print("A valid face has been recognized!")
                        mod = -1;
                    
            process_this_frame = not process_this_frame