#!/usr/bin/env python
#encoding:utf-8

class FlyChess():
    """棋子类，存有四方的所有十六枚棋子的状态：颜色和当前位置"""
    def __init__(self):
        """初始化变量"""
        self.blue = {1:None,2:None,3:None,4:None}
        self.green = {1:None,2:None,3:None,4:None}
        self.yellow = {1:None,2:None,3:None,4:None}
        self.red = {1:None,2:None,3:None,4:None}

    def GetPosition(self,color,num):
        """供外部调用得到棋子当前位置"""
        if color == 'blue':
            return self.blue[num]
        elif color == 'green':
            return self.green[num]
        elif color == 'yellow':
            return self.yellow[num]
        elif color == 'red':
            return self.red[num]
        else:
            return False

    def SetPosition(self,color,num,pos):
        if color == 'blue':
            self.blue[num] = pos
        elif color == 'green':
            self.green[num] = pos
        elif color == 'yellow':
            self.yellow[num] = pos
        elif color == 'red':
            self.red[num] = pos


