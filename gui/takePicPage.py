import cv2
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDialog, QLineEdit
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        print("b Video")
        cap = cv2.VideoCapture("http://102.172.117.114:8086/video")
        print("in run")
        while True:
            print("shit")
            ret, frame = cap.read()
            print("shit2")
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.bgWidget = QLabel(self)
        self.bgWidget.setObjectName("bgWidget")
        self.bgWidget.resize(1000, 800)
        self.bgWidget.setStyleSheet("QWidget#bgWidget{\n"
                                    "background-color: qlineargradient(spread:pad, x1:0, y1:0.369, x2:1, y2:0.756, stop:0 rgba(237, 66, 100, 255), stop:1 rgba(255, 237, 188, 255));\n"
                                    "}")
        self.error = QLabel(self.bgWidget)
        self.error.setGeometry(QtCore.QRect(420, 715, 211, 51))
        self.error.setStyleSheet("color: red;\n"
                                "font: 10pt \"MS Shell Dlg 2\";")
        self.error.setObjectName("error")

        self.nameLabel = QLabel(self.bgWidget)
        self.nameLabel.setGeometry(QtCore.QRect(391, 538, 211, 51))
        self.nameLabel.setStyleSheet("border-radius: 20px;\n"
                                   "font: 10pt \"MS Shell Dlg 2\";")
        self.nameLabel.setObjectName("nameLabel")

        self.nameInput = QLineEdit(self.bgWidget)
        self.nameInput.setGeometry(QtCore.QRect(390, 580, 211, 51))
        self.nameInput.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
                                  "background-color: rgba(0, 0, 0, 0);")
        self.nameInput.setObjectName("nameInput")

        self.takePic = QtWidgets.QPushButton(self.bgWidget)
        self.takePic.setGeometry(QtCore.QRect(390, 660, 211, 51))
        self.takePic.setStyleSheet("border-radius: 20px;\n"
                                  "font: 14pt \"MS Shell Dlg 2\";\n"
                                  "background-color: rgb(57, 174, 169);")
        self.takePic.setObjectName("takePic")
        self.takePic.clicked.connect(self.takePicFunc)

        self.retranslateUi(self.bgWidget)
        QtCore.QMetaObject.connectSlotsByName(self.bgWidget)

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(180, 70, 640, 480))

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

    def retranslateUi(self, bgWidget):
        _translate = QtCore.QCoreApplication.translate
        self.bgWidget.setWindowTitle(_translate("self.bgWidget", "Dialog"))
        self.takePic.setText(_translate("bgWidget", "take picture"))
        self.nameLabel.setText(_translate("bgWidget", "enter your name:"))

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def takePicFunc(self):
        name = self.nameInput.text()
        if len(name) == 0:
            self.error.setText("name box is empty!")
        # else:
        #ToDo: save the picture


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec())

