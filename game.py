# -*- coding: utf-8 -*-

import board
import resources

"""
 ゲームの進行状況を管理するクラス
 手を打てるプレイヤーや得点を管理する
"""

class Game:
    STATE_WAIT_PLAYER_CONNECTION = 0
    STATE_WAIT_PLAYER_PLAY = 1
    STATE_SEASON_END = 2
    STATE_GAME_END = 4
    #最大思考時間
    #max_thinking_time = 1000*60*5

    SEASON_NAMES = ['1a', '1b', '2a', '2b', '3a', '3b', '4a', '4b', '5a', '5b', '5a', '5b']
    TREND_ID_LIST = ['T1', 'T2', 'T3']
    
    def __init__(self):
        self.game_board = board.Board()
        
        self.game_resources = [resources.Resources(), resources.Resources()]
        self.game_resources[0].set_start_player(True)
        
        self.current_start_player = 0
        self.current_player = 0
        self.player_name = [None, None]
        self.game_state = self.STATE_WAIT_PLAYER_CONNECTION
        
        self.current_season = 0
        self.trend_ID = -1
        
        """
        self.timer_thread = new TimerThread()
        new Thread(self.timerThread).start()
        
        #self.set_changed()
        #self.notify_observers()
        


    タイマー
    private TimerThread timerThread
    """
    
    #ゲームの状況を取得する
    def get_game_state(self):
        return self.game_state
    
    def get_player_name(self):
        return self.player_name
    
    """
    def get_all_resouces(self):
        resources = [[self.game_resources[0].get_current_reserch_point(), self.game_resources[1].get_current_reserch_point()],
                     [self.game_resources[0].get_current_money(), self.game_resources[1].get_current_money()],
                     [self.game_resources[0].get_total_score(),self.game_resources[1].get_total_score()]]
        return resources
    """
    def get_useable_workers(self):
        workers = [[self.game_resources[0].get_number_of_useable_workers('P'), self.game_resources[1].get_number_of_useable_workers('P')],
                   [self.game_resources[0].get_number_of_useable_workers('A'), self.game_resources[1].get_number_of_useable_workers('A')],
                   [self.game_resources[0].get_number_of_useable_workers('S'), self.game_resources[1].get_number_of_useable_workers('S')]]
        return workers
    """
    def get_all_workers(self):
        workers = [[1, 1],
                   [self.game_resources[0].get_assistant(), self.game_resources[1].get_assistant()],
                   [self.game_resources[0].get_total_students_count(), self.game_resources[1].get_total_students_count()]]
        return workers
    """
    
    def get_score(self):
        score = [self.game_resources[0].get_total_score(), self.game_resources[1].get_total_score()]
        return score
    
    def get_current_player(self):
        return self.current_player
    
    """
    #時間計測開始
    def timer_start(PlayerID):
        self.timerThread.StartTimeCount(PlayerID)
    
    /** 時間計測終了 */
    public void TimerStop(int PlayerID):
        self.timerThread.StopTimeCount(PlayerID)
    

    public void setObserver(Observer gui):
        self.addObserver(gui)
    
    
    public void setTimerObserver(Observer gui):
        self.timerThread.addObserver(gui)
    
    
    //以下はボードの状態を変更するメソッドのため、呼び出し時はObserverに必ず通知すること
    """

    """
    手が打てるか事前に検証するメソッド。実際にはPLAYとやることは変わらない
    @param PlayerID
    @param workerType
    @param place
    @return 
    """
    def can_put_worker(self, player, place, type_of_worker):
        return self.play(player, place, type_of_worker, False)

    """
    実際に手を打つメソッド  
    @param player
    @param place
    @param type_of_worker
    @return 
    """
    def do_play(self, player, place, type_of_worker):
        return self.play(player, place, type_of_worker, True)
    
    """
    実際に手を打つメソッドで最後の引数により打てるかの調査なのかが決まる
    @param player
    @param place
    @param type_of_worker
    @param putmode Trueの場合は実際に手を打つ
    @return 
    """
    def play(self, player, place, type_of_worker, putmode):

        if self.game_state != self.STATE_WAIT_PLAYER_PLAY:
            return False

        if self.current_player != player:
            return False
        
        if not self.game_resources[player].has_worker_of(type_of_worker):
            return False
        
        if not self.game_board.can_put_worker(player, place):
            return False

        #リソースが十分かどうかを確認
        if place == '1-1':
            if putmode:
                self.game_board.put_worker(player, place, type_of_worker)
                self.game_resources[player].put_worker(type_of_worker)
                self.change_player()
                #self.set_changed()
                #self.notify_observers()
            
            return True
        
        if place[0] == '2':
            if self.game_resources[player].get_current_money() >= 2:
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].add_money(-2)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    ##self.notify_observers()
                
                return True
            else:
                return False
        
        if place == '3-1':
            if self.game_resources[player].get_current_reserch_point() >= 2:
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].add_reserch_point(-2)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    #self.notify_observers()
                
                return True
            else:
                return False
            
        if place == '3-2':
            if self.game_resources[player].get_current_reserch_point() >= 4 and self.game_resources[player].get_current_money() >= 1:
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].add_money(-1)
                    self.game_resources[player].add_reserch_point(-4)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    #self.notify_observers()
                
                return True
            else:
                return False
            
        if place == '3-3':
            if self.game_resources[player].get_current_reserch_point() >= 8 and self.game_resources[player].get_current_money() >= 1:
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].add_money(-1)
                    self.game_resources[player].add_reserch_point(-8)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    #self.notify_observers()
                
                return True
            else:
                return False
            
        if place[0] == '4':
            if self.game_resources[player].get_current_reserch_point() >= 8 and self.game_resources[player].get_current_money() >= 1:
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].add_money(-1)
                    self.game_resources[player].add_reserch_point(-8)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    #self.notify_observers()
                
                return True
            else:
                return False
        
        #タイプが問題ないかを確認
        if place == '5-1':
            if type_of_worker == 'P' or type_of_worker == 'A':
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    #self.notify_observers()
                
                return True
            else:
                return False
        
        if place == '5-2':
            if self.game_resources[player].get_current_reserch_point() >= 1:
                if type_of_worker == 'P' or type_of_worker == 'A':
                    if putmode:
                        self.game_resources[player].add_reserch_point(-1)
                        self.game_board.put_worker(player, place, type_of_worker)
                        self.game_resources[player].put_worker(type_of_worker)
                        self.change_player()
                        #self.set_changed()
                        #self.notify_observers()
                    
                    return True
                else:
                    return False
            else:
                return False
        
        if place == '5-3':
            if self.game_resources[player].get_current_reserch_point() >= 3:
                if type_of_worker == 'P' or type_of_worker == 'A':
                    if putmode:
                        self.game_resources[player].add_reserch_point(-3)
                        self.game_board.put_worker(player, place, type_of_worker)
                        self.game_resources[player].put_worker(type_of_worker)
                        self.change_player()
                        #self.set_changed()
                        #self.notify_observers()
                    
                    return True
                else:
                    return False
            else:
                return False
        
        if place == '6-1':
            if self.game_resources[player].get_current_reserch_point() >= 3:
                if type_of_worker == 'P' or type_of_worker == 'A':
                    if putmode:
                        self.game_resources[player].add_reserch_point(-3)
                        self.game_board.put_worker(player, place, type_of_worker)
                        self.game_resources[player].put_worker(type_of_worker)
                        self.change_player()
                        #self.set_changed()
                        #self.notify_observers()
                    
                    return True
                else:
                    return False
                
        if place == '6-2':
            if self.game_resources[player].already_hired_assistant(): 
                return False
            if type_of_worker == 'P' and self.game_resources[player].get_total_score() >= 10:
                if putmode:
                    self.game_board.put_worker(player, place, type_of_worker)
                    self.game_resources[player].put_worker(type_of_worker)
                    self.change_player()
                    #self.set_changed()
                    #self.notify_observers()
                
                return True
            else:
                return False
        
        return False
   
    """
    タイムアウトが発生した場合
    public void pass(int playerID):
        強制的にゼミに打たれる？
        throw new UnsupportedOperationException('Not supported yet.') //To change body of generated methods, choose Tools | Templates.
          #self.set_changed()
          #self.notify_observers()
    """
            
    #通常の手番切換え
    def change_player(self):
        #self.timerThread.StopTimeCount(self.current_player)

        if self.game_resources[(self.current_player+1) % 2].has_worker():
            #相手に手がうつせる場合
            self.current_player = (self.current_player+1) % 2
            #self.timerThread.StartTimeCount(self.current_player)
            #self.set_changed()
            #self.notify_observers()
            return
        else:
            #相手がもう手が打てない場合
            if self.game_resources[self.current_player].has_worker():
                #自分がまだ打てるんであれば、そのまま自分の手番で継続
                #self.timerThread.StartTimeCount(self.current_player)
                #self.set_changed()
                #self.notify_observers()
                return
            else:
                #互いに手が打てないのであれば、季節を進める
                self.current_player = -1
                self.game_state = self.STATE_SEASON_END
                self.change_new_season()
                #self.set_changed()
                #self.notify_observers()
                return
            
    #ボードそのもののメソッドを呼び出すための取得
    def get_board(self):
        return self.game_board
    
    
    def set_player_name(self, ID, name):
        if self.game_state == self.STATE_WAIT_PLAYER_CONNECTION and ID >= 0 and ID < 2:
            self.player_name[ID] = name
        
        if self.player_name[0] != None and self.player_name[1] != None:
            self.game_state = self.STATE_WAIT_PLAYER_PLAY

        return ID
        
        #self.set_changed()
        #self.notify_observers()
    
    """
    RESOURCES [01] P[01] A[01] S[0-9]+ M[1-9]*[0-9]+ R[1-9]*[0-9]+ D[0-9]+
    プレイヤーID（SP）コマの種類と残り個数（ SP 区切り）Mお金（SP）R研究力（SP） D負債
    を構造もつメッセージを返す
    @param playerID 0または1
    @return 
    """
    def get_resources_message_of(self, playerID):
        message = 'RESOURCES ' +\
                  str(playerID) + ' ' +\
                  'P' + str(self.game_resources[playerID].get_number_of_useable_workers('P')) + ' ' +\
                  'A' + str(self.game_resources[playerID].get_number_of_useable_workers('A')) + ' ' +\
                  'S' + str(self.game_resources[playerID].get_number_of_useable_workers('S')) + ' ' +\
                  'M' + str(self.game_resources[playerID].get_current_money()) + ' ' +\
                  'R' + str(self.game_resources[playerID].get_current_reserch_point()) + ' ' +\
                  'D' + str(self.game_resources[playerID].getDebt())
        return message
    
    def get_worker_name_of(self, place):
        workers = self.game_board.get_workers_on_board()
        return workers.get(place)
    
    def get_season(self):
        return self.SEASON_NAMES[self.current_season]
    

    def get_trend(self):
        if self.trend_ID < 0:
            return 'T0'
        elif self.trend_ID < 3:
            return self.TREND_ID_LIST[self.trend_ID]
        else:
            return 'T0'

    def get_score_of(self, trend, playerID):
        return self.game_resources[playerID].get_score_of(trend)
    

    #季節の進行
    def change_new_season(self):
        if self.game_state == self.STATE_SEASON_END:
            workers = self.get_board().get_workers_on_board()
            #ゼミによる研究ポイントの獲得
            seminorwokers = workers.get('1-1')
            if seminorwokers != None:
                PACount = 0
                SCount = [0, 0]
                for w in seminorwokers:
                    if w == 'P0':
                        PACount += 1
                        self.game_resources[0].add_reserch_point(2)
                    elif w == 'P1':
                        PACount += 1
                        self.game_resources[1].add_reserch_point(2)
                    elif w == 'A0':
                        PACount += 1
                        self.game_resources[0].add_reserch_point(3)
                    elif w == 'A1':
                        PACount += 1
                        self.game_resources[1].add_reserch_point(3)
                    elif w == 'S0':
                        SCount[0] += 1
                    elif w == 'S1':
                        SCount[1] += 1
                    
                self.game_resources[0].add_reserch_point((SCount[0]+SCount[1])//2 * PACount * SCount[0])
                self.game_resources[1].add_reserch_point((SCount[0]+SCount[1])//2 * PACount * SCount[1])

            
            #実験による研究ポイントの獲得
            keys = ['2-1', '2-2', '2-3']
            points = [3, 4, 5]
            for i, key in enumerate(keys):
                if key in workers.keys():
                    worker = workers.get(key)
                    if worker[-1] == '0':
                        self.game_resources[0].add_reserch_point(points[i])
                    elif worker[-1] == '1':
                        self.game_resources[1].add_reserch_point(points[i])

            #発表による業績の獲得
            score_trend = 0
            if self.current_season == 0 or self.current_season == 1 or self.current_season == 6 or self.current_season == 7:
                score_trend = 0
            elif self.current_season == 2 or self.current_season == 3 or self.current_season == 8 or self.current_season == 9:
                score_trend = 1
            elif self.current_season == 4 or self.current_season == 5 or self.current_season == 10 or self.current_season == 11:
                score_trend = 2

            key = '3-1'
            if key in workers.keys():
                w = workers.get(key)
                if w == 'P0':
                    self.game_resources[0].add_score_point(score_trend, 1)
                elif w == 'P1':
                    self.game_resources[1].add_score_point(score_trend, 1)
                elif w == 'A0':
                    self.game_resources[0].add_score_point(score_trend, 1)
                elif w == 'A1':
                    self.game_resources[1].add_score_point(score_trend, 1)
                elif w == 'S0':
                    self.game_resources[0].add_score_point(score_trend, 2)
                elif w == 'S1':
                    self.game_resources[1].add_score_point(score_trend, 2)    

            key = '3-2'
            if key in workers.keys():
                w = workers.get(key)
                if w == 'P0':
                    self.game_resources[0].add_score_point(score_trend, 3)
                elif w == 'P1':
                    self.game_resources[1].add_score_point(score_trend, 3)
                elif w == 'A0':
                    self.game_resources[0].add_score_point(score_trend, 4)
                elif w == 'A1':
                    self.game_resources[1].add_score_point(score_trend, 4)
                elif w == 'S0':
                    self.game_resources[0].add_score_point(score_trend, 4)
                elif w == 'S1':
                    self.game_resources[1].add_score_point(score_trend, 4)
  
            key = '3-3'
            if key in workers.keys():
                w = workers.get(key)
                if w == 'P0':
                    self.game_resources[0].add_score_point(score_trend, 7)
                elif w == 'P1':
                    self.game_resources[1].add_score_point(score_trend, 7)
                elif w == 'A0':
                    self.game_resources[0].add_score_point(score_trend, 6)
                elif w == 'A1':
                    self.game_resources[1].add_score_point(score_trend, 6)
                elif w == 'S0':
                    self.game_resources[0].add_score_point(score_trend, 5)
                elif w == 'S1':
                    self.game_resources[1].add_score_point(score_trend, 5)

            #論文による業績の獲得
            key = '4-1'
            if key in workers.keys():
                w = workers.get(key)
                if w == 'P0':
                    self.game_resources[0].add_score_point(score_trend, 8)
                elif w == 'P1':
                    self.game_resources[1].add_score_point(score_trend, 8)
                elif w == 'A0':
                    self.game_resources[0].add_score_point(score_trend, 7)
                elif w == 'A1':
                    self.game_resources[1].add_score_point(score_trend, 7)
                elif w == 'S0':
                    self.game_resources[0].add_score_point(score_trend, 6)
                elif w == 'S1':
                    self.game_resources[1].add_score_point(score_trend, 6)

            key = '4-2'
            if key in workers.keys():
                w = workers.get(key)
                if w == 'P0':
                    self.game_resources[0].add_score_point(score_trend, 7)
                elif w == 'P1':
                    self.game_resources[1].add_score_point(score_trend, 7)
                elif w == 'A0':
                    self.game_resources[0].add_score_point(score_trend, 6)
                elif w == 'A1':
                    self.game_resources[1].add_score_point(score_trend, 6)
                elif w == 'S0':
                    self.game_resources[0].add_score_point(score_trend, 5)
                elif w == 'S1':
                    self.game_resources[1].add_score_point(score_trend, 5)

            key = '4-3'
            if key in workers.keys():
                w = workers.get(key)
                if w == 'P0':
                    self.game_resources[0].add_score_point(score_trend, 6)
                elif w == 'P1':
                    self.game_resources[1].add_score_point(score_trend, 6)
                elif w == 'A0':
                    self.game_resources[0].add_score_point(score_trend, 5)
                elif w == 'A1':
                    self.game_resources[1].add_score_point(score_trend, 5)
                elif w == 'S0':
                    self.game_resources[0].add_score_point(score_trend, 4)
                elif w == 'S1':
                    self.game_resources[1].add_score_point(score_trend, 4)

            #スタートプレイヤーの決定
            key = '5-1'
            if key in workers.keys():
                worker = workers.get(key)
                if worker[-1] == '0':
                    self.current_start_player = 0
                    self.game_resources[0].add_money(3)
                    self.game_resources[0].set_start_player(True)
                    self.game_resources[1].set_start_player(False)
                elif worker[-1] == '1':
                    self.current_start_player = 1
                    self.game_resources[1].add_money(3)
                    self.game_resources[0].set_start_player(False)
                    self.game_resources[1].set_start_player(True)

            self.current_player = self.current_start_player

            #お金の獲得
            key = '5-2'
            if key in workers.keys():
                worker = workers.get(key)
                if worker[-1] == '0':
                    self.game_resources[0].add_money(5)
                elif worker[-1] == '1':
                    self.game_resources[1].add_money(5)

            key = '5-3'
            if key in workers.keys():
                worker = workers.get(key)
                if worker[-1] == '0':
                    self.game_resources[0].add_money(6)
                elif worker[-1] == '1':
                    self.game_resources[1].add_money(6)

            #トレンドを動かす処理はPLAY時に指定する必要ありなので要調整

            #コマの獲得
            key = '6-1'
            if key in workers.keys():
                worker = workers.get(key)
                if worker[-1] == '0':
                    self.game_resources[0].add_new_student()
                elif worker[-1] == '1':
                    self.game_resources[1].add_new_student()

            key = '6-2'
            if key in workers.keys():
                worker = workers.get(key)
                if worker[-1] == '0':
                    self.game_resources[0].add_new_assistant()
                elif worker[-1] == '1':
                    self.game_resources[1].add_new_assistant()

            #ボードのコマを全部戻す
            path = 'ai.txt'
            with open(path, mode='a') as f:
                f.write('\r\n')
            self.game_resources[0].return_all_workers()
            self.game_resources[1].return_all_workers()
            self.get_board().return_all_workers()

            if self.current_season == 11:
                #最後の季節の終了
                self.game_state = self.STATE_GAME_END
            elif self.current_season % 2 == 1:
                #奇数は表彰のある季節なので表彰する
                add_money = 5
                if self.current_season == 1 or self.current_season == 7:
                    if self.trend_ID == 0:
                        add_money += 3 
                    if self.game_resources[0].get_score_of('T1') == self.game_resources[1].get_score_of('T1'):
                        self.game_resources[0].add_money(add_money)
                        self.game_resources[1].add_money(add_money)
                    elif self.game_resources[0].get_score_of('T1') > self.game_resources[1].get_score_of('T1'):
                        self.game_resources[0].add_money(add_money)
                    else:
                        self.game_resources[1].add_money(add_money)
                    
                elif self.current_season == 3 or self.current_season == 9:
                    if self.trend_ID == 1:
                        add_money += 3 
                    if self.game_resources[0].get_score_of('T2') == self.game_resources[1].get_score_of('T2'):
                        self.game_resources[0].add_money(add_money)
                        self.game_resources[1].add_money(add_money)
                    elif self.game_resources[0].get_score_of('T2') > self.game_resources[1].get_score_of('T2'):
                        self.game_resources[0].add_money(add_money)
                    else:
                        self.game_resources[1].add_money(add_money)
                    
                elif self.current_season == 5:
                    if self.trend_ID == 2:
                        add_money += 3 
                    if self.game_resources[0].get_score_of('T3') == self.game_resources[1].get_score_of('T3'):
                        self.game_resources[0].add_money(add_money)
                        self.game_resources[1].add_money(add_money)
                    elif self.game_resources[0].get_score_of('T3') > self.game_resources[1].get_score_of('T3'):
                        self.game_resources[0].add_money(add_money)
                    else:
                        self.game_resources[1].add_money(add_money)
                    
                
                #季節を一つ進める
                self.current_season += 1
                #雇っているコストのお金を支払う
                self.game_resources[0].pay_money_to_wokers()
                self.game_resources[1].pay_money_to_wokers()
                self.game_state = self.STATE_WAIT_PLAYER_PLAY
            else:
                #表彰なく進行する場合
                #季節を一つ進める
                self.current_season += 1
                #雇っているコストのお金を支払う
                self.game_resources[0].pay_money_to_wokers()
                self.game_resources[1].pay_money_to_wokers()
                self.game_state = self.STATE_WAIT_PLAYER_PLAY

    def get_start_player(self):
        if self.game_resources[0].is_start_player():
            return 0
        else:
            return 1

    def set_trend(self, trend):
        for i, key in enumerate(self.TREND_ID_LIST):
            if key == trend:
                self.trend_ID = i

    """
    CUI出力用
    現在のボードの状態（どこに誰のコマがおいてあるか）を文字列で出力
    @return 
    """
    def get_board_information(self):
        workers = self.get_board().get_workers_on_board()
        if self.game_state == self.STATE_WAIT_PLAYER_CONNECTION:
            return 'プレイヤー接続待ち'
        
        message = '/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_//_/_/_/_/_/_/_/\n' +\
                  '/_/_/_/_/_/_/_/  ボードの状態  /_/_/_/_/_/_/_/\n' +\
                  '/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_//_/_/_/_/_/_/_/\n' +\
                  '1-1 ゼミの配置状況\n' +\
                  self.change_list_to_string(workers.get('1-1', 'not')) + '\n' +\
                  '2 実験の配置状況\n' +\
                  '2-1:' + workers.get('2-1', 'not') + '\n' +\
                  '2-2:' + workers.get('2-2', 'not') + '\n' +\
                  '2-3:' + workers.get('2-3', 'not') + '\n' +\
                  '3 発表の配置状況\n' +\
                  '3-1:' + workers.get('3-1', 'not') + '\n' +\
                  '3-2:' + workers.get('3-2', 'not') + '\n' +\
                  '3-3:' + workers.get('3-3', 'not') + '\n' +\
                  '4 論文の配置状況\n' +\
                  '4-1:' + workers.get('4-1', 'not') + '\n' +\
                  '4-2:' + workers.get('4-2', 'not') + '\n' +\
                  '4-3:' + workers.get('4-3', 'not') + '\n' +\
                  '5 研究報告の配置状況\n' +\
                  '5-1:' + workers.get('5-1', 'not') + '\n' +\
                  '5-2:' + workers.get('5-2', 'not') + '\n' +\
                  '5-3:' + workers.get('5-3', 'not') + '\n' +\
                  '6 雇用の配置状況\n' +\
                  '6-1:' + workers.get('6-1', 'not') + '\n' +\
                  '6-2:' + workers.get('6-2', 'not') + '\n' +\
                  '----------------------------------------------\n' +\
                  '時間経過と研究成果\n' +\
                  '現在の季節：' + self.get_season() + '\n' +\
                  '現在のトレンド：' + self.get_trend() + '\n' +\
                  'トレンド1のスコア：Player0=' + str(self.game_resources[0].get_score_of('T1')) + ',Player1=' + str(self.game_resources[1].get_score_of('T1')) + '\n' +\
                  'トレンド2のスコア：Player0=' + str(self.game_resources[0].get_score_of('T2')) + ',Player1=' + str(self.game_resources[1].get_score_of('T2')) + '\n' +\
                  'トレンド3のスコア：Player0=' + str(self.game_resources[0].get_score_of('T3')) + ',Player1=' + str(self.game_resources[1].get_score_of('T3')) + '\n' +\
                  '----------------------------------------------\n' +\
                  '現在プレイ待ちのプレイヤー：Player' + str(self.current_player) + '(' + self.player_name[self.current_player] + ')\n' +\
                  'スタートプレイヤー：Player' + str(self.current_start_player) + '\n' +\
                  '/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/\n'
        return message

    """
    CUI出力用
    現在のリソース状態（各プレイヤーが持つリソース）を文字列で出力
    @return
     """
    def get_resource_information(self):
        if self.game_state == self.STATE_WAIT_PLAYER_CONNECTION:
            return 'プレイヤー接続待ち'

        message = '/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_//_/_/_/_/_/_/_/\n' +\
                  '/_/_/_/_/_/_/_/  ボードの状態  /_/_/_/_/_/_/_/\n' +\
                  '/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_//_/_/_/_/_/_/_/\n' +\
                  self.get_individual_resource_information(0) +\
                  self.get_individual_resource_information(1) +\
                  '/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_//_/_/_/_/_/_/_/\n'
        return message
    
    
    def get_individual_resource_information(self, playerID):
        message = 'Player' + str(playerID) + '(' + self.player_name[playerID] + ')\n' +\
                  '----------------------------------------------\n' +\
                  '1 コマの利用可能状況\n' +\
                  '教授:' + str(self.game_resources[playerID].has_worker_of('P')) + '\n' +\
                  '助手:' + str(self.game_resources[playerID].has_worker_of('A')) + '\n' +\
                  '学生:' + str(self.game_resources[playerID].has_worker_of('S')) + '\n' +\
                  '学生コマの保持数:' +\
                  str(self.game_resources[playerID].get_total_students_count()) + '\n' +\
                  '2 資金と研究ポイントの状況\n' +\
                  'お金:' + str(self.game_resources[playerID].get_current_money()) + '\n' +\
                  '研究ポイント:' + str(self.game_resources[playerID].get_current_reserch_point()) + '\n' +\
                  '3 総合得点:' + str(self.game_resources[playerID].get_total_score()) + '\n'
        return message
    
    """
    def print_message(self, text):
        #self.set_changed()
        self.notify_observers(text)
    """

    def get_resources_of(self, i):
        if i==0 or i==1:
            return self.game_resources[i]
        
        return None
    
    def get_player_name_of(self, i):
        if i==0 or i==1:
            return self.player_name[i]
        
        return ''
    
    def setting_trend(self):
        if self.current_season==0 or self.current_season==1 or self.current_season==6 or self.current_season==7:
            setting_trend = 'T1'
        elif self.current_season==2 or self.current_season==3 or self.current_season==8 or self.current_season==9:
            setting_trend = 'T2'
        elif self.current_season==4 or self.current_season==5 or self.current_season==10 or self.current_season==11:
            setting_trend = 'T3'
        return setting_trend
    
    def change_list_to_string(self, seminor_list):
        return ':'.join(seminor_list)