#!/usr/bin/env python
#encoding:utf-8

import wx
import socket
import re
import login
import mainframe

class Flying():
    def __init__(self):
        """初始化"""
        self.name = None
        ip = None
        ok = False
        while not ok:
            logininfo = login.LoginDialog(self.name,ip)
            result = logininfo.ShowModal()
            logininfo.Destroy()
            self.name,ip = logininfo.GetData()
            name_backup = self.name
            if result == wx.ID_OK:
                if self.HandleInfo(ip):
                    self.InitSocket(ip)
                    ok = True
                else:
                    errorDlg = wx.MessageBox('名字过长或IP地址格式错误','Error',wx.OK | wx.ICON_INFORMATION)
            if not self.HandleName():
                ok = False
                errorDlg = wx.MessageBox('名字已被使用','Error',wx.OK | wx.ICON_INFORMATION)
                self.name = name_backup
        frame = mainframe.MainFrame(self.socket)

    def HandleName(self):
        """检查名字是否可用"""
        self.socket.send('01'+self.name+'_99')    # 向服务器发送名字
        result = self.socket.recv(1024)
        if result == '51_99':    # '10'代表名字已经被使用
            return False
        else:
            return True

    def InitSocket(self,ip):
        """初始化socket"""
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((ip,19000))

    def HandleInfo(self,ip):
        """检查ip地址是否正确,名字是否超出长度"""
        # 检查名字是否超出长度
        length = len(self.name)
        if length > 16:
            return False
        # 检查ip地址是否正确
        pattern = r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)'
        if not re.match(pattern,ip):
            return False
        else:
            return True


if __name__ == '__main__':
    app = wx.App()
    Flying()
    app.MainLoop()
