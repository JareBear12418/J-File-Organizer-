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
# pip install PyGTK / pip install giofile / pip install PyPDF2
import sys, os, getpass, subprocess, PyPDF2, re, gio, gtk
from time import sleep
title = ' Work Management'
version = 'v0.1'
width = 800
height = 600
username = getpass.getuser()

current_dir = os.path.dirname(os.path.realpath(__file__))
class MainMenu(QDialog):
    def __init__(self, parent = None):
        super(MainMenu, self).__init__(parent)
        # subprocess.Popen(['test.pdf'],shell=True)
        # creating an object
        self.last_pos_x = 0
        self.last_pos_w = 0
        self.last_size_h = 0
        self.last_size_w = 0
        self.title = title + ' ' + version
        self.width = width
        self.height = height
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
        fs = Folder_Screeen()
        fs.show()

    def createTabs(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Ignored)

        self.gridLayout = QGridLayout()
        # self.gridLayout.addWidget(self.labelFileName, 0, 0)
        # self.gridLayout.addWidget(self.lineEditFileName, 0, 1)
        # self.gridLayout.addWidget(self.labelFilePath, 1, 0)
        # self.gridLayout.addWidget(self.lineEditFilePath, 1, 1)

        self.layout = QVBoxLayout(self)
        self.layout.addLayout(self.gridLayout)
        # self.layout.addWidget(self.treeView)


        # self.layout.addWidget(self.btnAddFile, 0, 0)
        # tabImportHbox.setContentsMargins(5, 5, 5, 5)
        # self.layout.addWidget(self.tree, 1, 0)
        tabImport = QWidget()
        tabImport.setLayout(self.layout)
        # tabImport.setLayout(tabImportHbox)


        # HOME
        tabHome = QWidget()
        self.btnAddConnection = QPushButton('Add', self)

        tabHomehbox = QVBoxLayout()
        tabHomehbox.setContentsMargins(5, 5, 5, 5)
        tabHomehbox.addWidget(self.btnAddConnection)
        # tabHomehbox.addWidget(self.messageText)
        tabHome.setLayout(tabHomehbox)

        self.bottomLeftTabWidget.addTab(tabHome, "&Home")
        self.bottomLeftTabWidget.addTab(tabImport, "&Import")

class Folder_Screeen(QDialog):
    def __init__(self, parent = None):
        super(Folder_Screeen, self).__init__(parent)
        self.width = width
        self.height = height
        self.setMinimumSize(self.width, self.height)
        self.path = expanduser(os.path.dirname(os.path.realpath(__file__)))
        self.pathRoot = QDir.rootPath()

        self.labelFileName = QLabel(self)
        self.labelFileName.setText("Search:")
        self.labelFileName.resize(100, 30)

        self.txtSearch = QLineEdit(self)
        self.txtSearch.textChanged.connect(self.on_textChanged)
        self.thumbnail = QLabel(self)

        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries | QDir.Dirs | QDir.Files)
        self.proxy_model = QSortFilterProxyModel(recursiveFilteringEnabled = True, filterRole = QFileSystemModel.FileNameRole)
        self.proxy_model.setSourceModel(self.model)
        self.model.setReadOnly(False)
        self.model.setNameFilterDisables(False)

        self.indexRoot = self.model.index(self.model.rootPath())

        self.treeView = QTreeView(self)
        self.treeView.setModel(self.proxy_model)
        self.adjust_root_index()
        self.treeView.setRootIndex(self.proxy_model.mapFromSource(self.model.index(self.path)))
        self.treeView.clicked.connect(self.on_treeView_clicked)
        self.treeView.setDragDropMode(QAbstractItemView.InternalMove)
        self.treeView.setAnimated(True)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setEditTriggers(QTreeView.NoEditTriggers)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)

        self.pdfText = QPlainTextEdit(self)
        self.pdfText.setReadOnly(True)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.txtSearch, 1, 0)
        self.gridLayout.addWidget(self.treeView, 3, 0)
        self.gridLayout1 = QGridLayout()
        self.gridLayout1.addWidget(self.pdfText, 0, 1)
        self.gridLayout1.addWidget(self.thumbnail, 1, 1)

        layout = QHBoxLayout(self)
        layout.addLayout(self.gridLayout)
        layout.addLayout(self.gridLayout1)

    # TREE VIEW START ====================================
    def get_icon_filename(self, filename, size):
        #final_filename = "default_icon.png"
        final_filename = ""
        if os.path.isfile(filename):
            # Get the icon name
            file = gio.File(filename)
            file_info = file.query_info('standard::icon')
            file_icon = file_info.get_icon().get_names()[0]
            # Get the icon file path
            icon_theme = gtk.icon_theme_get_default()
            icon_filename = icon_theme.lookup_icon(file_icon, size, 0)
            if icon_filename != None:
                final_filename = icon_filename.get_filename()

        pixmap = QPixmap(final_filename)
        tn = pixmap.scaled(128, 64128, Qt.KeepAspectRatio)
        self.thumbnail.setPixmap(QPixmap(tn))
        self.thumbnail.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        return final_filename


    @QtCore.pyqtSlot(str)
    def on_textChanged(self):
        self.proxy_model.setFilterWildcard("*{}*".format(self.txtSearch.text()))
        self.adjust_root_index()

    def adjust_root_index(self):
        root_index = self.model.index(self.path)
        proxy_index = self.proxy_model.mapFromSource(root_index)
        self.treeView.setRootIndex(proxy_index)
    def btnAddFolder(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"Create Folder", "","All Files (*)", options=options)
        if fileName:
            print(fileName)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if self.lineEditFilePath.text() != '':
                os.remove(self.lineEditFilePath.text())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        fileName = self.model.fileName(indexItem)
        filePath = self.model.filePath(indexItem)

        try:
            get_icon_filename(filePath, 128)
            
            # pixmap = QPixmap(filePath)
            # tn = pixmap.scaled(128, 128, Qt.KeepAspectRatio)
            # self.thumbnail.setPixmap(QPixmap(tn))
            # self.thumbnail.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        except:
            print('not an image')
        if fileName.endswith('.pdf'):
            try:
                with open(filePath, mode = 'rb') as pdfFileObj:
                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    pageObj = pdfReader.getPage(0)
                    self.pdfText.setPlainText(pageObj.extractText())
            except:
                self.pdfText.setPlainText('Error reading "{}"'.format(fileName))
    def dragEnterEvent(self, event):
        m = event.mimeData()
        if m.hasUrls():
            for url in m.urls():
                if url.isLocalFile():
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        if event.source():
            QTreeView.dropEvent(self, event)
        else:
            ix = self.indexAt(event.pos())
            if not self.model().isDir(ix):
                ix = ix.parent()
            pathDir = self.model().filePath(ix)
            m = event.mimeData()
            if m.hasUrls():
                urlLocals = [url for url in m.urls() if url.isLocalFile()]
                accepted = False
                for urlLocal in urlLocals:
                    path = urlLocal.toLocalFile()
                    info = QFileInfo(path)
                    n_path = QDir(pathDir).filePath(info.fileName())
                    o_path = info.absoluteFilePath()
                    if n_path == o_path:
                        continue
                    if info.isDir():
                        QDir().rename(o_path, n_path)
                    else:
                        qfile = QFile(o_path)
                        if QFile(n_path).exists():
                            n_path += "(copy)"
                        qfile.rename(n_path)
                    accepted = True
                if accepted:
                    event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    def showContextMenu(self, point):
        ix = self.treeView.indexAt(point)
        if ix.column() == 0:
            menu = QMenu()
            menu.addAction("Rename")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            if action:
                if action.text() == "Rename":
                    self.treeView.edit(ix)
    # TREE VIEW END ====================================
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

    main = Folder_Screeen()
    main.setWindowTitle(title + ' ' + version)
    main.show()
    sys.exit(app.exec_())
