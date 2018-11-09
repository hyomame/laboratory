# -*- coding: utf-8 -*-

import re
import game
import board
from ai import DQN_Solver

class ProcessingMessage:
    MY_NAME = 'mame'
    
    reward = 0

    def __init__(self):
        self.winner = -1
        self.play_message = None
        self.opp_worker = None
        self.opp_place = None

        self.MSGPTN = re.compile(r'([0-9]+) (.*)')
        self.ID_MSGPTN = re.compile(r'102 PLAYERID ([0-1])')
        self.TREND_MSGPTN = re.compile(r'209 TREND (T[1-3])')
        self.PLAY_MSGPTN = re.compile(r'([PAS]) (([1-6])-([1-3]))(.*)')
        self.OPP_PLAY_MSGPTN = re.compile(r'206 PLAYED ([01]) ([PAS]) (([1-6])-([1-3])).*')
        self.WINNER_MSGPTN = re.compile(r'501 WINNER (-?[0-1])')
        
        self.state = game.Game()

    def analyze(self, message):
        mactch_msg = self.MSGPTN.match(message)
        path = 'ai.txt'
        if mactch_msg:
            num = int(mactch_msg.group(1))
            if num == 100:
                return '101 NAME ' + self.MY_NAME
            elif num == 102:
                mactch_ID_msg = self.ID_MSGPTN.match(message)
                if mactch_ID_msg:
                    self.MY_ID = int(mactch_ID_msg.group(1))
                    self.state.set_player_name(self.MY_ID, self.MY_NAME)
                    if self.MY_ID == 0:
                        self.OPP_ID = 1
                    else:
                        self.OPP_ID = 0
                    self.state.set_player_name(self.OPP_ID, 'opponent')
                return '000 NOTPLAY'
            elif num == 204:
                self.play_message = None
                #↓ここに関数
                propriety = self.play()
                if propriety and self.play_message != None:
                    return self.play_message
                else:
                    print('action error.')
                    return '003 DISCONNECT'
            elif num == 206:
                match_opp_msg = self.OPP_PLAY_MSGPTN.match(message)
                if match_opp_msg:
                    worker = match_opp_msg.group(2)
                    place = match_opp_msg.group(3)
                    if place != '5-3':
                        self.action(self.OPP_ID, place, worker)
                    else:
                        self.opp_worker = match_opp_msg.group(2)
                        self.opp_place = match_opp_msg.group(3)
                return '000 NOTPLAY'
            elif num == 209:
                match_trend_msg = self.TREND_MSGPTN.match(message)
                if match_trend_msg:
                    self.state.set_trend(match_trend_msg.group(1))
                    self.action(self.OPP_ID, self.opp_place, self.opp_worker)
                    self.opp_worker = None
                    self.opp_place = None
                return '000 NOTPLAY'
            elif num == 400:
                print('syntax error!')
                return '003 DISCONNECT'
            elif num == 401:
                print('worker error!')
                return '003 DISCONNECT'
            elif num == 402:
                print('turn error!')
                return '003 DISCONNECT'
            elif num == 501:
                print(self.state.get_board_information())
                print(self.state.get_resource_information())
                match_winner_msg = self.WINNER_MSGPTN.match(message)
                if match_winner_msg:
                    self.winner = match_winner_msg.group(1)
                    score = self.state.get_score()
                    reward = score[self.MY_ID] - score[self.OPP_ID]
                    with open(path, mode='a') as f:
                            f.write('\r\n'+str(reward)+'\r\n\r\n')
                    
                    print('winner is '+str(self.winner))
                return '000 NOTPLAY'
            elif num == 502:
                return '001 NEXT'
            else:
                return '000 NOTPLAY'

    def action(self, ID, place, worker):
        if self.state.can_put_worker(ID, place, worker):
            if ID == self.MY_ID:
                if place == '5-3':
                    trend = self.state.setting_trend()
                    self.state.set_trend(trend)
                    self.play_message = '205 PLAY ' + str(self.MY_ID) + ' ' + worker + ' ' + place + ' ' + trend
                else:
                    self.play_message = '205 PLAY ' + str(self.MY_ID) + ' ' + worker + ' ' + place
            print(self.state.get_board_information())
            print(self.state.get_resource_information())
            self.state.do_play(ID, place, worker)
            return True
        else:
            return False
  
    def play(self):
        workers = self.state.get_useable_workers()
        path = 'ai.txt'
        if workers[0][self.MY_ID] == 1:
            dql_solver = DQN_Solver(2,2)
            movables = self.can_put_P()
            if movables == []:
                return False

            action = dql_solver.choose_action(self.state.get_season(),movables)
            print(action)
            if action == '5-3':
                trend = self.state.setting_trend()
                self.state.set_trend(trend)
                self.play_message = '205 PLAY ' + str(self.MY_ID) + ' P ' + action + ' ' + trend
                with open(path, mode='a') as f:
                    f.write(action+','+'P'+', movables: ,')
                    for x in movables:
                        f.write(str(x)+',')
                    f.write('\r\n')
            else:
                self.play_message = '205 PLAY ' + str(self.MY_ID) + ' P ' + action
                with open(path, mode='a') as f:
                    f.write(action+','+'P'+', movables: ,')
                    for x in movables:
                        f.write(str(x)+',')
                    f.write('\r\n')

            print(self.state.get_board_information())
            print(self.state.get_resource_information())
            self.state.do_play(self.MY_ID, action, 'P')
            return True

        elif workers[2][self.MY_ID] >= 1:
            dql_solver = DQN_Solver(2,2)
            movables = self.can_put_S()
            if movables == []:
                return False

            action = dql_solver.choose_action(self.state.get_season(),movables)
            print(action)
            if action == '5-3':
                trend = self.state.setting_trend()
                self.state.set_trend(trend)
                self.play_message = '205 PLAY ' + str(self.MY_ID) + ' S ' + action + ' ' + trend
                with open(path, mode='a') as f:
                    f.write(action+','+'S'+', movables: ,')
                    for x in movables:
                        f.write(str(x)+',')
                    f.write('\r\n')
            
            else:
                self.play_message = '205 PLAY ' + str(self.MY_ID) + ' S ' + action
                with open(path, mode='a') as f:
                    f.write(action+','+'S'+', movables: ,')
                    for x in movables:
                        f.write(str(x)+',')
                    f.write('\r\n')
            
            print(self.state.get_board_information())
            print(self.state.get_resource_information())
            self.state.do_play(self.MY_ID, action, 'S')
            return True
        else:
            dql_solver = DQN_Solver(2,2)
            movables = self.can_put_A()
            if movables == []:
                return False

            action = dql_solver.choose_action(self.state.get_season(),movables)
            print(action)
            if action == '5-3':
                trend = self.state.setting_trend()
                self.state.set_trend(trend)
                self.play_message = '205 PLAY ' + str(self.MY_ID) + ' A ' + action + ' ' + trend
                with open(path, mode='a') as f:
                    f.write(action+','+'A'+', movables: ,')
                    for x in movables:
                        f.write(str(x)+',')
                    f.write('\r\n')
            
            else:
                self.play_message = '205 PLAY ' + str(self.MY_ID) + ' A ' + action
            print(self.state.get_board_information())
            print(self.state.get_resource_information())            
            self.state.do_play(self.MY_ID, action, 'A')
            with open(path, mode='a') as f:
                    f.write(action+','+'A'+', movables: ,')
                    for x in movables:
                        f.write(str(x)+',')
                    f.write('\r\n')
            
            return True
            
        return False

    def can_put_P(self):
        list1 = []
        if self.state.can_put_worker(self.MY_ID, '1-1', 'P'):
            list1 += ['1-1']
        if self.state.can_put_worker(self.MY_ID, '2-1', 'P'):
            list1 += ['2-1']
        if self.state.can_put_worker(self.MY_ID, '2-2', 'P'):
            list1 += ['2-2']
        if self.state.can_put_worker(self.MY_ID, '2-3', 'P'):
            list1 += ['2-3']
        if self.state.can_put_worker(self.MY_ID, '3-1', 'P'):
            list1 += ['3-1']
        if self.state.can_put_worker(self.MY_ID, '3-2', 'P'):
            list1 += ['3-2']
        if self.state.can_put_worker(self.MY_ID, '3-3', 'P'):
            list1 += ['3-3']
        if self.state.can_put_worker(self.MY_ID, '4-1', 'P'):
            list1 += ['4-1']
        if self.state.can_put_worker(self.MY_ID, '4-2', 'P'):
            list1 += ['4-2']
        if self.state.can_put_worker(self.MY_ID, '4-3', 'P'):
            list1 += ['4-3']
        if self.state.can_put_worker(self.MY_ID, '5-1', 'P'):
            list1 += ['5-1']
        if self.state.can_put_worker(self.MY_ID, '5-2', 'P'):
            list1 += ['5-2']
        if self.state.can_put_worker(self.MY_ID, '5-3', 'P'):
            list1 += ['5-3']
        if self.state.can_put_worker(self.MY_ID, '6-1', 'P'):
            list1 += ['6-1']
        if self.state.can_put_worker(self.MY_ID, '6-2', 'P'):
            list1 += ['6-2']

        return list1

    def can_put_S(self):
        list1 = []
        if self.state.can_put_worker(self.MY_ID, '1-1', 'S'):
            list1 += ['1-1']
        if self.state.can_put_worker(self.MY_ID, '2-1', 'S'):
            list1 += ['2-1']
        if self.state.can_put_worker(self.MY_ID, '2-2', 'S'):
            list1 += ['2-2']
        if self.state.can_put_worker(self.MY_ID, '2-3', 'S'):
            list1 += ['2-3']
        if self.state.can_put_worker(self.MY_ID, '3-1', 'S'):
            list1 += ['3-1']
        if self.state.can_put_worker(self.MY_ID, '3-2', 'S'):
            list1 += ['3-2']
        if self.state.can_put_worker(self.MY_ID, '3-3', 'S'):
            list1 += ['3-3']
        if self.state.can_put_worker(self.MY_ID, '4-1', 'S'):
            list1 += ['4-1']
        if self.state.can_put_worker(self.MY_ID, '4-2', 'S'):
            list1 += ['4-2']
        if self.state.can_put_worker(self.MY_ID, '4-3', 'S'):
            list1 += ['4-3']
        if self.state.can_put_worker(self.MY_ID, '5-1', 'S'):
            list1 += ['5-1']
        if self.state.can_put_worker(self.MY_ID, '5-2', 'S'):
            list1 += ['5-2']
        if self.state.can_put_worker(self.MY_ID, '5-3', 'S'):
            list1 += ['5-3']
        if self.state.can_put_worker(self.MY_ID, '6-1', 'S'):
            list1 += ['6-1']
        if self.state.can_put_worker(self.MY_ID, '6-2', 'S'):
            list1 += ['6-2']

        return list1

    def can_put_A(self):
        list1 = []
        if self.state.can_put_worker(self.MY_ID, '1-1', 'A'):
            list1 += ['1-1']
        if self.state.can_put_worker(self.MY_ID, '2-1', 'A'):
            list1 += ['2-1']
        if self.state.can_put_worker(self.MY_ID, '2-2', 'A'):
            list1 += ['2-2']
        if self.state.can_put_worker(self.MY_ID, '2-3', 'A'):
            list1 += ['2-3']
        if self.state.can_put_worker(self.MY_ID, '3-1', 'A'):
            list1 += ['3-1']
        if self.state.can_put_worker(self.MY_ID, '3-2', 'A'):
            list1 += ['3-2']
        if self.state.can_put_worker(self.MY_ID, '3-3', 'A'):
            list1 += ['3-3']
        if self.state.can_put_worker(self.MY_ID, '4-1', 'A'):
            list1 += ['4-1']
        if self.state.can_put_worker(self.MY_ID, '4-2', 'A'):
            list1 += ['4-2']
        if self.state.can_put_worker(self.MY_ID, '4-3', 'A'):
            list1 += ['4-3']
        if self.state.can_put_worker(self.MY_ID, '5-1', 'A'):
            list1 += ['5-1']
        if self.state.can_put_worker(self.MY_ID, '5-2', 'A'):
            list1 += ['5-2']
        if self.state.can_put_worker(self.MY_ID, '5-3', 'A'):
            list1 += ['5-3']
        if self.state.can_put_worker(self.MY_ID, '6-1', 'A'):
            list1 += ['6-1']
        if self.state.can_put_worker(self.MY_ID, '6-2', 'A'):
            list1 += ['6-2']

        return list1
        
    def reset_board(self):
        self.winner = -1
        self.play_message = None
        self.state = game.Game()
        self.state.set_player_name(self.MY_ID, self.MY_NAME)
        self.state.set_player_name(self.OPP_ID, 'opponent')