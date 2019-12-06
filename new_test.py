from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
import os, sys
class TreeDelegate(QtWidgets.QStyledItemDelegate):
    buttonClicked = pyqtSignal(QModelIndex, int)

    def __init__(self, fsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fsModel = fsModel

        self.clickedPaths = {}
        self._mousePos = None
        self._pressed = False
        self.minimumButtonWidth = 32

    def getOption(self, option, index):
        btnOption = QStyleOptionButton()
        # initialize the basic options with the view
        btnOption.initFrom(option.widget)

        clickedCount = self.clickedPaths.get(self.fsModel.filePath(index), 0)
        if clickedCount == 0:
            btnOption.text = 'Cutting'
        elif clickedCount == 1:
            btnOption.text = 'Picking'
        elif clickedCount == 2:
            btnOption.text = 'Bending'
        elif clickedCount == 3:
            btnOption.text = 'Painting'
        elif clickedCount == 4:
            btnOption.text = 'Assembly'
        elif clickedCount >= 5:
            btnOption.text = 'Complete'
        else:
            btnOption.text = 'Cutting'

        # the original option properties should never be touched, so we can't
        # directly use it's "rect"; let's create a new one from it
        btnOption.rect = QRect(option.rect)

        # adjust it to the minimum size
        btnOption.rect.setLeft(option.rect.right() - self.minimumButtonWidth)

        style = option.widget.style()
        # get the available space for the contents of the button
        textRect = style.subElementRect(
            QStyle.SE_PushButtonContents, btnOption)
        # get the margins between the contents and the border, multiplied by 2
        # since they're used for both the left and right side
        margin = style.pixelMetric(
            QStyle.PM_ButtonMargin, btnOption) * 2

        # the width of the current button text
        textWidth = btnOption.fontMetrics.width(btnOption.text)

        if textRect.width() < textWidth + margin:
            # if the width is too small, adjust the *whole* button rect size
            # to fit the contents
            btnOption.rect.setLeft(btnOption.rect.left() - (
                textWidth - textRect.width() + margin))

        return btnOption

    def editorEvent(self, event, model, option, index):
        # map the proxy index to the fsModel
        srcIndex = index.model().mapToSource(index)
        # I'm just checking if it's a file, if you want to check the extension
        # you might need to use fsModel.fileName(srcIndex)
        if not self.fsModel.isDir(srcIndex):
            if event.type() in (QEvent.Enter, QEvent.MouseMove):
                self._mousePos = event.pos()
                # request an update of the current index
                option.widget.update(index)
            elif event.type() == QEvent.Leave:
                self._mousePos = None
            elif (event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonDblClick)
                and event.button() == Qt.LeftButton):
                    # check that the click is within the virtual button rectangle
                    if event.pos() in self.getOption(option, srcIndex).rect:
                        self._pressed = True
                    option.widget.update(index)
                    if event.type() == QEvent.MouseButtonDblClick:
                        # do not send double click events
                        return True
            elif event.type() == QEvent.MouseButtonRelease:
                if self._pressed and event.button() == Qt.LeftButton:
                    # emit the click only if the release is within the button rect
                    if event.pos() in self.getOption(option, srcIndex).rect:
                        filePath = self.fsModel.filePath(srcIndex)
                        count = self.clickedPaths.setdefault(filePath, 0)
                        self.buttonClicked.emit(index, count + 1)
                        self.clickedPaths[filePath] += 1
                self._pressed = False
                option.widget.update(index)
        return super().editorEvent(event, model, option, index)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        srcIndex = index.model().mapToSource(index)
        if not self.fsModel.isDir(srcIndex):
            btnOption = self.getOption(option, srcIndex)

            # remove the focus rectangle, as it will be inherited from the view
            btnOption.state &= ~QStyle.State_HasFocus
            if self._mousePos is not None and self._mousePos in btnOption.rect:
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
            option.widget.style().drawControl(
                QStyle.CE_PushButton, btnOption, painter)

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
        self.treeDelegate = TreeDelegate(self.model)
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
