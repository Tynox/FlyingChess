#!/usr/bin/env python
#encoding:utf-8

# MainFrame 

import wx

class ChessPanel(wx.Panel):
    """Draw the chess board."""
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,size=(425,425),name="ChessPanel")

        # Draw the chess board.
        bmp = wx.Image(r'resource/flying_chess.jpg',wx.BITMAP_TYPE_ANY)
        bmp = bmp.Scale(bmp.GetWidth()/2,bmp.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.StaticBitmap(self,-1,wx.BitmapFromImage(bmp))



class MainFrame(wx.Frame):
    def __init__(self):
        """MainFrame initial"""
        wx.Frame.__init__(self,None,title="大蟒蛇飞行棋",style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN,size=(600,425))
        self.__InitUI()
        self.__EVT_Bind()
        self.Show(True)


    def __InitUI(self):
        """Initialize UI"""

        ChessPanel(self)
        # Draw chess board
#        image_file = r'resource/flying_chess.jpg'
#        bmp = wx.Image(image_file,wx.BITMAP_TYPE_ANY)
#        bmp = bmp.Scale(bmp.GetWidth()/2,bmp.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
#        bitmap = wx.StaticBitmap(self,-1,wx.BitmapFromImage(bmp))

        # Infomation box
        info_text = wx.TextCtrl(self,pos=(435,10),size=(150,100),style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Button
        self.start_button = wx.Button(self,-1,label="开始游戏",pos=(435,120))

        # Chess picture
        red_bmp = wx.Image(r'resource/red.gif',wx.BITMAP_TYPE_ANY)
        red_bmp = red_bmp.Scale(red_bmp.GetWidth()/2,red_bmp.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
        red_bitmap = wx.StaticBitmap(self,-1,wx.BitmapFromImage(red_bmp),pos=(124,20))

    def __EVT_Bind(self):
        pass

if __name__ == "__main__":
    """run the python program."""
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
