#!/usr/bin/env python
#coding:utf-8

#  login.py
#  This is a chat room login dialog. Running environment:Python 2.7,wxPython 2.8-unicode
#  Liences:MIT license. Detail information:http://opensource.org/licenses/MIT

import wx
import sys

reload(sys)   # reload sys module
sys.setdefaultencoding('utf-8')   # set sys coding utf-8. make widgets support utf-8

class LoginDialog(wx.Dialog):
    """Login Dialog class"""
    def __init__(self,name,ip):
        """initial"""
        wx.Dialog.__init__(self,None,title="Login",size=(280,140))
        self.name = name
        self.ip = ip
        self.InitUI()
#        self.ShowModal()

    def InitUI(self):
        """initial UI"""
        vbox = wx.BoxSizer(wx.VERTICAL)

        nameLabel = wx.StaticText(self,label="      Name:")
        self.nameText = wx.TextCtrl(self)
        if self.name:
            self.nameText.SetValue(self.name)
        else:
            self.nameText.SetValue('your name')
        ipLabel = wx.StaticText(self,label="Server IP:")
        self.ipText = wx.TextCtrl(self)
        if self.ip:
            self.ipText.SetValue(self.ip)
        else:
            self.ipText.SetValue('127.0.0.1')

        loginButton = wx.Button(self,label="Login")
        exitButton = wx.Button(self,label="Exit")

#        loginButton.Bind(wx.EVT_BUTTON,self.OnLogin)
#        exitButton.Bind(wx.EVT_BUTTON,self.OnExit)
        wx.EVT_BUTTON(self,loginButton.GetId(),self.OnLogin)
        wx.EVT_BUTTON(self,exitButton.GetId(),self.OnExit)

        hbox_1 = wx.BoxSizer()
        hbox_1.Add(nameLabel,proportion=0,flag=wx.ALL | wx.EXPAND | wx.ALIGN_LEFT,border=2)
        hbox_1.Add(self.nameText,proportion=2,flag=wx.ALL | wx.EXPAND |wx.ALIGN_CENTER,border=2)

        hbox_2 = wx.BoxSizer()
        hbox_2.Add(ipLabel,proportion=0,flag=wx.ALL | wx.EXPAND | wx.ALIGN_LEFT,border=2)
        hbox_2.Add(self.ipText,proportion=2,flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER,border=2)

        hbox_3 = wx.BoxSizer()
        hbox_3.Add(loginButton,proportion=0,flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER,border=2)
        hbox_3.Add(exitButton,proportion=0,flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER,border=2)

        vbox.Add(hbox_1,proportion=1,flag=wx.ALL | wx.EXPAND,border=2)
        vbox.Add(hbox_2,proportion=1,flag=wx.ALL | wx.EXPAND,border=2)
        vbox.Add(hbox_3,proportion=0,flag=wx.ALL | wx.ALIGN_CENTER,border=2)

        self.SetSizer(vbox)
    
    def GetData(self):
        return (self.nameText.GetValue(),self.ipText.GetValue())
    
    def OnLogin(self,e):
        """Login button"""
#        self.name = self.nameText.GetValue()
#        self.ip = self.ipText.GetValue()
        self.EndModal(wx.ID_OK)

    def OnExit(self,e):
        """Exit button"""
        self.EndModal(wx.ID_CANCEL)
        sys.exit()

if __name__ == '__main__':
    app = wx.App()
    name = None
    ip = None
    dlg = LoginDialog(name,ip)
    dlg.ShowModal()
    app.MainLoop()
