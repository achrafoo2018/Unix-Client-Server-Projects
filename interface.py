#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import subprocess
from time import sleep


class Ui_Dialog(object):
    def __init__(self):
        self.choice = 2 # default choice is project 2
        self.server = None
        self.client = None

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(720, 480)
        Dialog.setMaximumSize(QtCore.QSize(720, 1080))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        # Server text box
        self.serverPlainText = QtWidgets.QPlainTextEdit(Dialog)
        self.serverPlainText.setReadOnly(True)
        self.serverPlainText.setObjectName("plainTextEdit")
        self.horizontalLayout_4.addWidget(self.serverPlainText)

        # Client text box
        self.clientPlainText = QtWidgets.QPlainTextEdit(Dialog)
        self.clientPlainText.setReadOnly(True)
        self.clientPlainText.setObjectName("plainTextEdit_2")
        self.horizontalLayout_4.addWidget(self.clientPlainText)

        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.pushButton = QtWidgets.QPushButton(Dialog)

        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_5.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_5.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_5.setText(_translate("Dialog", "Run Server"))
        self.pushButton_5.clicked.connect(self.run_server)

        self.pushButton_4.setText(_translate("Dialog", "Run Client"))
        self.pushButton_4.clicked.connect(self.run_client)

        self.pushButton.setText(_translate("Dialog", "TCP Socket"))
        self.pushButton.setStyleSheet("background-color: green")
        self.pushButton.clicked.connect(self.tcp_socket)

        self.pushButton_2.setText(_translate("Dialog", "Named Pipe"))
        self.pushButton_2.clicked.connect(self.pipe)

        self.pushButton_3.setText(_translate("Dialog", "EXIT"))
        self.pushButton_3.clicked.connect(self.exit)
    
    def run_server(self):
        serverLog = open("server.log", "w+")
        # empty the log file
        serverLog.write("")
        if self.server is not None:
            self.server.kill()
            self.server = None
        if self.choice == 1: # PIPE (Project 1)
            self.server = subprocess.Popen(['./Server'], cwd='./Named_PIPE', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else: # TCP Socket (Project 2)
            self.server = subprocess.Popen(['./Server'], cwd='./TCP_Socket', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        sleep(0.5)
        self.serverPlainText.setPlainText(serverLog.read())
        serverLog.close()


    def run_client(self):
        if self.server is None:
            self.clientPlainText.setPlainText("Server is not running...")
            return

        if self.client is not None:
            self.client.kill()

        if self.choice == 1: # PIPE (Project 1)
            self.client = subprocess.Popen(['./Client'], cwd='./Named_PIPE', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else: # TCP Socket (Project 2)
            self.client = subprocess.Popen(['./Client'], cwd='./TCP_Socket', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Connect to the client's subprocess' standard output and error pipes
        try:
            client_stdout, client_stderr = self.client.communicate(timeout=2)
        except subprocess.TimeoutExpired:
            self.client.kill()
            self.clientPlainText.setPlainText("Client timed out...")
            return
        if self.client.poll() is None:
            self.client.kill()
            self.clientPlainText.setPlainText("Client timed out...")
            return

        # Decode the output and error messages of the client
        client_output = client_stdout.decode("utf-8")
        client_error = client_stderr.decode("utf-8")

        # Print the output and error messages of the client to the client text box
        self.clientPlainText.setPlainText(client_output)
        if client_error:
            self.clientPlainText.setPlainText(client_error)

        serverLog = open("server.log", "r")
        self.serverPlainText.setPlainText(serverLog.read())
        serverLog.close()

    def tcp_socket(self):
        if self.server is not None:
            self.server.kill()
            self.server = None
        self.choice = 2
        # make the TCP Socket button green
        self.pushButton.setStyleSheet("background-color: green")

        # make the PIPE button white
        self.pushButton_2.setStyleSheet("background-color: white")

        # clear the Server and Client text boxes
        self.serverPlainText.setPlainText("")
        self.clientPlainText.setPlainText("")
        serverLog = open("server.log", "w")
        # empty the server log file
        serverLog.write("")
        serverLog.close()


    def pipe(self):
        if self.server is not None:
            self.server.kill()
            self.server = None
        self.choice = 1
        # make the PIPE button green
        self.pushButton_2.setStyleSheet("background-color: green")

        # make the TCP Socket button white
        self.pushButton.setStyleSheet("background-color: white")

        # clear the Server and Client text boxes
        self.serverPlainText.setPlainText("")
        self.clientPlainText.setPlainText("")
        serverLog = open("server.log", "w")
        # empty the server log file
        serverLog.write("")
        serverLog.close()


    def exit(self):
        if self.server is not None:
            self.server.kill()
        if self.client is not None:
            self.client.kill()
        sys.exit()



def run_makefiles():
    subprocess.call(['make'], cwd='./Named_PIPE')
    subprocess.call(['make'], cwd='./TCP_Socket')


if __name__ == "__main__":
    run_makefiles() # Run the makefiles for both projects

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

