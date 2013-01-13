#!/usr/bin/env python
#encoding:utf-8

from twisted.internet import reactor
from twisted.internet.protocol import Protocol,ServerFactory
import random

# ----	ChatProtocol class start  ---- #
class ChatProtocol(Protocol):
    def __init__(self,users):
        """初始化协议"""
        self.users = users
        self.name = None
        self.state = '__GetName__'
        self.color = None    # 用于记录用户所使用的棋子颜色
        self.game = None    # 用于记录用户的游戏编号。一个游戏编号需要4位用户才能开始游戏
        self.partner = {}    # 用于记录同游戏编号的用户信息。数据格式：color:protocol
        self.go = None    # 记录色子的值

    def connectionMade(self):
        """链接建立时的处理函数"""
        print 'Got connection from ',self.transport.client

    def connectionLost(self,reason):
        """链接断开时的处理函数"""
        if self.name in self.users:
            del self.users[self.name]
        print 'Connection lost from',self.transport.client

    def dataReceived(self,data):
        """收到数据时的处理函数"""
        while data.find('_99') != -1:
            edge = data.find('_99')
            data_piece = data[:edge]
            data = data[edge+3:]
            if self.state == '__GetName__':    # 用户名处理
                self.HandleName(data_piece)
            elif self.state == '__Waiting__':    # 加入游戏请求
                self.GetReady(data_piece)
            elif self.state == '__InGame__':
                self.InGame(data_piece)
        
    def HandleName(self,data):
        """对用户连接服务器注册用户名请求的处理函数"""
        if data[:2] == '01':    # 判断数据内容为名字。01代表名字请求
            name = data[2:]
            if self.users.has_key(name):    # 检查名字是否已经被使用
                self.transport.write('51_99')    # 名字已被使用，返回51错误信息代码
            else:    # 名字未被使用。
                self.name = name
                self.users[name] = self
                self.transport.write('00_99')    # 00代表申请被接收并且成功执行
                self.state = '__Waiting__'

    def GetReady(self,data):
        """对用户加入游戏请求的处理函数"""
        if data[:2] == '02':    # 判断数据内容是否是加入游戏请求。02代表加入游戏请求
            self.state = '__Ready__'
            has_game = False    # 标记是否已经找到游戏编号
            group = 0    # 记录同一游戏编号内的排队玩家数
            group_in_game = []    # 记录已经使用的游戏编号
            for name,protocol in self.users.iteritems():
                if name != self.name:
                    if protocol.state == '__Ready__':
                        has_game = True    # 找到游戏编号
                        if self.game is None:    # 加入游戏编号
                            self.game = protocol.game
                        if self.game == protocol.game:    # protocol的游戏编号相同，加入同组游戏
                            group = group + 1
                            self.partner[protocol.color] = protocol    # 记录同编号游戏玩家
                            if group == 3:    # 检查是否到4人可以开始游戏。可以开始游戏，则所有人都进入'__InGame__'状态
                                self.state = '__InGame__'
                                for color,partner in self.partner.iteritems():
                                    partner.state = '__InGame__'
                    elif protocol.state == '__InGame__':    # 记录已使用的游戏编号
                        group_in_game.append(protocol.game)
            if not has_game:    # 如果没有找到可用的游戏编号，则启用一个新的游戏编号
                new_game = 1
                while self.game == None:
                    if not new_game in group_in_game:
                        self.game = new_game
                    else:
                        new_game = new_game + 1
            if not has_game:    # 给玩家分配颜色
                self.color = 'blue'
                self.partner['blue'] = self
                self.transport.write('30blue_99')
            elif not 'green' in self.partner:
                self.color = 'green'
                self.partner['green'] = self
                self.transport.write('30green_99')
            elif not 'yellow' in self.partner:
                self.color = 'yellow'
                self.partner['yellow'] = self
                self.transport.write('30yellow_99')
            else:
                self.color = 'red'
                self.partner['red'] = self
                self.transport.write('30red_99')
            for color,partner in self.partner.iteritems():    # 更新同游戏编号玩家的partner数据
                if color != self.color:
                    partner.partner[self.color] = self
            if group < 3:
                self.transport.write('31_99')    # 缺少玩家，发送等待信息
            else:
                # 玩家到齐，发送游戏开始信息
                for color,partner in self.partner.iteritems():
                    partner.transport.write('32_99')    # 游戏开始
                    if color == 'blue':
                        partner.transport.write('34_99')    # 34代表该玩家走棋
                    else:
                        partner.transport.write('33蓝方_99')    # 33代表该玩家等待其他玩家走棋

    def InGame(self,data):
        """游戏开始后的数据处理函数"""
        prefix = data[:2]
        data = data[2:]
        color_togo = None    # 保存下一位要走棋的颜色
        if prefix == '03':
            self.go = random.randrange(1,7)
            self.transport.write('35'+str(self.go)+'_99')    # 35代表向走棋玩家发送掷色子的结果
            for color,partner in self.partner.iteritems():    # 向其他玩家发送掷色子结果
                if color != self.color:
                    partner.transport.write('37'+str(self.go)+'_99')    # 37代表其他玩家掷色子的结果
        if prefix == '04':    # 客户端发送的棋子位置改变数据。格式说明：04代表棋子改动信息+棋子颜色+'_iso1_'+第几颗棋子+'_iso2_'+棋子新位置
            edge = data.find('_iso1_')
            color_changed = data[:edge]    # color_changed记录改变的棋子颜色
            data = data[edge+6:]
            edge = data.find('_iso2_')
            num_changed = data[:edge]    # num_changed记录改变的是第几颗棋子
            pos_changed = data[edge+6:]    # pos_changed记录的是改变后棋子的位置
            for color,partner in self.partner.iteritems():
                if color != color_changed:
                    partner.transport.write('36'+color_changed+'_iso1_'+num_changed+'_iso2_'+pos_changed+'_99')    # 向其他客户端发送棋子位置改变信息
            # 若新位置为本方颜色，就跳到下一本方颜色位置。在90,91,92,93,0,50,51,52,53,54,55,56位置都不跳棋。
#            if not int(pos_changed) in (90,91,92,93,0,50,51,52,53,54,55,56,18) and int(pos_changed)%4 == 2:
#                pos_changed = str(int(pos_changed) + 4)    # 跳到下一位置
#                for color,partner in self.partner.iteritems():
#                    partner.transport.write('36'+color_changed+'_iso1_'+num_changed+'_iso2_'+pos_changed+'_99')    # 向所有客户端都发送新位置
#            elif pos_changed == '18':    # 若新位置为18，则飞到30
#                pos_changed = '30'
#                for color,partner in self.partner.iteritems():
#                    partner.transport.write('36'+color_changed+'_iso1_'+num_changed+'_iso2_'+pos_changed+'_99')
            if self.go == 6:    # 如果玩家掷出6，则额外获得一次掷色子的机会
                self.transport.write('34_99')
                for color,partner in self.partner.iteritems():    # 向其他玩家发送等待信息
                    if color != self.color:
                        if self.color == 'blue':
                            partner.transport.write('33蓝方_99')
                        if self.color == 'green':
                            partner.transport.write('33绿方_99')
                        if self.color == 'red':
                            partner.transport.write('33红方_99')
                        if self.color == 'yellow':
                            partner.transport.write('33黄方_99')
            else:    # 选出下一位走棋玩家
                for color,partner in self.partner.iteritems():    # 选出下一位走棋的玩家：蓝--绿--红--黄--蓝
                    if color_changed == 'blue' and color == 'green':
                        partner.transport.write('34_99')    # 34：玩家走棋
                        color_togo = color    # color_togo保存下一位走棋玩家。用于发送信息
                    elif color_changed == 'green' and color == 'red':
                        partner.transport.write('34_99')
                        color_togo = color
                    elif color_changed == 'red' and color == 'yellow':
                        partner.transport.write('34_99')
                        color_togo = color
                    elif color_changed == 'yellow' and color == 'blue':
                        partner.transport.write('34_99')
                        color_togo = color
                for color,partner in self.partner.iteritems():    # 向其他玩家发送等待信息
                    if color != color_togo:
                        if color_togo == 'blue':
                            partner.transport.write('33蓝方_99')
                        elif color_togo == 'green':
                            partner.transport.write('33绿方_99')
                        elif color_togo == 'red':
                            partner.transport.write('33红方_99')
                        elif color_togo == 'yellow':
                            partner.transport.write('33黄方_99')
            self.go = None    # 判断结束，色子结果清空
        if prefix == '05':    # 玩家无棋子可走。下一位玩家走棋
            for color,partner in self.partner.iteritems():
                if self.color == 'blue' and color == 'green':
                    partner.transport.write('34_99')    # 34:玩家走棋
                    color_togo = color
                if self.color == 'green' and color == 'red':
                    partner.transport.write('34_99')
                    color_togo = color
                if self.color == 'red' and color == 'yellow':
                    partner.transport.write('34_99')
                    color_togo = color
                if self.color == 'yellow' and color == 'blue':
                    partner.transport.write('34_99')
                    color_togo = color
            for color,partner in self.partner.iteritems():
                if color != color_togo:
                    if color_togo == 'blue':
                        partner.transport.write('33蓝方_99')
                    elif color_togo == 'green':
                        partner.transport.write('33绿方_99')
                    elif color_togo == 'red':
                        partner.transport.write('33红方_99')
                    elif color_togo == 'yellow':
                        partner.transport.write('33黄方_99')
        # 若棋子被吃，则接收到06数据并且向所有客户端发送新位置数据
        if prefix == '06':
            for color,partner in self.partner.iteritems():
                partner.transport.write('36'+data+'_99')
        # 07:获胜信息
        if prefix == '07':
            for color,partner in self.partner.iteritems():
                partner.transport.write('38'+data+'_99')    # 38代表服务端向客户端发送获胜信息
                partner.state = '__Waiting__'
                partner.color = None
                partner.game = None


# ----	ChatProtocol class end  ---- #


# ----	FlyingServerFactory class start  ---- #
class FlyingServerFactory(ServerFactory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self,addr):
        return ChatProtocol(self.users)

# ----	FlyingServerFactory class end  ---- #

if __name__ == '__main__':
    port = 19000
    reactor.listenTCP(port,FlyingServerFactory())
    reactor.run()
