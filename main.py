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
from functools import partial
from PIL import Image
from time import sleep
from pathlib import Path
# pip install PyGTK / pip install giofile / pip install PyPDF2 / pip install PyMuPDF / pip install ezdxf
import sys, os, getpass, subprocess, PyPDF2, re, json, fitz, ezdxf, glob
title = ' Work Management'
version = 'v0.1'
width = 1000
height = 800
username = getpass.getuser()

current_dir = os.path.dirname(os.path.realpath(__file__))
settings_dir = os.path.dirname(os.path.realpath(__file__)) + '/settings/'
files_dir = os.path.dirname(os.path.realpath(__file__)) + '/Files/'
# JSON DATA START ================
saved_data = ''
paths_list = []
names_list = []
folder_list = []
metal_thickness_list = []
metal_type_list = []
cut_time_list = []
bend_time_list = []
weight_list = []
# price_list = []
# JSON DATA END ================


all_metal_thicknesses = ['8',
                         '9',
                         '10',
                         '11',
                         '12',
                         '13',
                         '14',
                         '15',
                         '16',
                         '17',
                         '18',
                         '19',
                         '20',
                         '21',
                         '22',
                         '23',
                         '24',
                         '25',
                         '26',
                         '27',
                         '28',
                         '29',
                         '30'
                         ]
all_metal_types = ['Steel',
                   'Stainless Steel']
class MainMenu(QWidget):
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


        self.filePath = ''
        self.fileName = ''
        self.price = ''


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

    def createTabs(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        # ==================================== IMPORT ========================================
        # ======================== GRID IMPORT ==========================
        self.gridLayoutImport = QGridLayout()
        self.gridLayoutImport.setColumnStretch(0, 0)
        self.gridLayoutImport.setColumnStretch(0, 0)
        self.gridLayoutImport.setRowStretch(0, 0)
        self.gridLayoutImport.setRowStretch(0, 0)
        self.previewText = QPlainTextEdit(self)
        self.metalThickness = QComboBox(self)
        self.metalType = QComboBox(self)
        self.txtCutTime = QLineEdit(self)
        self.txtCutTime.setValidator(QDoubleValidator(self))
        self.txtBendTime = QLineEdit(self)
        self.txtBendTime.setValidator(QDoubleValidator(self))
        self.txtWeight = QLineEdit(self)
        self.txtWeight.setValidator(QDoubleValidator(self))
        self.btnImport = QPushButton('Import',self)
        self.btnImport.clicked.connect(self.import_pdf)

        # dirs = [d for d in os.listdir('Files') if os.path.isdir(os.path.join('Files', d))]
        dirs = [os.path.abspath(x) for x in os.listdir(files_dir)]
        # dirs = [os.path.join(r,file) for r,d,f in os.walk(files_dir) for file in f]
        self.label = QLabel('Folder:', self)
        self.gridLayoutImport.addWidget(self.label, 0, 0)
        self.folderToImport = QComboBox(self)
        self.folderToImport.currentTextChanged.connect(self.verify)
        for i, j in enumerate(dirs):
            self.folderToImport.addItem(j)
            self.folderToImport.setItemIcon(i,QIcon('icons/folder.png'))
        self.gridLayoutImport.addWidget(self.folderToImport, 0, 1)

        self.label = QLabel('Thickness:', self)
        self.gridLayoutImport.addWidget(self.label, 1, 0)
        for i, j in enumerate(all_metal_thicknesses):
            self.metalThickness.addItem(j)
        self.metalThickness.currentTextChanged.connect(self.verify)
        self.gridLayoutImport.addWidget(self.metalThickness, 1, 1)

        self.label = QLabel('Type:', self)
        self.gridLayoutImport.addWidget(self.label, 2, 0)
        for i, j in enumerate(all_metal_types):
            self.metalType.addItem(j)
        self.metalType.currentTextChanged.connect(self.verify)
        self.gridLayoutImport.addWidget(self.metalType, 2, 1)

        self.label = QLabel('Cut Time:', self)
        self.gridLayoutImport.addWidget(self.label, 3, 0)
        self.txtCutTime.textChanged.connect(self.verify)
        self.gridLayoutImport.addWidget(self.txtCutTime, 3, 1)

        self.label = QLabel('Bend Time:', self)
        self.gridLayoutImport.addWidget(self.label, 4, 0)
        self.txtBendTime.textChanged.connect(self.verify)
        self.gridLayoutImport.addWidget(self.txtBendTime, 4, 1)

        self.label = QLabel('Weight:', self)
        self.gridLayoutImport.addWidget(self.label, 5, 0)
        self.txtWeight.textChanged.connect(self.verify)
        self.gridLayoutImport.addWidget(self.txtWeight, 5, 1)

        self.gridLayoutButtons2 = QGridLayout()
        self.gridLayoutButtons2.addWidget(self.btnImport, 0, 0)
        self.btnSelectPDF = QPushButton('Select PDF',self)
        self.btnSelectPDF.clicked.connect(self.find_pdf)
        self.gridLayoutButtons2.addWidget(self.btnSelectPDF, 0, 1)
        # self.gridLayoutImpor.addWidget(self.btnImport, 5, 0)

        # ======================== GRID PREVIEW ==========================
        self.gridLayoutPreview = QGridLayout()

        self.previewText.setReadOnly(True)
        self.gridLayoutPreview.addWidget(self.previewText, 0, 0)
        self.thumbnail = QPushButton(self)
        self.thumbnail.setFlat(True)
        self.thumbnail.clicked.connect(self.openImage)
        self.gridLayoutPreview.addWidget(self.thumbnail, 0, 1)

        self.layout2 = QVBoxLayout(self)
        self.layout2.addLayout(self.gridLayoutImport)
        self.layout2.addLayout(self.gridLayoutPreview)
        self.layout2.addLayout(self.gridLayoutButtons2)
        self.layout2.setContentsMargins(5, 5, 5, 5)

        tabImport = QWidget()
        tabImport.setLayout(self.layout2)
        # tabImport.setLayout(tabImportHbox)

        # ====================================== HOME ==================================
        self.gridLayoutButtons = QGridLayout()
        self.gridLayoutButtons.setColumnStretch(3, 3)
        tabHome = QWidget()
        j = 0
        k = 0
        dirs = [d for d in os.listdir('Files') if os.path.isdir(os.path.join('Files', d))]
        for i, p in enumerate(dirs):
            p = files_dir + dirs[i]
            open_directory = partial(self.open_tree_directory, p)
            p = p.replace(files_dir, '')
            self.btnOpen = QPushButton(p, self)
            self.btnOpen.setIcon(QIcon('icons/folder.png'))
            self.btnOpen.setIconSize(QSize(64,64))
            self.btnOpen.resize(50, 50)
            self.btnOpen.clicked.connect(open_directory)
            self.gridLayoutButtons.addWidget(self.btnOpen, j, k, 1, 1)
            k += 1
            if k > 2:
                k = 0
                j += 1
        self.btnAddConnection = QPushButton('Add', self)
        self.btnAddConnection.clicked.connect(self.btnAddFolder)

        tabHomehbox = QVBoxLayout()
        tabHomehbox.addLayout(self.gridLayoutButtons)
        tabHomehbox.setContentsMargins(5, 5, 5, 5)
        tabHomehbox.addWidget(self.btnAddConnection)
        # tabHomehbox.addWidget(self.messageText)
        tabHome.setLayout(tabHomehbox)

        self.bottomLeftTabWidget.addTab(tabHome, "&Home")
        self.bottomLeftTabWidget.addTab(tabImport, "&Import")
    def import_pdf(self):
        global saved_data, paths_list, names_list, folder_list, metal_thickness_list, metal_type_list, cut_time_list, bend_time_list, weight_list
        passwords_json.append({
            'path': [self.filePath],
            'name': [self.fileName],
            'folder': [self.folderToImport.currentText()], #TODO this
            'thickness': [self.metalThickness.currentText()],
            'type': [self.metalType.currentText()],
            'cut time': [self.txtCutTime.text()],
            'bend time': [self.txtBendTime.text()],
            'weight': [self.txtWeight.text()]
            }
        )
        # sort json file
        sorted_obj = sorted(passwords_json, key=lambda x : x['name'], reverse=False)
        # Write to passwords file
        with open(settings_dir + 'saved_data.json', mode='w+', encoding='utf-8') as file:
            json.dump(sorted_obj, file, ensure_ascii=True, indent=4, sort_keys=True)

    def verify(self):
        self.filePath = self.filePath.replace('\\', '/')
        self.previewText.setPlainText(f"""Preview:
PDF Path: {self.filePath}
PDF Name: {self.fileName}

Selected Folder: {self.folderToImport.currentText()}
Selected Metal Thickness: {self.metalThickness.currentText()}
Selected Metal Type: {self.metalType.currentText()}

Cut Time: {self.txtCutTime.text()}
Bend Time: {self.txtBendTime.text()}
Weight: {self.txtWeight.text()}
Price: {self.price}
""")
        if self.txtBendTime.text() == '' or self.txtCutTime.text() == '' or self.txtWeight.text() == '' or self.fileName == '' or self.filePath == '':
            self.btnImport.setEnabled(False)
        else:
            self.btnImport.setEnabled(True)
    def openImage(self):
        self.vi = view_image(self.filePath)
        self.vi.show()
    def find_pdf(self):
        filePath, _ = QFileDialog.getOpenFileName(self,"Your PDF", "","Portable Document File(*.pdf)")
        if filePath:
            self.filePath = filePath
            p = Path(self.filePath)
            self.fileName = p.name
            pdffile = self.filePath
            doc = fitz.open(pdffile)
            page = doc.loadPage(0) #number of page
            pix = page.getPixmap()
            output = "outfile.png"
            pix.writePNG(output)
            pixmap = QPixmap(output)
            tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
            # self.thumbnail.setPixmap(QPixmap(tn))
            self.thumbnail.setIcon(QIcon(tn))
            self.thumbnail.setIconSize(QSize(512,512))
            self.verify()
        # directory = QFileDialog.getExistingDirectory(None,
        #     "Select Directory",
        #     QDir.currentPath())
        # print(directory)
        # options = QFileDialog.Options()
        # fileName, _ = QFileDialog.getOpenFileName(self,"Your PDF", "","Portable Document File(*.pdf)", options=options)
        # if fileName:
        #     print(fileName)

    def open_tree_directory(self, directory):
        self.fs = Folder_Screeen(directory)
        self.fs.show()
    def btnAddFolder(self):
        text, okPressed = QInputDialog.getText(self, "Folder name","Name:", QLineEdit.Normal, "New Folder")
        if okPressed and text != '':
            print(text)
            if not os.path.exists(files_dir + text):
                os.makedirs(files_dir + text)
        # options = QFileDialog.Options()
        # fileName, _ = QFileDialog.getOpenFileName(self,"Create Folder", "","All Files (*)", options=options)
        # if fileName:
        #     print(fileName)
class Folder_Screeen(QWidget):
    def __init__(self, directory_to_open, parent = None):
        super(Folder_Screeen, self).__init__(parent)
        self.fileName = ''
        self.filePath = ''
        self.width = width
        self.height = height
        directory_to_open = directory_to_open.replace("\\", "/")
        self.setWindowTitle(directory_to_open)
        self.setMinimumSize(self.width, self.height)

        self.path = directory_to_open
        self.pathRoot = QDir.rootPath()

        self.labelFileName = QLabel(self)
        self.labelFileName.setText("Search:")
        self.labelFileName.resize(100, 30)

        self.txtSearch = QLineEdit(self)
        self.txtSearch.textChanged.connect(self.on_textChanged)
        self.thumbnail = QPushButton(self)
        self.thumbnail.setFlat(True)
        self.thumbnail.clicked.connect(self.openImage)

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

        self.treeView.setRootIndex(self.indexRoot)
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


    @QtCore.pyqtSlot(str)
    def on_textChanged(self):
        self.proxy_model.setFilterWildcard("*{}*".format(self.txtSearch.text()))
        self.adjust_root_index()

    def adjust_root_index(self):
        root_index = self.model.index(self.path)
        proxy_index = self.proxy_model.mapFromSource(root_index)
        self.treeView.setRootIndex(proxy_index)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            if self.lineEditFilePath.text() != '':
                os.remove(self.lineEditFilePath.text())

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def on_treeView_clicked(self, index):
        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)
        self.setWindowTitle(self.filePath)
        try:
            pixmap = QPixmap(self.filePath)
            tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
            self.thumbnail.setIcon(QIcon(tn))
            # self.button.setIconSize(QtCore.QSize(24,24))
            # self.thumbnail.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        except:
            print('not an image')
        if self.fileName.endswith('.dxf') or self.fileName.endswith('.DXF'):
            try:
                os.popen(f'dia \"{self.filePath}\" -e outfile.png')
                from PyQt5 import QtTest
                QtTest.QTest.qWait(1000)
                output = "outfile.png"
                pixmap = QPixmap(output)
                tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                # self.thumbnail.setPixmap(QPixmap(tn))
                self.thumbnail.setIcon(QIcon(tn))
                self.thumbnail.setIconSize(QSize(512,512))
            except:
                self.pdfText.setPlainText('Error reading "{}"'.format(self.fileName))

        if self.fileName.endswith('.pdf') or self.fileName.endswith('.PDF'):
            try:
                with open(self.filePath, mode = 'rb') as pdfFileObj:
                    pdffile = self.filePath
                    doc = fitz.open(pdffile)
                    page = doc.loadPage(0) #number of page
                    pix = page.getPixmap()
                    output = "outfile.png"
                    pix.writePNG(output)

                    pixmap = QPixmap(output)
                    tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                    # self.thumbnail.setPixmap(QPixmap(tn))
                    self.thumbnail.setIcon(QIcon(tn))
                    self.thumbnail.setIconSize(QSize(512,512))
                    # self.thumbnail.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

                    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    pageObj = pdfReader.getPage(0)
                    self.pdfText.setPlainText(pageObj.extractText())
            except:
                self.pdfText.setPlainText('Error reading "{}"'.format(self.fileName))

    def openImage(self):
        self.vi = view_image(self.filePath)
        self.vi.show()
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
        self.on_treeView_clicked(ix)
        if ix.column() == 0:
            menu = QMenu()
            menu.addAction("Rename")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            if action:
                if action.text() == "Rename":
                    self.treeView.edit(ix)
    # TREE VIEW END ====================================
# class view_iamge(QWidget):
class PhotoViewer(QtWidgets.QGraphicsView):
    photoClicked = pyqtSignal(QPoint)
    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 100
        self._empty = True
        self._scene = QGraphicsScene(self)
        self._photo = QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        self.setFrameShape(QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 100
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QGraphicsView.NoDrag)
            self._photo.setPixmap(QPixmap())
        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
        super(PhotoViewer, self).mousePressEvent(event)


class view_image(QtWidgets.QWidget):
    def __init__(self, directory_to_open):
        super(view_image, self).__init__()
        self.image_to_open = directory_to_open
        self.setWindowTitle(directory_to_open)
        self.viewer = PhotoViewer(self)
        # self.resize(width, height)
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(0, 0, rect.width(), rect.height())
        self.viewer.photoClicked.connect(self.photoClicked)
        # Arrange layout
        VBlayout = QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QHBoxLayout()
        HBlayout.setAlignment(Qt.AlignLeft)
        VBlayout.addLayout(HBlayout)
        self.loadImage()

    def loadImage(self):
        self.viewer.setPhoto(QPixmap('outfile.png'))

    def pixInfo(self):
        self.viewer.toggleDragMode()

    def photoClicked(self, pos):
        if self.viewer.dragMode()  == QGraphicsView.NoDrag:
            self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))
if __name__ == '__main__':
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)


    if not os.path.exists(files_dir):
        os.makedirs(files_dir)

    if os.path.exists(settings_dir + 'saved_data.json'):
        with open(settings_dir + 'saved_data.json') as file:
            passwords_json = json.load(file)
            for info in passwords_json:
                for path in info['path']:
                    paths_list.append(path)
                for name in info['name']:
                    names_list.append(name)
                for folder in info['folder']:
                    folder_list.append(folder)
                for thickness in info['thickness']:
                    metal_thickness_list.append(thickness)
                for metal_type in info['type']:
                    metal_type_list.append(metal_type)
                for cut_time in info['cut time']:
                    cut_time_list.append(cut_time)
                for bend_time in info['bend time']:
                    bend_time_list.append(bend_time)
                for weight in info['weight']:
                    weight_list.append(weight)
    elif not os.path.exists(settings_dir + 'saved_data.json'):
        file = open(settings_dir + "saved_data.json", "w+")
        file.write("[]")
        file.close()
        with open(settings_dir + 'saved_data.json') as file:
            saved_data = json.load(file)
    app = QApplication(sys.argv)
    # app.setStyle('Fusion')

    # palette = QPalette()
    # palette.setColor(QPalette.Window, QColor(35, 35, 35))
    # palette.setColor(QPalette.WindowText, Qt.white)
    # palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    # palette.setColor(QPalette.ToolTipBase, Qt.white)
    # palette.setColor(QPalette.ToolTipText, Qt.white)
    # palette.setColor(QPalette.Text, Qt.white)
    # palette.setColor(QPalette.Button, QColor(53, 53, 53))
    # palette.setColor(QPalette.ButtonText, Qt.white)
    # palette.setColor(QPalette.BrightText, Qt.red)
    # palette.setColor(QPalette.Link, QColor(42, 130, 218))
    # palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # palette.setColor(QPalette.HighlightedText, Qt.black)
    # app.setPalette(palette)

    main = MainMenu()
    main.setWindowTitle(title + ' ' + version)
    main.show()
    sys.exit(app.exec_())
