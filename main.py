# pip install pyqt5
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from PIL import Image
from time import sleep
from pathlib import Path
from requests import Session
from threading import Thread
from functools import partial
from functools import partial
from os.path import expanduser
# pip install PyGTK / pip install giofile / pip install PyPDF2 / pip install PyMuPDF / pip install ezdxf
import sys, os, getpass, subprocess, glob, shutil, PyPDF2, re, json, fitz
title = ' Work Management'
version = 'v0.1'
width = 800
height = 600
username = getpass.getuser()

current_dir = os.path.dirname(os.path.realpath(__file__))
settings_dir = os.path.dirname(os.path.realpath(__file__)) + '/settings/'
files_dir = os.path.dirname(os.path.realpath(__file__)) + '/Files/'
cache_dir = os.path.dirname(os.path.realpath(__file__)) + '/Cache/'
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
# MISC VAR START ==============
last_hovered_file = ''
# MISC VAR EMD ==============
# BATCH Var START ==============
batch_list = []
total_batches = 0
unfinished_batches = 0
# BATCH Var END ==============
all_metal_thicknesses = ['8',
                         '9',
                         '10',
                         '11',
                         '12',
                         '14',
                         '16',
                         '18',
                         '20',
                         '22',
                         '24',
                         '26',
                         '28',
                         '30']
all_metal_thicknesses_inches = [
                                '0.1681',
                                '0.1532',
                                '0.1382',
                                '0.1233',
                                '0.1084',
                                '0.0785',
                                '0.0635',
                                '0.0516',
                                '0.0396',
                                '0.0336',
                                '0.0276',
                                '0.0217',
                                '0.0187',
                                '0.0157']
all_metal_types = ['Steel',
                   'Stainless Steel']
class HoverButton(QPushButton):
    def __init__(self, name, parent=None):
        global last_hovered_file
        QPushButton.__init__(self, name, parent)
        self.name = name
        last_hovered_file = self.name
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        global last_hovered_file
        last_hovered_file = self.name
        # self.parent().lastHoverdButton = self.hoverdButton
        # print(self.name)
class MainMenu(QWidget):
    def __init__(self, parent = None):
        super(MainMenu, self).__init__(parent)
        global last_hovered_file
        # subprocess.Popen(['test.pdf'],shell=True)
        # creating an object
        self.last_pos_x = 0
        self.last_pos_w = 0
        self.last_size_h = 0
        self.last_size_w = 0
        self.title = title + ' ' + version
        self.width = width
        self.height = height
        self.showMaximized()
        # self.lastHoverdButton = last_hovered_file
        self.filePath = ''
        self.fileName = ''
        self.price = ''
        self.pdf_location = ''
        self.mt = ''

        self.createTabs()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

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
        self.metalThickness.setFont(QFont('Calibri', 14))
        self.metalType = QComboBox(self)
        self.metalType.setFont(QFont('Calibri', 14))
        self.txtCutTime = QLineEdit(self)
        self.txtCutTime.setValidator(QDoubleValidator(self))
        self.txtBendTime = QLineEdit(self)
        self.txtBendTime.setValidator(QDoubleValidator(self))
        self.txtWeight = QLineEdit(self)
        self.txtWeight.setValidator(QDoubleValidator(self))
        self.btnImport = QPushButton('Import',self)
        self.btnImport.clicked.connect(self.import_pdf)
        self.btnImportAll = QPushButton('Import All',self)
        self.btnImportAll.clicked.connect(self.import_all_pdf)
        self.pathList = QListWidget(self)
        self.pathList.itemSelectionChanged.connect(self.path_list_clicked)

        self.label = QLabel('Folder:', self)
        self.gridLayoutImport.addWidget(self.label, 0, 0)
        self.folderToImport = QComboBox(self)
        self.folderToImport.setFont(QFont('Calibri', 14))
        self.folderToImport.currentTextChanged.connect(self.verify)
        # dirs = [d for d in os.listdir('Files') if os.path.isdir(os.path.join('Files', d))]
        # dirs = [os.path.join(r,file) for r,d,f in os.walk(files_dir) for file in f]
        # dirs = [os.path.abspath(x) for x in os.listdir(files_dir)]
        # dirs = [d for d in os.listdir('Files') if os.path.isdir(os.path.join('Files', d))]
        global files_dir
        # dirs = [x[0] for x in os.walk(files_dir)]
        # dirs = [fname.rsplit('.', 1)[0] for fname in os.listdir(files_dir)]
        d = files_dir
        dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
        dirs2 = []
        for i, d in enumerate(dirs):
            dirs2.append([os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))])
        flat = [x for sublist in dirs2 for x in sublist]
        flat = dirs + flat
        for i, j in enumerate(flat):
            j = j.replace('\\', '/')
            files_dir = files_dir.replace('\\', '/')
            self.folderToImport.addItem(j)
            self.folderToImport.setItemIcon(i,QIcon('icons/folder.png'))
        self.gridLayoutImport.addWidget(self.folderToImport, 0, 1)


        self.label = QLabel('Thickness:', self)
        self.gridLayoutImport.addWidget(self.label, 1, 0)
        for i, j in enumerate(all_metal_thicknesses):
            self.metalThickness.addItem(j + ' Gauge')
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
        self.gridLayoutButtons2.addWidget(self.btnImportAll, 0, 1)
        self.btnSelectPDF = QPushButton('Select PDF',self)
        self.btnSelectPDF.clicked.connect(self.find_pdf)
        self.gridLayoutButtons2.addWidget(self.btnSelectPDF, 0, 2)

        # ======================== GRID PREVIEW ==========================
        self.gridLayoutPreview = QGridLayout()

        self.previewText.setReadOnly(True)
        self.gridLayoutPreview.addWidget(self.previewText, 0, 0)
        self.thumbnail = QPushButton(self)
        self.thumbnail.setFlat(True)
        self.thumbnail.clicked.connect(self.openImage)
        self.gridLayoutPreview.addWidget(self.thumbnail, 0, 1)
        self.gridLayoutPreview.addWidget(self.pathList, 0, 2)

        self.layout2 = QVBoxLayout(self)
        self.gridLayoutImport.setColumnStretch(3, 3)
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
            self.btnOpen = HoverButton(p,self)
            self.btnOpen.setStyleSheet('text-align: bottom')
            self.btnOpen.setFlat(True)
            # self.btnOpen.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
            # set button context menu policy
            self.btnOpen.setContextMenuPolicy(Qt.CustomContextMenu)
            self.btnOpen.customContextMenuRequested.connect(self.btnOpenContextMenu)

            # create context menu
            self.btnOpenPopup = QMenu(self)
            createFolder = QAction('Add folder', self)
            btnAdd_directory = partial(self.btnAddFolder, True)
            createFolder.triggered.connect(btnAdd_directory)
            self.btnOpenPopup.addAction(createFolder)
            # self.btnOpenPopup.addAction(QAction('Add folder', self))
            # self.btnOpenPopup.addAction(QAction('Delete', self))
            # self.btnOpen.addAction(QAction('test1', self))
            # self.btnOpen.addSeparator()
            # self.btnOpen.addAction(QAction('test2', self))
            self.btnOpen.setIcon(QIcon('icons/folder.png'))
            self.btnOpen.setIconSize(QSize(64,64))
            self.btnOpen.resize(50, 50)
            self.btnOpen.clicked.connect(open_directory)
            self.gridLayoutButtons.addWidget(self.btnOpen, j, k)
            k += 1
            if k > 2:
                k = 0
                j += 1
        # self.btnAddConnection = QPushButton('Add', self)
        # self.btnAddConnection.clicked.connect(self.btnAddFolder)

        tabHomehbox = QVBoxLayout()
        tabHomehbox.addLayout(self.gridLayoutButtons)
        tabHomehbox.setContentsMargins(5, 5, 5, 5)
        # tabHomehbox.addWidget(self.btnAddConnection)
        # tabHomehbox.addWidget(self.messageText)
        tabHome.setLayout(tabHomehbox)
        tabBatches = QWidget()

        f = files_dir.split('/')
        f[0] = f[0].capitalize()
        f = '/'.join(f)
        self.path = f

        self.pathRoot = QDir.rootPath()

        self.labelFileName = QLabel(self)
        self.labelFileName.setText("Search:")
        self.labelFileName.resize(100, 30)

        self.txtSearch = QLineEdit(self)
        self.txtSearch.textChanged.connect(self.on_textChanged)
        self.btnBack = QPushButton('Back', self)
        self.btnBack.clicked.connect(self.back)

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
        self.treeView.doubleClicked.connect(self.treeMedia_doubleClicked)
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
        for i in range(1, self.treeView.model().columnCount()):
            self.treeView.header().hideSection(i)
        self.gridLayout = QGridLayout()
        self.gridLayout.setColumnStretch(1, 4)
        # self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.btnBack, 2, 0)
        self.gridLayout.addWidget(self.txtSearch, 1, 0)
        self.gridLayout.addWidget(self.treeView, 3, 0)
        self.gridLayout1 = QGridLayout()
        # self.gridLayout1.setColumnStretch(1, 4)
        self.progressbar = QProgressBar(self)
        self.lblProgress = QLabel('0/0', self)
        layout = QHBoxLayout(self)
        layout.addLayout(self.gridLayout)
        layout.addLayout(self.gridLayout1)
        self.scroll = QScrollArea(self)
        self.gridLayout1.addWidget(self.scroll, 0, 0)
        self.gridLayout1.addWidget(self.lblProgress, 1, 0)
        self.gridLayout1.addWidget(self.progressbar, 2, 0)
        
        self.scroll.move(7, 80)
        self.scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.scroll.setWidget(self.content)
        self.lay = QGridLayout(self.content)
        # self.grid_batch_names_grid = QGridLayout(self)
        # self.lay.addWidget(self.grid_batch_names_grid, 0, 1)
        tabBatches.setLayout(layout)
        self.bottomLeftTabWidget.addTab(tabHome, "&Home")
        self.bottomLeftTabWidget.addTab(tabImport, "&Import")
        self.bottomLeftTabWidget.addTab(tabBatches, "&Batches")
        self.verify()
    def back(self):
        temp = os.getcwd() + '/Files'
        temp = temp.replace('\\', '/')
        temp = temp.split('/')
        temp[0] = temp[0].capitalize()
        temp = '/'.join(temp)
        if not temp == self.path:
            a = self.path
            a = a.replace('\\', '/')
            a = a.split('/')
            del a[-1]
            a = '/'.join(a)
            self.path = a
            self.filePath = a
            self.setWindowTitle(self.filePath)
            self.adjust_root_index()
    def update_batches(self):
        global total_batches, unfinished_batches
        total_batches += 1
        batch_list.sort()
        # for i, j in enumerate(batch_list):
        #     print(str(i) + ' = ' + str(total_batches))
            # if i < total_batches:
        self.btnName = QPushButton(self)
        button_name = self.fileName
        button_name = button_name.replace('.pdf', '')
        button_name = button_name.replace('.dxf', '')
        self.btnName.setText(button_name + ' - ' + self.mt)
        self.btnName.setFlat(True)
        self.lay.addWidget(self.btnName, total_batches, 1)
            # else:
            #     continue
        self.check_box = QCheckBox(self)
        self.check_box.stateChanged.connect(self.clickBox)
        self.lay.addWidget(self.check_box, total_batches, 0)

        self.lblProgress.setText(str(unfinished_batches) + '/' + str(total_batches))
        self.progressbar.setMaximum(total_batches)
    def clickBox(self, state):
        global unfinished_batches, total_batches
        if state == Qt.Checked:
            unfinished_batches += 1
        else:
            unfinished_batches -= 1
        self.lblProgress.setText(str(unfinished_batches) + '/' + str(total_batches))
        self.progressbar.setValue(unfinished_batches)
        try:
            perc = int(unfinished_batches / total_batches * 100)
            self.setWindowTitle(self.filePath + '  ' + str(perc) + '%')
        except Exception as DivisionByZero:
            self.setWindowTitle(self.filePath + '  ' + str(0) + '%')

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
        global saved_data, paths_list, names_list, folder_list, metal_thickness_list, metal_type_list, cut_time_list, bend_time_list, weight_list, unfinished_batches, total_batches

        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)
        # self.pdf_location = ''
        try:
            perc = int(unfinished_batches / total_batches * 100)
            self.setWindowTitle(self.filePath + '  ' + str(perc) + '%')
        except Exception as DivisionByZero:
            self.setWindowTitle(self.filePath + '  ' + str(0) + '%')
            
        if self.fileName.endswith('.dxf') or self.fileName.endswith('.DXF'):
            new_name = (os.path.splitext(self.fileName)[0])
            output = cache_dir + new_name + ' - dxf.png'
            self.pdf_location = output
        if self.fileName.endswith('.pdf') or self.fileName.endswith('.PDF'):
            new_name = (os.path.splitext(self.fileName)[0])
            output = cache_dir + new_name + ' - pdf.png'
            self.pdf_location = output
        
        for i, j in enumerate(paths_list):
            j = j.replace('\\', '/')
            j = j.split('/')
            j[0] = j[0].capitalize()
            j = '/'.join(j)
            if self.filePath == j:
                self.mt = metal_thickness_list[i]
    def treeMedia_doubleClicked(self,index):
        global batch_list, metal_thickness_list, unfinished_batches, total_batches
        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)
        try:
            perc = int(unfinished_batches / total_batches * 100)
            self.setWindowTitle(self.filePath + '  ' + str(perc) + '%')
        except Exception as DivisionByZero:
            self.setWindowTitle(self.filePath + '  ' + str(0) + '%')
        if not self.fileName.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', 'dfx', 'txt')):
            self.path = self.filePath
            self.adjust_root_index()
        elif self.fileName.lower().endswith(('.pdf', '.dxf')):
            batch_list.append(self.fileName)
            self.update_batches()
    def openImage(self):
        self.vi = view_image(self.pdf_location)
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
            menu.addAction("Create folder")
            menu.addAction("View")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            if action:
                if action.text() == "View":
                    if self.fileName.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', 'dfx')):
                        self.openImage()
                if action.text() == "Create folder":
                    if not self.fileName.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', 'dfx', 'txt')):
                        self.treeView.edit(ix)
    # TREE VIEW END ====================================
    def import_pdf(self):
        global saved_data, paths_list, names_list, folder_list, metal_thickness_list, metal_type_list, cut_time_list, bend_time_list, weight_list
        with open(settings_dir + 'saved_data.json') as file:
            saved_data = json.load(file)
            paths_list.clear()
            names_list.clear()
            folder_list.clear()
            weight_list.clear()
            cut_time_list.clear()
            bend_time_list.clear()
            metal_type_list.clear()
            metal_thickness_list.clear()
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
        folder = self.folderToImport.currentText().replace('\\', '/')
        folder = folder + '/' +  self.metalThickness.currentText()
        for i, j in enumerate(folder_list):
            j = j.replace('\\', '/')
            if folder == j:
                if self.fileName == names_list[i]:
                    buttonReply = QMessageBox.information(self, 'Already Exists', f"{self.fileName} already exists in\n{folder}", QMessageBox.Ok, QMessageBox.Ok)
                    self.pathList.setCurrentRow(self.pathList.currentRow() + 1)
                    return
        passwords_json.append({
            'path': [folder + '/' + self.fileName],
            'name': [self.fileName],
            'folder': [folder], #TODO this
            'thickness': [self.metalThickness.currentText()],
            'type': [self.metalType.currentText()],
            'cut time': [self.txtCutTime.text()],
            'bend time': [self.txtBendTime.text()],
            'weight': [self.txtWeight.text()]
            }
        )
        file_copy_location = folder + '/'
        if not os.path.exists(file_copy_location):
            os.makedirs(file_copy_location)
        shutil.copyfile(self.filePath, file_copy_location + self.fileName)
        # sort json file
        sorted_obj = sorted(passwords_json, key=lambda x : x['name'], reverse=False)
        # Write to passwords file
        with open(settings_dir + 'saved_data.json', mode='w+', encoding='utf-8') as file:
            json.dump(sorted_obj, file, ensure_ascii=True, indent=4, sort_keys=True)

        with open(settings_dir + 'saved_data.json') as file:
            saved_data = json.load(file)
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

        self.pathList.setCurrentRow(self.pathList.currentRow() + 1)
    def import_all_pdf(self):
        global saved_data, paths_list, names_list, folder_list, metal_thickness_list, metal_type_list, cut_time_list, bend_time_list, weight_list
        with open(settings_dir + 'saved_data.json') as file:
            saved_data = json.load(file)
            paths_list.clear()
            names_list.clear()
            folder_list.clear()
            weight_list.clear()
            cut_time_list.clear()
            bend_time_list.clear()
            metal_type_list.clear()
            metal_thickness_list.clear()
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
        readedFileList = [self.pathList.item(i).text() for i in range(self.pathList.count())]

        for i, file_in_list in enumerate(readedFileList):
            self.filePath = file_in_list
            p = Path(self.filePath)
            self.fileName = p.name
            folder = self.folderToImport.currentText().replace('\\', '/')
            for i, j in enumerate(folder_list):
                j = j.replace('\\', '/')
                if folder == j:
                    if self.fileName == names_list[i]:
                        buttonReply = QMessageBox.information(self, 'Already Exists', f"{self.fileName} already exists in\n{folder}", QMessageBox.Ok, QMessageBox.Ok)
                        self.pathList.setCurrentRow(self.pathList.currentRow() + 1)
                        return
            passwords_json.append({
                'path': [folder + '/' + self.fileName],
                'name': [self.fileName],
                'folder': [folder], #TODO this
                'thickness': [self.metalThickness.currentText()],
                'type': [self.metalType.currentText()],
                'cut time': [self.txtCutTime.text()],
                'bend time': [self.txtBendTime.text()],
                'weight': [self.txtWeight.text()]
                }
            )
            file_copy_location = folder + '/' + self.metalThickness.currentText() + '/'
            if not os.path.exists(file_copy_location):
                os.makedirs(file_copy_location)
            shutil.copyfile(self.filePath, file_copy_location + self.fileName)
            self.pathList.setCurrentRow(readedFileList.index(self.filePath))
            # sort json file
            sorted_obj = sorted(passwords_json, key=lambda x : x['name'], reverse=False)
            # Write to passwords file
            with open(settings_dir + 'saved_data.json', mode='w+', encoding='utf-8') as file:
                json.dump(sorted_obj, file, ensure_ascii=True, indent=4, sort_keys=True)

            with open(settings_dir + 'saved_data.json') as file:
                saved_data = json.load(file)
                paths_list.clear()
                names_list.clear()
                folder_list.clear()
                weight_list.clear()
                cut_time_list.clear()
                bend_time_list.clear()
                metal_type_list.clear()
                metal_thickness_list.clear()
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
    def verify(self):
        self.filePath = self.filePath.replace('\\', '/')

        self.previewText.setFont(QFont('Calibri', 16))
        self.previewText.setPlainText(f"""File Name: {self.fileName}\nFile Path: {self.filePath}\n\nDestination: {self.folderToImport.currentText() + '/' + self.metalThickness.currentText()}\n\nSelected Metal Thickness: {self.metalThickness.currentText()}\nSelected Metal Type: {self.metalType.currentText()}\n\nCut Time: {self.txtCutTime.text()}\nBend Time: {self.txtBendTime.text()}\nWeight: {self.txtWeight.text()}\n\nPrice: {self.price}""")
        if self.txtBendTime.text() == '' or self.txtCutTime.text() == '' or self.txtWeight.text() == '' or self.fileName == '' or self.filePath == '':
            self.btnImport.setEnabled(False)
            self.btnImportAll.setEnabled(False)
        else:
            self.btnImport.setEnabled(True)
            self.btnImportAll.setEnabled(True)
    def openImage(self):
        self.vi = view_image(self.pdf_location)
        self.vi.show()
    def find_pdf(self):
        filePath, _ = QFileDialog.getOpenFileNames(self,"Your PDF", "","Portable Document File(*.pdf)")
        if filePath:
            for i, j in enumerate(filePath):
                self.pathList.setFont(QFont('Calibri', 16))
                self.pathList.insertItem(i, j)
                self.filePath = j
                self.verify()
            self.pathList.setCurrentRow(0)
    def path_list_clicked(self):
        try:
            item = self.pathList.currentItem()
            self.filePath = item.text()
            p = Path(self.filePath)
            self.fileName = p.name
            new_name = (os.path.splitext(self.fileName)[0])
            output = cache_dir + new_name + ' - pdf.png'
            self.pdf_location = output
            if not os.path.exists(output):
                pdffile = self.filePath
                doc = fitz.open(pdffile)
                page = doc.loadPage(0) #number of page
                pix = page.getPixmap()
                pix.writePNG(output)
                pixmap = QPixmap(output)
                tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                self.thumbnail.setIcon(QIcon(tn))
                self.thumbnail.setIconSize(QSize(512,512))
            else:
                pixmap = QPixmap(output)
                tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                self.thumbnail.setIcon(QIcon(tn))
                self.thumbnail.setIconSize(QSize(512,512))
            self.verify()
        except:
            print('No more elements')
    def open_tree_directory(self, directory):
        self.fs = Folder_Screeen(directory)
        self.fs.show()
        self.close()
    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        createFolder = QAction('Create Folder', self)
        btnAdd_directory = partial(self.btnAddFolder, False)
        createFolder.triggered.connect(btnAdd_directory)
        self.menu.addAction(createFolder)
        # add other required actions
        self.menu.popup(QCursor.pos())
    def btnDeleteFolder(self):
        text, okPressed = QInputDialog.getText(self, "Folder name","Name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            if os.path.exists(files_dir + text):
                shutil.rmtree(files_dir + text, ignore_errors=True)
                self.mm = MainMenu()
                self.mm.show()
                self.close()
            else:
                buttonReply = QMessageBox.warning(self, 'Doesn\'t Exist', f"\"{text}\" Doesn\'t Exist", QMessageBox.Ok, QMessageBox.Ok)
                return
    def btnAddFolder(self, create_file):
        # print(direc)
        print(last_hovered_file)
        text, okPressed = QInputDialog.getText(self, "Folder name","Name:", QLineEdit.Normal, "New Folder")
        print(text)
        if okPressed and text != '':
            if create_file == False:
                if not os.path.exists(files_dir + text):
                    os.makedirs(files_dir  + text)
                    self.mm = MainMenu()
                    self.mm.show()
                    self.close()
                else:
                    buttonReply = QMessageBox.warning(self, 'Already Exists', f"\"{text}\" Already Exists", QMessageBox.Ok, QMessageBox.Ok)
                    return
            else:
                if not os.path.exists(files_dir + last_hovered_file + '/' + text):
                    os.makedirs(files_dir + last_hovered_file + '/' + text)
                    self.mm = MainMenu()
                    self.mm.show()
                    self.close()
                else:
                    buttonReply = QMessageBox.warning(self, 'Already Exists', f"\"{last_hovered_file}\" Already Exists", QMessageBox.Ok, QMessageBox.Ok)
                    return
    def btnOpenContextMenu(self, point):
        self.btnOpenPopup.exec_(QCursor.pos())
class Folder_Screeen(QWidget):
    def __init__(self, directory_to_open, parent = None):
        super(Folder_Screeen, self).__init__(parent)
        self.fileName = ''
        self.filePath = ''
        self.width = width
        self.height = height
        directory_to_open = directory_to_open.replace("\\", "/")
        self.showMaximized()

        directory_to_open = directory_to_open.replace('\\', '/')
        directory_to_open = directory_to_open.split('/')
        directory_to_open[0] = directory_to_open[0].capitalize()
        directory_to_open = '/'.join(directory_to_open)
        self.setWindowTitle(directory_to_open)

        self.last_directory = directory_to_open
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
        self.btnBack = QPushButton('Back', self)
        self.btnBack.clicked.connect(self.back)

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
        self.treeView.doubleClicked.connect(self.treeMedia_doubleClicked)
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
        for i in range(1, self.treeView.model().columnCount()):
            self.treeView.header().hideSection(i)
        self.pdfText = QPlainTextEdit(self)
        self.pdfText.setReadOnly(True)

        self.gridLayout = QGridLayout()
        self.gridLayout.setColumnStretch(1, 4)
        # self.gridLayout.setRowStretch(0, 2)
        self.gridLayout.addWidget(self.labelFileName, 0, 0)
        self.gridLayout.addWidget(self.btnBack, 2, 0)
        self.gridLayout.addWidget(self.txtSearch, 1, 0)
        self.gridLayout.addWidget(self.treeView, 3, 0)
        self.gridLayout.addWidget(self.pdfText, 3, 1)
        self.gridLayout1 = QGridLayout()
        self.gridLayout1.addWidget(self.thumbnail, 0, 1)

        layout = QHBoxLayout(self)
        layout.addLayout(self.gridLayout)
        layout.addLayout(self.gridLayout1)

    def back(self):
        temp = os.getcwd() + '/Files'
        temp = temp.replace('\\', '/')
        temp = temp.split('/')
        temp[0] = temp[0].capitalize()
        temp = '/'.join(temp)
        if not temp == self.path:
            a = self.path
            a = a.replace('\\', '/')
            a = a.split('/')
            del a[-1]
            a = '/'.join(a)
            self.path = a
            self.filePath = a
            self.setWindowTitle(self.filePath)
            self.adjust_root_index()
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
        global saved_data, paths_list, names_list, folder_list, metal_thickness_list, metal_type_list, cut_time_list, bend_time_list, weight_list

        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)
        self.pdf_location = ''
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
                new_name = (os.path.splitext(self.fileName)[0])
                output = cache_dir + new_name + ' - dxf.png'
                if not os.path.exists(output):
                    os.popen(f'dia \"{self.filePath}\" -e \"{output}\"')
                    from PyQt5 import QtTest
                    QtTest.QTest.qWait(1000)
                    pixmap = QPixmap(output)
                    tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                    # self.thumbnail.setPixmap(QPixmap(tn))
                    self.thumbnail.setIcon(QIcon(tn))
                    self.thumbnail.setIconSize(QSize(512,512))
                else:
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
                    new_name = (os.path.splitext(self.fileName)[0])
                    output = cache_dir + new_name + ' - pdf.png'
                    self.pdf_location = output
                    for i, j in enumerate(paths_list):
                        j = j.replace('\\', '/')
                        j = j.split('/')
                        j[0] = j[0].capitalize()
                        j = '/'.join(j)
                        if self.filePath == j:
                            self.price = ''
                            n = folder_list[i].split('/')
                            n[0] = n[0].capitalize()
                            n = '/'.join(n)
                            j = j.replace(n + '/', '')
                            m = paths_list[i].split('/')
                            m[0] = m[0].capitalize()
                            m = '/'.join(m)
                            self.pdfText.setPlainText(f"""File Name: {j}\nFile Path: {m}\n\nDestination: {n}\n\nSelected Metal Thickness: {metal_thickness_list[i]}\nSelected Metal Type: {metal_type_list[i]}\n\nCut Time: {cut_time_list[i]}\nBend Time: {bend_time_list[i]}\nWeight: {weight_list[i]}\n\nPrice: {self.price}""")
                    if not os.path.exists(output):
                        pdffile = self.filePath
                        doc = fitz.open(pdffile)
                        page = doc.loadPage(0) #number of page
                        pix = page.getPixmap()
                        # output = "outfile.png"
                        pix.writePNG(output)

                        pixmap = QPixmap(output)
                        tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                        # self.thumbnail.setPixmap(QPixmap(tn))
                        self.thumbnail.setIcon(QIcon(tn))
                        self.thumbnail.setIconSize(QSize(512,512))
                        # self.thumbnail.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
                    else:
                        pixmap = QPixmap(output)
                        tn = pixmap.scaled(512, 512, Qt.KeepAspectRatio)
                        # self.thumbnail.setPixmap(QPixmap(tn))
                        self.thumbnail.setIcon(QIcon(tn))
                        self.thumbnail.setIconSize(QSize(512,512))
                    # self.pdfText.setPlainText(pageObj.extractText())
            except:
                self.pdfText.setPlainText('Error reading "{}"'.format(self.fileName))
    def treeMedia_doubleClicked(self,index):
        source_index = self.proxy_model.mapToSource(index)
        indexItem = self.model.index(source_index.row(), 0, source_index.parent())
        self.fileName = self.model.fileName(indexItem)
        self.filePath = self.model.filePath(indexItem)
        self.setWindowTitle(self.filePath)

        if not self.fileName.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', 'dfx', 'txt')):
            self.path = self.filePath
            self.adjust_root_index()
            # root_index = self.model.index(self.path)
        elif self.fileName.lower().endswith(('.pdf', '.dfx')):
            self.openImage()
    def openImage(self):
        self.vi = view_image(self.pdf_location)
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
            menu.addAction("Delete")
            action = menu.exec_(self.treeView.mapToGlobal(point))
            if action:
                if action.text() == "Rename":
                    self.treeView.edit(ix)
                if action.text() == "Delete":
                    if os.path.exists(self.filePath):
                        try:
                            os.remove(self.filePath)
                        except Exception as e:
                            buttonReply = QMessageBox.critical(self, 'Error!', "Need Administrator privileges to delete files.", QMessageBox.Ok, QMessageBox.Ok)
                            return
                    else:
                        buttonReply = QMessageBox.warning(self, 'Error!', f"\"{self.fileName}\" Doesn\'t Exist", QMessageBox.Ok, QMessageBox.Ok)
                        return
    # TREE VIEW END ====================================

    def closeEvent(self, event):
        self.mm = MainMenu()
        self.mm.setWindowTitle(title + ' ' + version)
        self.mm.show()
        self.close()
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
        directory_to_open = directory_to_open.replace('\\','/')
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
        self.viewer.setPhoto(QPixmap(self.image_to_open))
        self.showMaximized()

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

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

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

    main = MainMenu()
    main.setWindowTitle(title + ' ' + version)
    main.show()
    sys.exit(app.exec_())
