#encoding=utf-8
'''
@author: wufulin
'''

CODEC='utf-8'

def ParseSongName(source):
    return source.split('\\')[-1]

def ParseSongNameEscapeFileExt(source):
    return ParseSongName(source).split('.')[0]

def ms2time(ms):
        """时间转换为字符串"""
        if ms <= 0: return '00:00'
        time_sec, ms = ms / 1000, ms % 1000
        time_min, time_sec = time_sec / 60, time_sec % 60
        time_hor, time_min = time_min / 60, time_min % 60
        if time_hor == 0: return '%02d:%02d'%(time_min, time_sec)
        return '--:--'