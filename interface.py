# make an interface using PyQt5 that shows 2 buttons 
# to choose between Project 1 and Project 2
# and a button to quit the program

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import subprocess

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 interface'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create a vertical box layout and add a label
        vbox = QVBoxLayout()
        label = QLabel("Choose a project to run")
        vbox.addWidget(label)

        # Create a horizontal box layout and add buttons
        hbox = QHBoxLayout()
        button1 = QPushButton('Project 1', self)
        button1.setToolTip('Run Project 1')
        button1.clicked.connect(self.on_click1)
        hbox.addWidget(button1)
        button2 = QPushButton('Project 2', self)
        button2.setToolTip('Run Project 2')
        button2.clicked.connect(self.on_click2)
        hbox.addWidget(button2)
        button3 = QPushButton('Quit', self)
        button3.setToolTip('Quit')
        button3.clicked.connect(self.on_click3)
        hbox.addWidget(button3)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Show window
        self.show()

    @pyqtSlot()
    def on_click1(self):
        # Launch ./Server executable in Project1 folder
        server = subprocess.Popen(['./Server'], cwd='./Project1', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Launch ./Client executable in Project1 folder and show output in window
        client = subprocess.Popen(['./Client'], cwd='./Project1', stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        # Connect to the client's subprocess' standard output and error pipes
        client_stdout, client_stderr = client.communicate()

        # Decode the output and error messages of the client
        client_output = client_stdout.decode("utf-8")
        client_error = client_stderr.decode("utf-8")
        

    @pyqtSlot()
    def on_click2(self):
        print('Project 2 button clicked')

    @pyqtSlot()
    def on_click3(self):
        print('Quit button clicked')
        sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

