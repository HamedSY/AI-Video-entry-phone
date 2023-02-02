import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QDialog, QLineEdit
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import database
import controller


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(database.url)
        while True:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        # self._run_flag = False
        self.wait()


class App(QDialog):
    def __init__(self):
        super().__init__()
        self._new_window = None
        self.setupUi()

    def setupUi(self):
        self.bgWidget = QLabel(self)
        self.bgWidget.setObjectName("bgWidget")
        self.bgWidget.resize(600, 400)
        self.bgWidget.setStyleSheet("QWidget#bgWidget{\n"
                               "background-color: qlineargradient(spread:pad, x1:0, y1:0.369, x2:1, y2:0.756, stop:0 rgba(237, 66, 100, 255), stop:1 rgba(255, 237, 188, 255));\n"
                               "}")
        self.takePic = QtWidgets.QPushButton(self.bgWidget)
        self.takePic.setGeometry(QtCore.QRect(410, 170, 170, 40))
        self.takePic.setStyleSheet("border-radius: 20px;\n"
                                   "font: 14pt \"MS Shell Dlg 2\";\n"
                                   "background-color: rgb(57, 174, 169);")
        self.takePic.setObjectName("takePic")
        self.takePic.clicked.connect(self.takePicFunc)
        self.label = QtWidgets.QLabel(self.bgWidget)
        self.label.setGeometry(QtCore.QRect(20, 70, 320, 240))
        self.label.setText("")
        self.label.setObjectName("label")
        self.error = QtWidgets.QLabel(self.bgWidget)
        self.error.setGeometry(QtCore.QRect(230, 10, 121, 31))
        self.error.setStyleSheet("color: red;\n"
                                 "font: 10pt \"MS Shell Dlg 2\";")
        self.error.setText("")
        self.error.setObjectName("error")
        self.nameInput = QtWidgets.QLineEdit(self.bgWidget)
        self.nameInput.setGeometry(QtCore.QRect(420, 120, 142, 30))
        self.nameInput.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
                                     "background-color: rgba(0, 0, 0, 0);")
        self.nameInput.setObjectName("nameInput")
        self.return_2 = QtWidgets.QPushButton(self.bgWidget)
        self.return_2.setGeometry(QtCore.QRect(410, 220, 170, 40))
        self.return_2.setStyleSheet("border-radius: 20px;\n"
                                    "font: 14pt \"MS Shell Dlg 2\";\n"
                                    "background-color: rgb(57, 174, 169);")
        self.return_2.setObjectName("return_2")
        # self.takePic.clicked.connect(self.returnFunc)
        self.nameLabel = QtWidgets.QLabel(self.bgWidget)
        self.nameLabel.setGeometry(QtCore.QRect(420, 100, 150, 20))
        self.nameLabel.setObjectName("nameLabel")

        self.retranslateUi(self.bgWidget)
        QtCore.QMetaObject.connectSlotsByName(self.bgWidget)

        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

    def retranslateUi(self, bgWidget):
        _translate = QtCore.QCoreApplication.translate
        self.bgWidget.setWindowTitle(_translate("bgWidget", "Dialog"))
        self.takePic.setText(_translate("bgWidget", "take picture"))
        self.return_2.setText(_translate("bgWidget", "return"))
        self.nameLabel.setText(_translate("bgWidget", "enter your name:"))

    def closeEvent(self, event):
        self.th.stop()
        event.accept()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def takePicFunc(self):
        name = self.nameInput.text()
        if len(name) == 0:
            self.error.setText("name box is empty!")
        else:
            controller.takePicture(str(len(database.valid_imgs) + 1))
            self.error.setText(controller.updateValidImgs(str(len(database.valid_imgs) + 1) + ".jpg"))

    # def returnFunc(selfself):
    # #TODO : switch to main




