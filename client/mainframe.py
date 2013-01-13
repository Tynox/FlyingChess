#!/usr/bin/env python
#encoding:utf-8

# MainFrame 

import wx
import chess
import random
import socket
import threading

# step变量，用于存储四色棋子的可落子点
blue_step = { 1:( 22,122), 2:( 50,110), 3:( 75,110), 4:(104,122),
              5:(120,100), 6:(112, 76), 7:(112, 50), 8:(122, 20),
              9:(150, 14),10:(175, 14),11:(200, 14),12:(225, 14),
             13:(250, 14),14:(278, 22),15:(288, 50),16:(288, 76),
             17:(278,100),18:(296,122),19:(324,110),20:(350,110),
             21:(376,122),22:(388,150),23:(388,175),24:(388,200),
             25:(388,225),26:(388,250),27:(376,275),28:(350,288),
             29:(325,288),30:(296,275),31:(278,296),32:(288,325),
             33:(288,350),34:(278,377),35:(250,388),36:(225,388),
             37:(200,388),38:(175,388),39:(150,388),40:(122,377),
             41:(112,350),42:(112,325),43:(122,296),44:(104,275),
             45:( 75,288),46:( 50,288),47:( 22,275),48:( 14,250),
             49:( 14,225),50:( 14,200),51:( 50,200),52:( 75,200),
             53:(100,200),54:(125,200),55:(150,200),56:(175,200),
              0:(  6,100),90:(  5,  5),91:(  5, 50),92:( 50,  5),
             93:( 50, 50)}

green_step = { 1:(278, 22), 2:(288, 50), 3:(288, 76), 4:(278,100),
               5:(296,122), 6:(324,110), 7:(350,110), 8:(376,122),
               9:(388,150),10:(388,175),11:(388,200),12:(388,225),
              13:(388,250),14:(376,275),15:(350,288),16:(325,288),
              17:(296,275),18:(278,296),19:(288,325),20:(288,350),
              21:(278,377),22:(250,388),23:(225,388),24:(200,388),
              25:(175,388),26:(150,388),27:(122,377),28:(112,350),
              29:(112,325),30:(122,296),31:(104,275),32:( 75,288),
              33:( 50,288),34:( 22,275),35:( 14,250),36:( 14,225),
              37:( 14,200),38:( 14,175),39:( 14,150),40:( 22,122),
              41:( 50,110),42:( 75,110),43:(104,122),44:(120,100),
              45:(112, 76),46:(112, 50),47:(122, 20),48:(150, 14),
              49:(175, 14),50:(200, 14),51:(200, 50),52:(200, 75),
              53:(200,100),54:(200,125),55:(200,150),56:(200,175),
               0:(300,  6),90:(330,  5),91:(330, 50),92:(375,  5),
              93:(375, 50)}

yellow_step = { 1:(122,377), 2:(112,350), 3:(112,325), 4:(122,296),
                5:(104,275), 6:( 75,288), 7:( 50,288), 8:( 22,275),
                9:( 14,250),10:( 14,225),11:( 14,200),12:( 14,175),
               13:( 14,150),14:( 22,122),15:( 50,110),16:( 75,110),
               17:(104,122),18:(120,100),19:(112, 76),20:(112, 50),
               21:(122, 20),22:(150, 14),23:(175, 14),24:(200, 14),
               25:(225, 14),26:(250, 14),27:(278, 22),28:(288, 50),
               29:(288, 76),30:(278,100),31:(296,122),32:(324,110),
               33:(350,110),34:(376,122),35:(388,150),36:(388,175),
               37:(388,200),38:(388,225),39:(388,250),40:(376,275),
               41:(350,288),42:(325,288),43:(296,275),44:(278,296),
               45:(288,325),46:(288,350),47:(278,377),48:(250,388),
               49:(225,388),50:(200,388),51:(200,350),52:(200,325),
               53:(200,300),54:(200,275),55:(200,250),56:(200,225),
                0:(102,400),90:(  5,325),91:(  5,370),92:( 50,325),
               93:(50,370)}

red_step = { 1:(376,275), 2:(350,288), 3:(325,288), 4:(296,275),
             5:(278,296), 6:(288,325), 7:(288,350), 8:(278,377),
             9:(250,388),10:(225,388),11:(200,388),12:(175,388),
            13:(150,388),14:(122,377),15:(112,350),16:(112,325),
            17:(122,296),18:(104,275),19:( 75,288),20:( 50,288),
            21:( 22,275),22:( 14,250),23:( 14,225),24:( 14,200),
            25:( 14,175),26:( 14,150),27:( 22,122),28:( 50,110),
            29:( 75,110),30:(104,122),31:(120,100),32:(112, 76),
            33:(112, 50),34:(122, 20),35:(150, 14),36:(175, 14),
            37:(200, 14),38:(225, 14),39:(250, 14),40:(278, 22),
            41:(288, 50),42:(288, 76),43:(278,100),44:(296,122),
            45:(324,110),46:(350,110),47:(376,122),48:(388,150),
            49:(388,175),50:(388,200),51:(350,200),52:(325,200),
            53:(300,200),54:(275,200),55:(250,200),56:(225,200),
             0:(400,300),90:(330,330),91:(330,375),92:(375,330),
            93:(375,375)}


# ----	RECVData class start  ---- #
class RECVData(wx.PyCommandEvent):
    """自定义wx事件：socket数据接收"""
    def __init__(self,evtType,id,data):
        wx.PyCommandEvent.__init__(self,evtType,id)
        self.data = data

    def GetData(self):
        return self.data
# ----  RECVData class end  ---- #


# 创建一个事件类型
myEVT_RECV_DATA = wx.NewEventType()

# 创建绑定器对象
EVT_RECV_DATA = wx.PyEventBinder(myEVT_RECV_DATA)


# ----	MainFrame class start  ---- #
class MainFrame(wx.Frame):
    """主界面"""
    def __init__(self,socket):
        """MainFrame initial"""
        wx.Frame.__init__(self,None,title="大蟒蛇飞行棋",style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN,size=(600,425))
        self.chess = chess.FlyChess()    # self.chess:棋子类的实例
        self.color = None    # self.color:用于存储服务器所分配的控制棋子的颜色.测试默认为blue
        self.go_step = None    # 色子数值
        self.socket = socket    # self.socket:socket实例
        self.thread = None    # self.thread:thread实例
        self.alive = threading.Event()
        self.__InitData()
        self.__InitUI()
        self.__EVT_Bind()
        self.StartThread()
        self.Show(True)

    def __InitData(self):
        """Init chess position data"""
        # init blue chess
        self.chess.SetPosition('blue',1,90)
        self.chess.SetPosition('blue',2,91)
        self.chess.SetPosition('blue',3,92)
        self.chess.SetPosition('blue',4,93)

        # init green chess
        self.chess.SetPosition('green',1,90)
        self.chess.SetPosition('green',2,91)
        self.chess.SetPosition('green',3,92)
        self.chess.SetPosition('green',4,93)

        # init yellow chess
        self.chess.SetPosition('yellow',1,90)
        self.chess.SetPosition('yellow',2,91)
        self.chess.SetPosition('yellow',3,92)
        self.chess.SetPosition('yellow',4,93)

        # init red chess
        self.chess.SetPosition('red',1,90)
        self.chess.SetPosition('red',2,91)
        self.chess.SetPosition('red',3,92)
        self.chess.SetPosition('red',4,93)
        

    def __InitUI(self):
        """Initialize UI"""
        # Infomation box
        self.info_text = wx.TextCtrl(self,pos=(435,10),size=(150,300),style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.info_text.AppendText('点击“开始游戏”按钮加入游戏\n')

        # dice_text:用于显示色子值
        self.dice_label = wx.StaticText(self,label='色子:',pos=(435,315),size=(35,18),style=wx.ALIGN_LEFT)
        self.dice_text = wx.TextCtrl(self,pos=(475,315),size=(25,25),style=wx.TE_READONLY)

        # Button
        self.start_button = wx.Button(self,-1,label="开始游戏",pos=(435,350))
        self.dice_button = wx.Button(self,-1,label="掷色子",pos=(435,390))
        self.dice_button.Enable(False)

    def __EVT_Bind(self):
        """wx event bind."""
        # start_button event:开始游戏
        self.Bind(wx.EVT_BUTTON,self.OnStart,self.start_button)

        # dice_button event:掷色子
        self.Bind(wx.EVT_BUTTON,self.OnDice,self.dice_button)

        # Click mouse to choose a chess and decide which chess flies.
        self.Bind(wx.EVT_LEFT_DOWN,self.ChooseChess)
        
        # Draw the chess when window is changed
        self.Bind(wx.EVT_PAINT,self.OnPaint)

        # 绑定事件处理函数
        self.Bind(EVT_RECV_DATA,self.RecvData)

    def StartThread(self):
        """启动数据接收线程"""
        self.thread = threading.Thread(target=self.OnRECV)
        self.thread.setDaemon(True)
        self.alive.set()
        self.thread.start()

    def StopThread(self):
        """关闭数据接收线程"""
        if self.thread is not None:
            self.alive.clear()
            self.thread = None

    def OnRECV(self):
        """数据接收"""
        while self.alive.isSet():
            recvData = self.socket.recv(1024)
            if recvData:
                dataEvent = RECVData(myEVT_RECV_DATA,self.GetId(),recvData)
                self.GetEventHandler().AddPendingEvent(dataEvent)

    def RecvData(self,event):
        """接收到数据后地处理"""
        data = event.GetData()
        while data.find('99') != -1:
            edge = data.find('_99')
            data_piece = data[:edge]
            self.HandleData(data_piece)
            data = data[edge+3:]

    def HandleData(self,data):
        """数据分片处理。根据前两位字符确定数据内容，进行相应的功能处理"""
        prefix = data[:2]
        data = data[2:]
        if prefix == '30':    # 分配颜色
            self.SetColor(data)
        if prefix == '31':    # 等待玩家加入游戏
            self.info_text.AppendText('等待其他玩家加入\n')
        if prefix == '32':
            self.info_text.AppendText('游戏开始！\n')
        if prefix == '33':    # 等待其他玩家走棋
            self.info_text.AppendText('等待'+data+'玩家走棋\n')
        if prefix == '34':    # 掷色子并走棋
            self.info_text.AppendText('请掷色子并走棋\n')
            self.dice_button.Enable(True)    # 允许走棋，将色子按钮置为可用
        if prefix == '35':    # 掷色子结果
            self.DiceResult(int(data))    # 把色子结果传给是否走棋的函数
        if prefix == '36':    # 其他玩家的棋子位置改变信息
            self.RecvPosition(data)
        if prefix == '37':    # 其他玩家掷色子结果
            self.info_text.AppendText('该玩家掷色子结果为'+data+'\n')
        if prefix == '38':    # 获胜方出现，游戏结束
            self.Restart(data)    # 重置游戏

    def Restart(self,data):
        """游戏结束，重置游戏"""
        self.info_text.AppendText(data+'\n')
        self.color = None
        self.go_step = None
        self.start_button.Enable(True)
        
    def OnStart(self,event):
        """开始游戏按钮，向服务器发送加入游戏请求"""
        self.socket.send('02_99')
        self.__InitData()
        self.OnPaint(self)

    def OnDice(self,event):
        """掷色子函数"""
        self.socket.send('03_99')    # 03代表掷色子请求
        self.dice_button.Enable(False)    # 色子置好，将色子按钮禁用

    def SetColor(self,data):
        """根据服务器信息分配控制颜色"""
        self.color = data
        self.start_button.Enable(False)    # 禁用开始游戏按钮
        if self.color == 'blue':
            text = '蓝色'
        elif self.color == 'green':
            text = '绿色'
        elif self.color == 'yellow':
            text = '黄色'
        else:
            text = '红色'
        self.info_text.AppendText('您使用'+text+'棋子\n')

    def DiceResult(self,data):
        """判断是否可走棋。色子结果不是6则机场中的飞机都不可走棋"""
        # 显示色子数值
        self.dice_text.Clear()
        self.dice_text.AppendText(str(data))
        # 取得当前用户棋子颜色
        if self.color == 'blue':
            chess = self.chess.blue
        if self.color == 'green':
            chess = self.chess.green
        if self.color == 'yellow':
            chess = self.chess.yellow
        if self.color == 'red':
            chess = self.chess.red
        # 判断飞机是否全在机场或到达终点。若是，色子结果必须为6才能走棋
        if chess[1] in (90,91,92,93,56) and chess[2] in (90,91,92,93,56) and chess[3] in (90,91,92,93,56) and chess[4] in (90,91,92,93,56) and data != 6:
            self.info_text.AppendText('无棋可走\n')
            self.socket.send('05_99')    # 通知服务器无棋可走
        else:
            self.go_step = data

    def ChooseChess(self,event):
        """Left click to choose a chess."""
        if self.go_step is not None:
            if self.color == 'blue':
                step = blue_step    # step保存当前操作棋子棋盘
                chess = self.chess.blue    # chess保存玩家的棋子状态
            elif self.color == 'green':
                step = green_step
                chess = self.chess.green
            elif self.color == 'yellow':
                step = yellow_step
                chess = self.chess.yellow
            elif self.color == 'red':
                step = red_step
                chess = self.chess.red
            if self.go_step:    # 获取当前棋子坐标
                current_pos = {1:step[self.chess.GetPosition(self.color,1)],
                               2:step[self.chess.GetPosition(self.color,2)],
                               3:step[self.chess.GetPosition(self.color,3)],
                               4:step[self.chess.GetPosition(self.color,4)]}
                mouse_pos = event.GetPositionTuple()    # 获取当前鼠标位置
                # 确定鼠标点击位置是否在机场内。若在机场内，则反映范围扩大为45，否则为25
                if mouse_pos[0] in range(5,90) and mouse_pos[1] in range(5,90):
                    area = 45
                elif mouse_pos[0] in range(330,415) and mouse_pos[1] in range(5,90):
                    area = 45
                elif mouse_pos[0] in range(5,90) and mouse_pos[1] in range(325,410):
                    area = 45
                elif mouse_pos[0] in range(330,415) and mouse_pos[1] in range(330,415):
                    area = 45
                else:
                    area = 25
                # 确定是否为第一颗棋子
                if mouse_pos[0] in range(current_pos[1][0],current_pos[1][0]+area):    # 比较X轴位置：棋子左上角起点<当前鼠标位置<棋子有下角终点
                    if mouse_pos[1] in range(current_pos[1][1],current_pos[1][1]+area):    # 比较Y轴位置：同上
                        if chess[1] in (90,91,92,93) and self.go_step != 6:    # 如果棋子是在机场且色子不是6，则无反映
                            pass
                        elif chess[1] == 56:    # 如果棋子已经到达终点，则无反应
                            pass
                        else:    # 其他时候都有效
                            self.SetPosition(1)     # 保存新位置
                        return
                # 确定是否为第二颗棋子
                if mouse_pos[0] in range(current_pos[2][0],current_pos[2][0]+area):
                    if mouse_pos[1] in range(current_pos[2][1],current_pos[2][1]+area):
                        if chess[2] in (90,91,92,93) and self.go_step != 6:
                            pass
                        elif chess[2] == 56:
                            pass
                        else:
                            self.SetPosition(2)
                        return
                # 确定是否为第三颗棋子
                if mouse_pos[0] in range(current_pos[3][0],current_pos[3][0]+area):
                    if mouse_pos[1] in range(current_pos[3][1],current_pos[3][1]+area):
                        if chess[3] in (90,91,92,93) and self.go_step != 6:
                            pass
                        elif chess[3] == 56:
                            pass
                        else:
                            self.SetPosition(3)
                        return
                # 确定是否为第四颗棋子
                if mouse_pos[0] in range(current_pos[4][0],current_pos[4][0]+area):
                    if mouse_pos[1] in range(current_pos[4][1],current_pos[4][1]+area):
                        if chess[4] in (90,91,92,93) and self.go_step != 6:
                            pass
                        elif chess[4] == 56:
                            pass
                        else:
                            self.SetPosition(4)
                        return

    def SetPosition(self,current):
        """保存新位置。根据current值确定是第几颗棋子。再根据之前的位置计算出当前位置"""
        if self.color == 'blue':
            temp = self.chess.blue[current]    # 获取当前棋子所在位置
        elif self.color == 'green':
            temp = self.chess.green[current]
        elif self.color == 'yellow':
            temp = self.chess.yellow[current]
        elif self.color == 'red':
            temp = self.chess.red[current]
        if temp in (90,91,92,93):
            new = 0
        else:
            new = temp + self.go_step
            if new > 56:
                new = 56 - (new - 56)
        self.chess.SetPosition(self.color,current,new)
        self.SendNewPosition(current,new)    # 调用发送新位置函数
        self.OnPaint(self)
        if not new in (90,91,92,93,0,50,51,52,53,54,55,56,18) and new%4 == 2:    # 检查是否同色能跳到下一位置
            new = new +4
            self.chess.SetPosition(self.color,current,new)
            self.SendNewPosition(current,new)
            self.OnPaint(self)
        elif new == 18:    # 检查是否能飞到30.18-->30
            new = 30
            self.chess.SetPosition(self.color,current,new)
            self.SendNewPosition(current,new)
            self.OnPaint(self)
        if not new in (90,91,92,93,0,51,52,53,54,55,56):
            self.HitCheck(new)    # 检查是否有吃棋子的情况发生。current表示是当前玩家选择的棋子，new代表其位置
        if new == 56:    # 胜利检测
            self.Win()
        self.go_step = None

    def SendNewPosition(self,num,pos):
        """向服务器发送玩家改变的棋子位子"""
        self.socket.send('04'+self.color+'_iso1_'+str(num)+'_iso2_'+str(pos)+'_99')    # 数据格式说明：04代表棋子改动信息+棋子颜色+'_iso1_'+第几颗棋子+'_iso2_'+棋子新位置+_99

    def Win(self):
        """胜利检测"""
        if self.color == 'blue':
            chess = self.chess.blue
        elif self.color == 'green':
            chess = self.chess.green
        elif self.color == 'red':
            chess = self.chess.red
        elif self.color == 'yellow':
            chess = self.chess.yellow
        if chess[1] == chess[2] == chess[3] == chess[4] == 56:
            if self.color == 'blue':
                self.socket.send('07蓝方获胜_99')    # 07代表获胜信息
            elif self.color == 'green':
                self.socket.send('07绿方获胜_99')
            elif self.color == 'red':
                self.socket.send('07红方获胜_99')
            elif self.color == 'yellow':
                self.socket.send('07黄方获胜_99')


    def HitCheck(self,pos):
        """检查是否发生吃其他玩家的情况发生，发生则棋子被吃发送被吃棋子的新位置（返回机场）"""
        pos_tmp = None
        # 检查蓝色棋子
        if self.color != 'blue':
            if self.color == 'green':    # 位置转换成蓝色棋子位置表
                if pos in range(1,38):
                    pos_tmp = pos + 13
                elif pos in range(40,51):
                    pos_tmp = pos - 39
            elif self.color == 'red':
                if pos in range(1,25):
                    pos_tmp = pos+26
                elif pos in range(27,51):
                    pos_tmp = pos-26
            elif self.color == 'yellow':
                if pos in range(1,12):
                    pos_tmp = pos+39
                elif pos in range(14,51):
                    pos_tmp = pos-13
            if pos_tmp:
                if self.chess.blue[1] == pos_tmp:
                    self.socket.send('06blue_iso1_1_iso2_90_99')    # 发送被吃棋子新位置。06代表棋子被吃更新信息
                if self.chess.blue[2] == pos_tmp:
                    self.socket.send('06blue_iso1_2_iso2_91_99')
                if self.chess.blue[3] == pos_tmp:
                    self.socket.send('06blue_iso1_3_iso2_92_99')
                if self.chess.blue[4] == pos_tmp:
                    self.socket.send('06blue_iso1_4_iso2_93_99')
        # 检查绿色棋子
        if self.color != 'green':
            if self.color == 'blue':
                if pos in range(1,12):
                    pos_tmp = pos + 39
                elif pos in range(14,51):
                    pos_tmp = pos - 13
            elif self.color == 'red':
                if pos in range(1,38):
                    pos_tmp = pos + 13
                elif pos in range(40,51):
                    pos_tmp = pos - 39
            elif self.color == 'yellow':
                if pos in range(1,25):
                    pos_tmp = pos + 26
                elif pos in range(27,51):
                    pos_tmp = pos - 26
            if pos_tmp:
                if self.chess.green[1] == pos_tmp:
                    self.socket.send('06green_iso1_1_iso2_90_99')
                if self.chess.green[2] == pos_tmp:
                    self.socket.send('06green_iso1_2_iso2_91_99')
                if self.chess.green[3] == pos_tmp:
                    self.socket.send('06green_iso1_3_iso2_92_99')
                if self.chess.green[4] == pos_tmp:
                    self.socket.send('06green_iso1_4_iso2_93_99')
        # 检查黄色棋子
        if self.color != 'yellow':
            if self.color == 'blue':
                if pos in range(1,38):
                    pos_tmp = pos + 13
                elif pos in range(40,51):
                    pos_tmp = pos - 39
            elif self.color == 'green':
                if pos in range(1,25):
                    pos_tmp = pos + 26
                elif pos in range(27,51):
                    pos_tmp = pos - 26
            elif self.color == 'red':
                if pos in range(1,12):
                    pos_tmp = pos + 39
                elif pos in range(14,51):
                    pos_tmp = pos - 13
            if pos_tmp:
                if self.chess.yellow[1] == pos_tmp:
                    self.socket.send('06yellow_iso1_1_iso2_90_99')
                if self.chess.yellow[2] == pos_tmp:
                    self.socket.send('06yellow_iso1_2_iso2_91_99')
                if self.chess.yellow[3] == pos_tmp:
                    self.socket.send('06yellow_iso1_3_iso2_92_99')
                if self.chess.yellow[4] == pos_tmp:
                    self.socket.send('06yellow_iso1_4_iso2_93_99')
        # 检查红色棋子
        if self.color != 'red':
            if self.color == 'blue':
                if pos in range(1,25):
                    pos_tmp = pos + 26
                elif pos in range(27,51):
                    pos_tmp = pos - 26
            elif self.color == 'green':
                if pos in range(1,12):
                    pos_tmp = pos + 39
                elif pos in range(14,51):
                    pos_tmp = pos - 13
            elif self.color == 'yellow':
                if pos in range(1,38):
                    pos_tmp = pos + 13
                elif pos in range(40,51):
                    pos_tmp = pos - 39
            if pos_tmp:
                if self.chess.red[1] == pos_tmp:
                    self.socket.send('06red_iso1_1_iso2_90_99')
                if self.chess.red[2] == pos_tmp:
                    self.socket.send('06red_iso1_2_iso2_91_99')
                if self.chess.red[3] == pos_tmp:
                    self.socket.send('06red_iso1_3_iso2_92_99')
                if self.chess.red[4] == pos_tmp:
                    self.socket.send('06red_iso1_4_iso2_93_99')

    def RecvPosition(self,data):
        """其他玩家的棋子位子改变处理函数"""
        edge = data.find('_iso1_')
        color = data[:edge]    # 取得颜色
        data = data[edge+6:]
        edge = data.find('_iso2_')
        num = data[:edge]    # 取得改变的棋子编号
        pos = data[edge+6:]    # 取得改变后的位子
        self.chess.SetPosition(color,int(num),int(pos))    # 写入数据
        self.OnPaint(self)    # 重绘棋盘

    def OnPaint(self,event):
        """wx.EVT_PAINT event function"""
        dc = wx.PaintDC(self)
        # 载入图片
        blue_chess = wx.Image(r'resource/blue.gif',wx.BITMAP_TYPE_ANY)
        blue_chess_half = blue_chess.Scale(blue_chess.GetWidth()/2,blue_chess.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
        green_chess = wx.Image(r'resource/green.gif',wx.BITMAP_TYPE_ANY)
        green_chess_half = green_chess.Scale(green_chess.GetWidth()/2,green_chess.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
        yellow_chess = wx.Image(r'resource/yellow.gif',wx.BITMAP_TYPE_ANY)
        yellow_chess_half = yellow_chess.Scale(yellow_chess.GetWidth()/2,yellow_chess.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
        red_chess = wx.Image(r'resource/red.gif',wx.BITMAP_TYPE_ANY)
        red_chess_half = red_chess.Scale(red_chess.GetWidth()/2,red_chess.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)
        chess_board = wx.Image(r'resource/flying_chess.jpg',wx.BITMAP_TYPE_ANY)
        chess_board = chess_board.Scale(chess_board.GetWidth()/2,chess_board.GetHeight()/2,wx.IMAGE_QUALITY_HIGH)

        # Draw chess board
        dc.DrawBitmap(wx.BitmapFromImage(chess_board),0,0,True)

        # Draw blue chess
        if self.chess.blue[1] in (90,91,92,93):    # 判断棋子所在位置，决定使用图片的大小
            blue_draw = blue_chess
        else:
            blue_draw = blue_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(blue_draw),blue_step[self.chess.GetPosition('blue',1)][0],blue_step[self.chess.GetPosition('blue',1)][1],True)
        if self.chess.blue[2] in (90,91,92,93):
            blue_draw = blue_chess
        else:
            blue_draw = blue_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(blue_draw),blue_step[self.chess.GetPosition('blue',2)][0],blue_step[self.chess.GetPosition('blue',2)][1],True)
        if self.chess.blue[3] in (90,91,92,93):
            blue_draw = blue_chess
        else:
            blue_draw = blue_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(blue_draw),blue_step[self.chess.GetPosition('blue',3)][0],blue_step[self.chess.GetPosition('blue',3)][1],True)
        if self.chess.blue[4] in (90,91,92,93):
            blue_draw = blue_chess
        else:
            blue_draw = blue_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(blue_draw),blue_step[self.chess.GetPosition('blue',4)][0],blue_step[self.chess.GetPosition('blue',4)][1],True)

        # Draw green chess
        if self.chess.green[1] in (90,91,92,93):
            green_draw = green_chess
        else:
            green_draw = green_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(green_draw),green_step[self.chess.GetPosition('green',1)][0],green_step[self.chess.GetPosition('green',1)][1],True)
        if self.chess.green[2] in (90,91,92,93):
            green_draw = green_chess
        else:
            green_draw = green_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(green_draw),green_step[self.chess.GetPosition('green',2)][0],green_step[self.chess.GetPosition('green',2)][1],True)
        if self.chess.green[3] in (90,91,92,93):
            green_draw = green_chess
        else:
            green_draw = green_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(green_draw),green_step[self.chess.GetPosition('green',3)][0],green_step[self.chess.GetPosition('green',3)][1],True)
        if self.chess.green[4] in (90,91,92,93):
            green_draw = green_chess
        else:
            green_draw = green_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(green_draw),green_step[self.chess.GetPosition('green',4)][0],green_step[self.chess.GetPosition('green',4)][1],True)

        # Draw yellow chess
        if self.chess.yellow[1] in (90,91,92,93):
            yellow_draw = yellow_chess
        else:
            yellow_draw = yellow_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(yellow_draw),yellow_step[self.chess.GetPosition('yellow',1)][0],yellow_step[self.chess.GetPosition('yellow',1)][1],True)
        if self.chess.yellow[2] in (90,91,92,93):
            yellow_draw = yellow_chess
        else:
            yellow_draw = yellow_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(yellow_draw),yellow_step[self.chess.GetPosition('yellow',2)][0],yellow_step[self.chess.GetPosition('yellow',2)][1],True)
        if self.chess.yellow[3] in (90,91,92,93):
            yellow_draw = yellow_chess
        else:
            yellow_draw = yellow_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(yellow_draw),yellow_step[self.chess.GetPosition('yellow',3)][0],yellow_step[self.chess.GetPosition('yellow',3)][1],True)
        if self.chess.yellow[4] in (90,91,92,93):
            yellow_draw = yellow_chess
        else:
            yellow_draw = yellow_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(yellow_draw),yellow_step[self.chess.GetPosition('yellow',4)][0],yellow_step[self.chess.GetPosition('yellow',4)][1],True)

        # Draw red chess
        if self.chess.red[1] in (90,91,92,93):
            red_draw = red_chess
        else:
            red_draw = red_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(red_draw),red_step[self.chess.GetPosition('red',1)][0],red_step[self.chess.GetPosition('red',1)][1],True)
        if self.chess.red[2] in (90,91,92,93):
            red_draw = red_chess
        else:
            red_draw = red_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(red_draw),red_step[self.chess.GetPosition('red',2)][0],red_step[self.chess.GetPosition('red',2)][1],True)
        if self.chess.red[3] in (90,91,92,93):
            red_draw = red_chess
        else:
            red_draw = red_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(red_draw),red_step[self.chess.GetPosition('red',3)][0],red_step[self.chess.GetPosition('red',3)][1],True)
        if self.chess.red[4] in (90,91,92,93):
            red_draw = red_chess
        else:
            red_draw = red_chess_half
        dc.DrawBitmap(wx.BitmapFromImage(red_draw),red_step[self.chess.GetPosition('red',4)][0],red_step[self.chess.GetPosition('red',4)][1],True)

# ----	MainFrame class end  ---- #

if __name__ == "__main__":
    """run the python program."""
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
