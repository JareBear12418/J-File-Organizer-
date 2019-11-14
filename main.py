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
from time import sleep

title = ' Work Management'
version = 'v0.1'
width = 800
height = 600
username = getpass.getuser()
name = username
chat_url = "https://build-system.fman.io/chat"
server = Session()
new_messages = []

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

        # self.fetch_new_messages()
        self.thread = Thread(target=self.fetch_new_messages, daemon=True)
        self.thread.start()
        self.display_new_messages()
        # Signals:
        self.messageText.returnPressed.connect(self.send_message)
        self.timer = QTimer()
        self.timer.timeout.connect(self.display_new_messages)
        self.timer.start(1000)
    def createTabs(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        home_directory = expanduser(os.path.dirname(os.path.realpath(__file__)))
        model = QDirModel()
        view = QTreeView()
        view.setModel(model)
        view.setRootIndex(model.index(home_directory))

        tabFileshbox = QHBoxLayout()
        tabFileshbox.setContentsMargins(5, 5, 5, 5)
        tabFileshbox.addWidget(view)
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

    def fetch_new_messages(self):
        while True:
            response = server.get(chat_url).text
            if response:
                new_messages.append(response)
            sleep(.5)

    def display_new_messages(self):
        while new_messages:
            self.textEdit.appendPlainText(new_messages.pop(0))

    def send_message(self):
        from datetime import datetime
        server.post(chat_url, {"time": str(datetime.now()), "name": name, "message": self.messageText.text()})
        self.messageText.clear()



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
