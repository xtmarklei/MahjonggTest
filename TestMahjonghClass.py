# -*- coding: UTF-8 -*-
import random
import time
from TestCalcMinCost import *
suit_tup = ('dot', 'bamboo', 'character')
name_arr = ('一筒', '二筒', '三筒', '四筒', '五筒', '六筒', '七筒', '八筒', '九筒', '一条', '二条', '三条', '四条',
            '五条', '六条', '七条', '八条', '九条', '一万', '二万', '三万', '四万', '五万', '六万', '七万', '八万', '九万')
players = []
def print_cards(cards):
    a = []
    b = []
    str_b = ''
    for i in cards:
        # print str(i) + ' , current_size =' + str(len(cards))
        a.append(i.number)
    #print a
    a.sort()
    print(a)
    for i in a:
        b.append(Card.get_name(i))
    for i in range(0,len(a)):
        str_b +=' ' + str(a[i]) + ':' + (b[i]).decode('UTF-8').encode('GBK') 
    print(str_b)
    
class Card:
    def __init__(self, number):
        self.suit = int(number/36)
        self.value = int((number%36)/4 + 1)
        self.number = number
    def __str__(self):
        return suit_tup[self.suit]+' :' + str(self.value) + '---->number:' + str(self.number)
    @staticmethod
    def get_suit(number):
        return int(number/36)
    @staticmethod
    def get_value(number):
        return  int((number%36)/4 + 1)
    @staticmethod
    def get_name(number):
        return name_arr[int(number/4)]

class CardWalls:
    cards=[]
    current_size=0
    key_cards = []
    root_card = None 
    @staticmethod
    def reset_cards():
        CardWalls.key_cards = []
        CardWalls.root_card = None
        CardWalls.cards=[]
        random_source = list(range(0,108))
        for i in range(0,108):
            # print 'i='+str(i)
            CardWalls.cards.append(Card(random_source.pop(random.randint(1,108-i)-1)))
            CardWalls.current_size += 1
    @staticmethod
    def print_yourself():
        print_cards(CardWalls.cards)
    @staticmethod
    def deal_card(num):
        if num == 1:
            return [CardWalls.cards.pop(0)]
        elif num == -1:
            return [CardWalls.cards.pop(-1)]
        else:
            return [CardWalls.cards.pop(0),CardWalls.cards.pop(0),CardWalls.cards.pop(0),CardWalls.cards.pop(0)]
    @staticmethod
    def get_keycard():
        CardWalls.root_card = CardWalls.cards.pop(0)
        key_card_suit = CardWalls.root_card.suit
        key_card_value = CardWalls.root_card.value%9 # 这里root_card.value已经有加一
        start_num = key_card_suit*36 + key_card_value*4
        CardWalls.key_cards = [start_num,start_num+1,start_num+2,start_num+3]
    
class Player:
    def __init__(self,index):
        self.index = index
        self.hh_index = 0
        self.hand_cards = []
        self.pong_cards = []
        # Exposed / Concealed Kong
        self.kong_cards = []
        self.discard_cards = []
        self.hand_number_list = []
        self.hand_key_list = []
    def reset(self):
        self.hh_index = 0
        self.hand_cards = []
        self.pong_cards = []
        # Exposed / Concealed Kong
        self.kong_cards = []
        self.discard_cards = []
        self.hand_number_list = []
        self.hand_key_list = []
    def get_4cards(self):
        self.hh_index += 1
        self.hand_cards.extend(CardWalls.deal_card(4))
        # Seq.callnextpalyer()
    def get_card(self):
        self.hh_index+=1
        self.hand_cards.extend(CardWalls.deal_card(1))
    def get_hand_list(self):
        if len(self.hand_number_list) == 0:
            for i in self.hand_cards:
                self.hand_number_list.append(i.number)
            self.hand_number_list.sort()
        return self.hand_number_list
    def cnt_key_cards(self):
        tmp_hand_list = []
        tmp_hand_key_list = []
        key_cnt = 0
        for i in self.hand_number_list:
            if i in CardWalls.key_cards:
                key_cnt += 1
                tmp_hand_key_list.append(i)
            else:
                tmp_hand_list.append(i)
        self.hand_number_list = tmp_hand_list
        self.hand_key_list = tmp_hand_key_list
        return key_cnt
def release_key_cards(card_list):
    for i in range(0,len(card_list)):
        if card_list[i] in CardWalls.key_cards:
            card_list.pop(i)

def init():
    if len(players) == 4:
        return
    for i in range(0,4):
        players.append(Player(i))

def start():
    CardWalls.reset_cards()
    # CardWalls.print_yourself()
    for i in players:
        i.reset()
    # 1st step 4 cards * 3 times
    for i in range(0,3):
        for p in players:
            p.get_4cards()
    # 2nd step 1 card
    for p in players:
        p.get_card()
    # 3nd now is a test
    # for p in players:
    #     p.get_card()
    # 4nd get key card
    CardWalls.get_keycard()

init()
# start()
# print 'root : '+ str(CardWalls.root_card)
# print 'keys : '+ str(CardWalls.key_cards)

# for i in players:
#     print 'player '+str(i.index)+'--->'
#     print_cards(i.hand_cards)
#     check_total_cost(i.get_hand_list())
#     print i.cnt_key_cards()
#     print i.hand_number_list
#     fan_list = check_total_cost(i.get_hand_list())
cnt_test_times = 0
print(time.asctime( time.localtime(time.time()) ))
while(True):
    cnt_test_times += 1
    start()
    # print 'root : '+ str(CardWalls.root_card)
    # print 'keys : '+ str(CardWalls.key_cards)
    tmk = 0
    for i in players:
        # print 'player '+str(i.index)+'--->'
        # print_cards(i.hand_cards)
        i.get_hand_list()
        i.cnt_key_cards() # print i.cnt_key_cards()
        # print i.hand_number_list
        fan_list = check_total_cost(i.get_hand_list())
        if (get_cost_for_all(fan_list) - i.cnt_key_cards()) <= 2:
            tmk = 1
    if tmk == 1:
        break
print(cnt_test_times)
print(time.asctime( time.localtime(time.time()) ))


