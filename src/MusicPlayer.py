#encoding=utf-8
'''
@author: wufulin
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
from ui import main

class MusicPlayer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
        
    def initUI(self):
        self._ui = main.Ui_MainWidget()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self._ui.setupUi(self)

    def initMenu(self):
        pass
    
    ########## 鼠标事件 ##########
    def mouseReleaseEvent(self, e):
#         if self.rightButton == True:
#             self.rightButton = False
#             self.popMenu.popup(e.globalPos())
        pass

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton:
            self.move(e.globalPos()-self.dragPos)
            e.accept()
            
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.dragPos=e.globalPos()-self.frameGeometry().topLeft()
            e.accept()
        if e.button() == Qt.RightButton and self.rightButton == False:
            self.rightButton=True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    musicPlayer = MusicPlayer()
    musicPlayer.show()
    sys.exit(app.exec_())