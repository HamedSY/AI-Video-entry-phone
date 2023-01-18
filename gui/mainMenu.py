import sys
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget
from PyQt5.uic import loadUi


class welcomeScreen(QDialog):
    def __init__(self):
        super(welcomeScreen, self).__init__()
        loadUi("welcomeScreen.ui", self)
        self.member.clicked.connect(self.memberFunc)
        self.mode_1.clicked.connect(self.mode_1Func)
        self.mode_2.clicked.connect(self.mode_2Func)
        self.mode_3.clicked.connect(self.mode_3Func)

    def memberFunc(self):
        print("add member")
    def mode_1Func(self):
        print("mode 1")
    def mode_2Func(self):
        print("mode 2")
    def mode_3Func(self):
        print("mode 3")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = welcomeScreen()
    widget = QStackedWidget()
    widget.addWidget(window)
    widget.setFixedSize(1000, 800)
    widget.show()
    sys.exit(app.exec())

