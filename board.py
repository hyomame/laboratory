# -*- coding: utf-8 -*-

"""
 盤面を管理するクラス
 辞書型で状態を取得可能で,
 テキストによる出力も可能
 
 -1:誰もおいていない
 0:プレイヤー0の設置
 1:プレイヤー1の設置
 とする。
 
 ワーカー配置のメソッドを持つ
"""

class Board:
    PLACE_NAMES = ['1-1', '2-1', '2-2', '2-3', '3-1', '3-2', '3-3', '4-1', '4-2', '4-3', '5-1', '5-2', '5-3', '6-1', '6-2']
    PLAYER_COUNT = 2
    board_state = {}
    
    def __init__(self):
        for key in self.PLACE_NAMES:
            self.board_state[key] = ''
        self.seminor_workers = []
    
    #季節の変わり目などにボード上におかれたワーカーをすべて除去する
    def return_all_workers(self):
        for key in self.PLACE_NAMES:
            self.board_state[key] = ''
        self.seminor_workers = []
    
    """
    ピース設置可能かの判定
    第1引数:player プレイヤー番号0または1
    第2引数:pice 設置場所
    
    戻り値は設置可能かどうかのブール値
    """
    def can_put_worker(self, player, place):
        if player < 0 or player > 1:
            #プレイヤー番号が不正
            return False

        if place not in self.PLACE_NAMES:
            #設置場所が不正
            return False

        #1-1はいくつでもピースを受け入れ可能
        if place == '1-1':
            return True

        #その場所に既にコマがおかれているかを確認
        if self.board_state[place] != '':
            return False

        #設置誓約がある場所かを確認
        if place == '2-2':
            if self.board_state['2-1'] == '':
                return False

        if place == '2-3':
            if self.board_state['2-2'] == '':
                return False

        if place == '4-2':
            if self.board_state['4-1'] == '':
                return False

        if place == '4-3':
            if self.board_state['4-2'] == '':
                return False
        
        #以上の条件に引っかからなければOK
        return True

    """
    コマを設置するメソッド
    第1引数:player プレイヤー番号0または1
    第2引数:place 設置場所
    第3引数:worker ワーカーの種類
    """

    def put_worker(self, player, place, worker):
        if not self.can_put_worker(player, place):
            return False
        
        if place == '1-1':
            self.seminor_workers.append(worker + str(player))
        else:
            self.board_state[place] = worker + str(player)

        return True
    
    def get_seminor_workers(self):
        return self.seminor_workers
    
    def get_workers_on_board(self):
        workers = {}
        for key in self.PLACE_NAMES:
            if key == '1-1':
                if self.seminor_workers:
                    workers[key] = self.seminor_workers
            else:
                if self.board_state[key]:
                    workers[key] = self.board_state[key]

        return workers

    def print_current_board(self):
        for key in self.PLACE_NAMES:
            if key == '1-1':
                print('1-1:', end = '')
                print(self.seminor_workers)
            else:
                print(key + ':', end = '')
                print(self.board_state[key])
