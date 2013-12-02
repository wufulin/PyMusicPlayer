#encoding=utf-8
'''
@author: wufulin
'''

import os
import sys

sys.path.append("..")

from util.Tool import *

####################################
#SongManager
#歌曲列表管理类
####################################
class SongManager(object):
    '''
            播放列表管理器
    '''

    def __init__(self):
        self.__SongList = []
        self.__SongListFile = 'conf/playlist.txt'
    
    def loadSongList(self):
        """从playlist.txt获取歌曲列表"""
        if os.path.exists(self.__SongListFile) is True:
            try:
                file = open(self.__SongListFile, 'r')
            except IOError:
                pass
            else:
                self.__SongList = []
                for song in file:
                    song = song.replace('\n','')
                    self.__SongList.append(song)
            finally:
                file.close()
    
    def saveSongList(self):
        """将歌曲列表的内容保存在playlist.txt文件"""
        try:
            file = open(self.__SongListFile, "w")
        except:
            pass
        else:
            for song in self.__SongList:
                file.write(song.__str__().encode(CODEC))
                file.write("\n")
        finally:
            file.close()
    
    def addSong(self, filePath):
        """添加一个歌曲文件全路径名到播放列表"""
        song_formate = filePath.split('.')[-1]
        if 'mp3' == song_formate \
        or 'wav' == song_formate \
        or 'WAV' == song_formate \
        or 'wm' == song_formate \
        or 'WM' == song_formate \
        or 'MP3' == song_formate:
            if 0 == self.__SongList.count(filePath.__str__()):
                self.__SongList.append(filePath.__str__().encode(CODEC))
                self.saveSongList()
                return True
            else:
                return False
    
    def deleteSongByIndex(self, index):
        self.__SongList.remove(self.__SongList[index])
        self.saveSongList()
    
    def getSongByIndex(self, index):
        return self.__SongList[index]
    
    def getSongList(self):
        return self.__SongList
    
    def getSongCount(self):
        return len(self.__SongList)
    
    def printSongList(self):
        for song in self.__SongList:
            print song
