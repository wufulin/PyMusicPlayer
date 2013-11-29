#encoding=utf-8
'''
@author: wufulin
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtGui import *

import sys

class MainApp(QWidget):
    def __init__(self, parent=None):
        pass
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainApp = MainApp()
    mainApp.show()
    sys.exit(app.exec_())