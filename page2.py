import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDialog, QLineEdit
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import main

url = "http://192.168.53.142:8080/video"
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(url)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


    def stop(self):
        self._run_flag = False
        self.wait()


class App2(QDialog):
    def __init__(self, mode):
        super().__init__()
        self.setupUi()
        print(mode)

    def setupUi(self):
        self.bgWidget = QLabel(self)
        self.bgWidget.setObjectName("bgWidget")
        self.bgWidget.resize(1000, 800)
        self.bgWidget.setStyleSheet("QWidget#bgWidget{\n"
                                    "background-color: qlineargradient(spread:pad, x1:0, y1:0.369, x2:1, y2:0.756, stop:0 rgba(237, 66, 100, 255), stop:1 rgba(255, 237, 188, 255));\n"
                                    "}")

        self.retranslateUi(self.bgWidget)
        QtCore.QMetaObject.connectSlotsByName(self.bgWidget)

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(180, 70, 640, 480))

        print("j")
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    def retranslateUi(self, bgWidget):
        _translate = QtCore.QCoreApplication.translate
        self.bgWidget.setWindowTitle(_translate("self.bgWidget", "Dialog"))
        # self.takePic.setText(_translate("bgWidget", "take picture"))
        # self.nameLabel.setText(_translate("bgWidget", "enter your name:"))

    def closeEvent(self, event):
        self.th.stop()
        event.accept()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

