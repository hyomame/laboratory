# -*- coding: utf-8 -*-

class Resources:
    def __init__(self):
        self.money = 5
        self.reserch_point = 0
        self.score = [0, 0, 0]
        self.worker_list = [1, 0, 1]
        self.used_worker_list = [0, 0, 0]
        self.debt_count = 0
        self.start_player_flag = False

    def has_worker_of(self, type_of_worker):
        if type_of_worker == 'P':
            return self.worker_list[0] > 0
        elif type_of_worker == 'A':
            return self.worker_list[1] > 0
        elif type_of_worker == 'S':
            return self.worker_list[2] > 0

        return False

    def get_current_money(self):
        return self.money

    def add_money(self, i):
        self.money += i

    def already_hired_assistant(self):
        if self.worker_list[1] > 0:
            return True
        if self.used_worker_list[1] > 0:
            return True
        return False

    def put_worker(self, type_of_worker):
        if self.has_worker_of(type_of_worker):
            if type_of_worker == 'P':
                self.worker_list[0] -= 1
                self.used_worker_list[0] +=1
            elif type_of_worker == 'A':
                self.worker_list[1] -= 1
                self.used_worker_list[1] += 1
            elif type_of_worker == 'S':
                self.worker_list[2] -= 1
                self.used_worker_list[2] += 1

    def get_current_reserch_point(self):
        return self.reserch_point

    def add_reserch_point(self, i):
        self.reserch_point += i

    def has_worker(self):
        return (self.worker_list[0]+self.worker_list[1]+self.worker_list[2]) > 0

    def get_score_of(self, trend):
        if trend == 'T1':
            return self.score[0]
        elif trend == 'T2':
            return self.score[1]
        elif trend == 'T3':
            return self.score[2]

        return -1

    def get_total_score(self):
        return self.score[0] + self.score[1] + self.score[2] - 3 * self.debt_count

    def is_start_player(self):
        return self.start_player_flag

    def add_score_point(self, score_treand, point):
        self.score[score_treand] += point

    def add_new_student(self):
        self.used_worker_list[2] += 1

    def add_new_assistant(self):
        self.used_worker_list[1] += 1

    def return_all_workers(self):
        for i in range(3):
            self.worker_list[i] = self.used_worker_list[i]
            self.used_worker_list[i] = 0

    def pay_money_to_wokers(self):
        self.money -= self.worker_list[2]
        self.money -= 3*self.worker_list[1]
        if self.money < 0:
            self.debt_count += (-1)*self.money
            self.money = 0

    def set_start_player(self, b):
        self.start_player_flag = b

    def get_assistant(self):
        return self.worker_list[1] + self.used_worker_list[1]
    
    def get_total_students_count(self):
        return self.worker_list[2] + self.used_worker_list[2]
    
    def get_number_of_useable_workers(self, type_of_worker):
        if type_of_worker == 'P':
            return self.worker_list[0]
        elif type_of_worker == 'A':
            return self.worker_list[1]
        elif type_of_worker == 'S':
            return self.worker_list[2]

    def get_debt():
        return self.debt_count