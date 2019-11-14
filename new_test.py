# pip install pyqt5
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from requests import Session
from threading import Thread
from functools import partial
from os.path import expanduser
import sys, os, getpass, subprocess
from socket import AF_INET, socket, SOCK_STREAM
from time import sleep

title = ' Work Management'
version = 'v0.1'
width = 800
height = 600
username = getpass.getuser()
name = username

class MainMenu(QDialog):
    def __init__(self, parent = None):
        super(MainMenu, self).__init__(parent)
        subprocess.Popen(['test.pdf'],shell=True)
        self.last_pos_x = 0
        self.last_pos_w= 0
        self.last_size_h = 0
        self.last_size_w= 0
        self.title = title + ' ' + version
        self.width = width
        self.height = height
        self.num_of_lower_buttons = 4
        self.setMinimumSize(self.width, self.height)


        self.createTabs()

        topLayout = QHBoxLayout()
        # topLayout.addWidget(styleLabel)
        # topLayout.addWidget(styleComboBox)
        topLayout.addStretch(1)
        # topLayout.addWidget(self.useStylePaletteCheckBox)
        # topLayout.addWidget(disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 0, 0)
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        # mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 0, 0)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)


        mainLayout = QGridLayout()

        #----Now comes the sockets part----
        self.HOST = input('Enter host: ')
        self.PORT = input('Enter port: ')
        if not self.PORT:
            self.PORT = 33000
        else:
            self.PORT = int(self.PORT)

        self.BUFSIZ = 1024
        self.ADDR = (self.HOST, self.PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(self.ADDR)

        self.receive_thread = Thread(target=self.receive)
        self.receive_thread.start()
    def createTabs(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        home_directory = expanduser(os.path.dirname(os.path.realpath(__file__)))
        self.model = QFileSystemModel()
        self.model.setRootPath('')
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)
        self.tree.setRootIndex(self.model.index(home_directory))

        tabFileshbox = QHBoxLayout()
        tabFileshbox.setContentsMargins(5, 5, 5, 5)
        tabFileshbox.addWidget(self.tree)
        tabFiles = QWidget()
        tabFiles.setLayout(tabFileshbox)

        tabChat = QWidget()
        self.textEdit = QPlainTextEdit()
        self.messageText = QLineEdit()
        self.textEdit.setFocusPolicy(Qt.NoFocus)

        tabChathbox = QVBoxLayout()
        tabChathbox.setContentsMargins(5, 5, 5, 5)
        tabChathbox.addWidget(self.textEdit)
        tabChathbox.addWidget(self.messageText)
        tabChat.setLayout(tabChathbox)

        self.bottomLeftTabWidget.addTab(tabFiles, "&Files")
        self.bottomLeftTabWidget.addTab(tabChat, "&Chat")



    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                self.textEdit.appendPlainText(msg)
            except OSError:  # Possibly client has left the chat.
                break


    def send(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        msg = self.messageText.text()
        self.messageText.setText("")  # Clears input field.
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            self.close()


    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.messageText.setText("{quit}")
        send()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(35, 35, 35))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    main = MainMenu()
    main.setWindowTitle('Main Menu')
    main.show()
    sys.exit(app.exec_())
