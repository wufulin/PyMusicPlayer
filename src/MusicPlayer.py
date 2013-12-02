#encoding=utf-8
'''
@author: wufulin
'''

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.phonon import *

from util.Tool import *
from util.SongManager import SongManager
from ui import main

import sys
import random

class MusicPlayer(QWidget, main.Ui_MainWidget):   
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.initUI()
        self.initMenu()
        self.initPhonon()
        self.initConf()
        
    def initUI(self):
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.setupUi(self)
        self.connect(self.btnClose, SIGNAL('clicked()'), self.closePrograme)
        self.connect(self.btnAdd, SIGNAL('clicked()'), self.addSongs)
        self.connect(self.btnDel, SIGNAL('clicked()'), self.delSong)
        self.connect(self.btnStart, SIGNAL('clicked()'), self.playSong)
        self.connect(self.btnReset, SIGNAL('clicked()'), self.resetSong)
        self.connect(self.btnNext, SIGNAL('clicked()'), self.playNextSong)
        self.connect(self.btnPrev, SIGNAL('clicked()'), self.playPrevSong)
        self.connect(self.btnRepeat, SIGNAL('clicked()'), self.repeatPlay)
        self.connect(self.btnShuffle, SIGNAL('clicked()'), self.shufflePlay)
        
        self.listSongs.mouseDoubleClickEvent = self.doubleSelectSong

    def initMenu(self):
        quitAction = QAction(QIcon(""), u'退出(&Q)', self)
        self.connect(quitAction, SIGNAL("triggered()"), self.closePrograme)
        aboutAction = QAction(QIcon(""), u'关于(&A)', self)
        self.connect(aboutAction, SIGNAL("triggered()"), self.aboutBox)
        self.rightButton = False
        
        # 添加到右键菜单
        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(aboutAction)
        self.popMenu.addAction(quitAction)      
          
    def initPhonon(self):
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.setTickInterval(100)
        self.mediaObject.tick.connect(self.updateTime)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory)
        
        # 把 mediaObject 和 audioOutput连接起来
        Phonon.createPath(self.mediaObject, self.audioOutput)

        # 绑定声音控件
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.volumeSlider.setMaximumVolume(0.75)
        
        # 绑定播放进度控件
        self.seekSlider.setMediaObject(self.mediaObject)
        
        # 设置播放器初始状态
        self.currentIndex = 0
        self.isPlaying = False
        self.isReset = False
    
    def initConf(self):
        """装置配置信息"""
        self.songManager = SongManager()
        
        # 装载默认歌曲列表
        self.refreshSongList()
    
    def refreshSongList(self):
        self.songManager.loadSongList()
        self.listSongs.clear()
        if self.songManager.getSongCount() !=0:
            songList = self.songManager.getSongList()
            for file in songList:
                self.listSongs.addItem(ParseSongName(file.decode(CODEC)))
            
    def addSongs(self):
        """添加歌曲到列表"""
        files = QFileDialog.getOpenFileNames(self, u"请选择歌曲", u"", self.tr("Song Files(*.mp3)"))
        for file in files:
            result = self.songManager.addSong(file)
            if result is True:
                self.listSongs.addItem(ParseSongName(file))
    
    def delSong(self):
        """从播放列表中，删除被选中的歌曲"""
        items = self.listSongs.selectedItems()
        for item in items:
            index = self.listSongs.row(item)
            self.songManager.deleteSongByIndex(index)
        self.refreshSongList()
    
    def doubleSelectSong(self, e):
        """双击歌曲播放"""
        self.currentIndex = self.listSongs.row(self.listSongs.selectedItems()[0])
        self.playSongByIndex(self.currentIndex)
        
    def playSong(self):
        items = self.listSongs.selectedItems()
        if len(items) > 0:
            item = self.listSongs.selectedItems()[0]
            self.currentIndex = self.listSongs.row(item)
        self.playSongByIndex(self.currentIndex)
        
    def playSongByIndex(self, index):
        url = self.songManager.getSongByIndex(index)
        self.mediaObject.setCurrentSource(Phonon.MediaSource(url.decode()))
#         if self.mediaObject.state == Phonon.PausedState:
        self.mediaObject.play()
        self.isPlaying = True
        songName = ParseSongNameEscapeFileExt(self.songManager.getSongByIndex(index))
        self.labelName.setText(songName.decode())
        
        # 设置play按钮状态
        if self.isPlaying:
            # 按钮变停止
            self.btnStart.setStyleSheet(QtCore.QString.fromUtf8("QPushButton#btnStart {border:none;background: url(:/button/btnStop.jpg);}"))
            self.connect(self.btnStart, SIGNAL('clicked()'), self.pauseSong)
    
    def pauseSong(self):
        # 按钮变开始
        self.btnStart.setStyleSheet(QtCore.QString.fromUtf8("QPushButton#btnStart {border:none;background: url(:/button/btnStart.jpg);}"))
        self.connect(self.btnStart, SIGNAL('clicked()'), self.playSong)
        self.isPlaying = False
        self.mediaObject.pause()
        
    def resetSong(self):
        self.mediaObject.stop()
        self.btnStart.setStyleSheet(QtCore.QString.fromUtf8("QPushButton#btnStart {border:none;background: url(:/button/btnStart.jpg);}"))
        self.connect(self.btnStart, SIGNAL('clicked()'), self.playSong)
        self.consumeTime.setText(ms2time(0))
        self.totalTime.setText(ms2time(0))
    
    def updateTime(self, time):
        totalTime = self.mediaObject.totalTime()
        self.totalTime.setText(ms2time(totalTime))
        self.consumeTime.setText(ms2time(time))
    
    def playNextSong(self):
        self.currentIndex += 1
        if self.currentIndex >= self.songManager.getSongCount():
            self.currentIndex = 0
        self.playSongByIndex(self.currentIndex)
        self.listSongs.setCurrentRow(self.currentIndex)
    
    def playPrevSong(self):
        self.currentIndex -= 1
        if self.currentIndex < 0:
            self.currentIndex = self.songManager.getSongCount() - 1
        self.playSongByIndex(self.currentIndex)
        self.listSongs.setCurrentRow(self.currentIndex)
    
    def shufflePlay(self):
        """随机播放"""
        index = random.randint(0, self.songManager.getSongCount() - 1)
        self.playSongByIndex(index)
    
    def repeatPlay(self):
        """循环播放"""
        pass
    
    def closePrograme(self):
        self.mediaObject.clear()
        exit(0)
        
    def aboutBox(self):
        about = QMessageBox(self)
        about.setWindowTitle(u"关于Dribbble Music Player")
        about.setText(u"Dribbble Music Player 是一个使用PyQt编写的简单MP3播放器\n\t作者：wufulin<wufulinit@gmail.com>")
        about.show()
        
    ########## 鼠标事件 ##########
    
    def mouseReleaseEvent(self, e):
        if self.rightButton == True:
            self.rightButton = False
            self.popMenu.popup(e.globalPos())

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