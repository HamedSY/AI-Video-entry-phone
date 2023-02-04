import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDialog, QLineEdit
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import face_recognition
import main


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        counter = 0
        cap = cv2.VideoCapture(main.url)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
            if main.mode == 3:
                counter += 1
                if counter % 20 != 0:
                    continue
                for frame_img_encoding in face_recognition.face_encodings(frame):
                    if main.compareFaces(main.valid_imgs_encodings, frame_img_encoding):
                        main.showMessage("A valid face has been recognized!")
                        main.turn_off()
                        main.turn_on("blue", 3)
                        main.turn_on("red", -1)
            if counter % 10000 == 0:
                counter = 0

    def stop(self):
        # self._run_flag = False
        self.wait()


class App2(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.bgWidget = QLabel(self)
        self.bgWidget.setObjectName("bgWidget")
        self.bgWidget.resize(600, 400)
        self.bgWidget.setStyleSheet("QWidget#bgWidget{\n"
                                    "background-color: qlineargradient(spread:pad, x1:0, y1:0.369, x2:1, y2:0.756, stop:0 rgba(237, 66, 100, 255), stop:1 rgba(255, 237, 188, 255));\n"
                                    "}")
        self.return_ = QtWidgets.QPushButton(self.bgWidget)
        self.return_.setGeometry(QtCore.QRect(215, 320, 170, 40))
        self.return_.setStyleSheet("border-radius: 20px;\n"
                                    "font: 14pt \"MS Shell Dlg 2\";\n"
                                    "background-color: rgb(57, 174, 169);")
        self.return_.setObjectName("return_")
        self.return_.clicked.connect(self.returnFunc)

        self.retranslateUi(self.bgWidget)
        QtCore.QMetaObject.connectSlotsByName(self.bgWidget)

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(140, 60, 320, 240))

        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

    def retranslateUi(self, bgWidget):
        _translate = QtCore.QCoreApplication.translate
        self.bgWidget.setWindowTitle(_translate("self.bgWidget", "Dialog"))
        self.return_.setText(_translate("bgWidget", "return"))

    def closeEvent(self, event):
        self.th.quit()
        event.accept()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def returnFunc(self):
        main.mode = -1
        self.th.quit()
        main.qtStack.setCurrentIndex(0)

