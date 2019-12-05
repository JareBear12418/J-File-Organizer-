from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
import os, sys
class TreeDelegate(QtWidgets.QStyledItemDelegate):
    buttonClicked = pyqtSignal(QModelIndex)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mousePos = None
        self._pressed = False
        self.buttonWidth = 32
        self.buttonIcon = QIcon('some icon')

    def editorEvent(self, event, model, option, index):
        if event.type() in (QEvent.Enter, QEvent.MouseMove):
            self._mousePos = event.pos()
            # request an update of the current index
            option.widget.update(index)
        elif event.type() == QEvent.Leave:
            self._mousePos = None
        elif event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # check that the click is within the virtual button rectangle; note
            # that the option rect shouldn't be touched, so we create a new one
            # based on it
            rect = QRect(option.rect)
            rect.setLeft(rect.right() - self.buttonWidth)
            if event.pos() in rect:
                self._pressed = True
            option.widget.update(index)
        elif event.type() == QEvent.MouseButtonRelease:
            if self._pressed and event.button() == Qt.LeftButton:
                rect = QRect(option.rect)
                rect.setLeft(rect.right() - self.buttonWidth)
                # emit the click only if the release is within the button rect
                if event.pos() in rect:
                    self.buttonClicked.emit(index)
            self._pressed = False
            option.widget.update(index)
        return super().editorEvent(event, model, option, index)


    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        if index.isValid():
            proxy = index.model()
            fsModel = proxy.sourceModel()
            # map the proxy index to the fsModel
            srcIndex = proxy.mapToSource(index)
            # I'm just checking if it's a file, if you want to check the extension
            # you might need to use fsModel.fileName(srcIndex)
            if not fsModel.isDir(srcIndex):
                btnOption = QStyleOptionButton()
                btnOption.text = 'hi'
                # initialize the basic options with the view
                btnOption.initFrom(option.widget)
                # you can also use fsModel.fileIcon(srcIndex)
                btnOption.icon = self.buttonIcon
                # as before, create a new rectangle
                btnOption.rect = QRect(option.rect)
                btnOption.rect.setLeft(option.rect.right() - self.buttonWidth)
                # remove the focus rectangle, as it will be inherited from the view
                btnOption.state &= ~QStyle.State_HasFocus
                if self._mousePos and self._mousePos in btnOption.rect:
                    # if the style supports it, some kind of "glowing" border
                    # will be shown on the button
                    btnOption.state |= QStyle.State_MouseOver
                    if self._pressed == Qt.LeftButton:
                        # set the button pressed state
                        btnOption.state |= QStyle.State_On
                else:
                    # ensure that there's no mouse over state (see above)
                    btnOption.state &= ~QStyle.State_MouseOver

                # finally, draw the virtual button
                option.widget.style().drawControl(QStyle.CE_PushButton, btnOption, painter)


class MainMenu(QWidget):
    def __init__(self, parent = None):
        super(MainMenu, self).__init__(parent)
        
        self.treeView = QTreeView(self)
        self.treeView.resize(800,400)
        self.treeView.setMouseTracking(True)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllEntries | QDir.Dirs | QDir.Files)
        self.proxy_model = QSortFilterProxyModel(recursiveFilteringEnabled = True, filterRole = QFileSystemModel.FileNameRole)
        self.proxy_model.setSourceModel(self.model)
        self.model.setReadOnly(False)
        self.model.setNameFilterDisables(False)

        self.indexRoot = self.model.index(self.model.rootPath())
        self.treeView.setModel(self.proxy_model)

        self.treeView.setRootIndex(self.indexRoot)
        self.treeView.setAnimated(True)
        self.treeView.setIndentation(20)
        self.treeView.setSortingEnabled(True)
        self.treeView.setDragEnabled(False)
        self.treeView.setAcceptDrops(False)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setEditTriggers(QTreeView.NoEditTriggers)
        self.treeDelegate = TreeDelegate()
        self.treeView.setItemDelegateForColumn(0, self.treeDelegate)
        # self.treeDelegate.setText('press me :)')
        self.treeDelegate.buttonClicked.connect(self.treeButtonClicked)
        
        for i in range(1, self.treeView.model().columnCount()):
            self.treeView.header().hideSection(i)


    def treeButtonClicked(self, index):
        print('{} clicked'.format(index.data()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainMenu()
    main.show()
    sys.exit(app.exec_())
