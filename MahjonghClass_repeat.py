# -*- coding: UTF-8 -*-
import random
import time
from CalcMinCost_repeat import *
suit_tup = ('dot', 'bamboo', 'character')
name_value_arr = ('一', '二', '三', '四', '五', '六', '七', '八', '九')
name_suit_arr  = ('筒','条','万')

players = []
player_header = 0
play_seq = []
def print_cards(cards_list):
    str_cards_with_index = ''
    for i in range(0,len(cards_list)):
        str_cards_with_index += str(cards_list[i]) + ':' + name_value_arr[Card.get_value(cards_list[i])] + name_suit_arr[Card.get_suit(cards_list[i])] + ' '
        if i%16==15:
            print(str_cards_with_index)
            str_cards_with_index = ''
    print(str_cards_with_index)
    
class Card:
    @staticmethod
    def get_card_index(number):
        return int(number/4)
    @staticmethod
    def get_suit(index):
        return int(index/9)
    @staticmethod
    def get_value(index):
        return  int(index%9)
    @staticmethod
    def calc_index_by_suit_value(suit, value):
        return int(suit*9+value)

class CardWalls:
    cards=[]
    root_card=-1
    key_card=-1
    @staticmethod
    def reset_cards():
        CardWalls.key_card = -1
        CardWalls.root_card = -1
        CardWalls.cards=[]
        random_source = list(range(0,108))
        for i in range(0,108):
            CardWalls.cards.append(Card.get_card_index(random_source.pop(random.randint(1,108-i)-1)))
        # print(CardWalls.cards)
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
        key_card_suit = Card.get_suit(CardWalls.root_card)
        key_card_value = (Card.get_value(CardWalls.root_card)+1)%9
        CardWalls.key_card = Card.calc_index_by_suit_value(key_card_suit, key_card_value)
    
class Player:
    def __init__(self,index):
        self.index = index
        self.hh_index = 0
        self.key_cnt = 0
        self.hand_cards = []
        self.pong_cards = []
        # Exposed / Concealed Kong
        self.kong_cards = []
        self.discard_cards = []
    def reset(self):
        self.hh_index = 0
        self.key_cnt = 0
        self.hand_cards = []
        self.pong_cards = []
        # Exposed / Concealed Kong
        self.kong_cards = []
        self.discard_cards = []
    def get_4cards(self):
        self.hh_index += 1
        self.hand_cards.extend(CardWalls.deal_card(4))
        self.hand_cards.sort()
        # Seq.callnextpalyer()
    def get_card(self):
        self.hh_index+=1
        self.hand_cards.extend(CardWalls.deal_card(1))
        self.hand_cards.sort()
    def get_reversed_card(self):
        self.hh_index+=1
        self.hand_cards.extend(CardWalls.deal_card(-1))
        self.hand_cards.sort()
    def release_key_cards(self):
        for i in self.hand_cards:
            if i == CardWalls.key_card:
                self.key_cnt += 1
        self.hand_cards = list(filter(lambda x:x !=CardWalls.key_card,self.hand_cards))
    def cnt_key_cards(self):
        self.release_key_cards()
        return self.key_cnt
    def check_self_win(self):
        win_cost = get_cost_for_all(check_total_cost(self.hand_cards))
        return self.key_cnt >= win_cost
    def check_concealed_kong(self):
        repeat_cnt = 1
        last_cardnum =-1
        for i in self.hand_cards:
            if i == last_cardnum:
                repeat_cnt += 1
            else:
                last_cardnum = i
                repeat_cnt = 1
            if repeat_cnt == 4:
                return last_cardnum
        return -1
    def do_concealed_kong(self,card_idx):
        self.kong_cards.append(card_idx)
        self.hand_cards = list(filter(lambda x:x !=card_idx,self.hand_cards))
    # this for auto play select the min cost card
    def select_min_cost_list(self):
        tmp_last_card = -1
        tmp_min_cost = 99
        tmp_result_list = []
        for i in self.hand_cards:
            if tmp_last_card == i:
                continue
            copy_list = self.hand_cards[:]
            copy_list.remove(i)
            tmp_copy_cost = get_cost_for_all(check_total_cost(copy_list))
            if tmp_min_cost > tmp_copy_cost: # if min cost is changed recreate a new rst list
                tmp_result_list = []
                tmp_result_list.append(i)
                tmp_min_cost = tmp_copy_cost
            elif tmp_min_cost == tmp_copy_cost: # if min cost == current cost add current idx to rst list
                tmp_result_list.append(i)
            tmp_last_card = i
        return tmp_result_list
    # for auto play function
    def get_random_min_discard(self):
        discard_choice_list = self.select_min_cost_list()
        return random.choice(discard_choice_list)
    def discard_by_idx(self,idx):
        self.hand_cards.remove(idx)
        self.discard_cards.append(idx)
        return idx

def init():
    global player_header
    global players
    if len(players) == 4:
        return
    players = []
    player_header = 0
    for i in range(0,4):
        players.append(Player(i))

def start():
    global play_seq
    CardWalls.reset_cards()
    CardWalls.print_yourself()
    play_seq = []
    for i in range(0,4):
        play_seq.append((i+player_header)%4)
    print('play_seq ----->>>>>> ' + str(play_seq))
    for i in players:
        i.reset()
    # 1st step get 4 cards * 3 times for all
    for i in range(0,3):
        for idx in play_seq:
            players[idx].get_4cards()
    # 2nd step get 1 card for all
    for idx in play_seq:
        players[idx].get_card()
    # 3rd step get 1 card for 1st player
    players[player_header].get_card()
    # 4th step get key card
    CardWalls.get_keycard()
    # 5th step cnt keys for all
    for idx in play_seq:
        players[idx].release_key_cards()
    
    print('Here We Go !--------------->>>>>>>>>>>>>>>>')
    print('KEY--->>>'+str(CardWalls.key_card))
    print(len(CardWalls.cards))
    # 6th enter play_loop
    play_loop()

def get_next_player(idx):
    return (idx+1)%4

def play_loop():
    current_player = player_header
    while(True):
        # check win
        if players[current_player].check_self_win():
            print('player '+str(current_player) + ' win the game !!!!!!!!!!!!!!!!!')
            current_cost = get_cost_for_all(check_total_cost(players[current_player].hand_cards))
            print(str(players[current_player].hand_cards) + ' current cost = ' + str(current_cost) 
                + ' key_cnt = ' + str(players[current_player].key_cnt))
            print_cards(players[current_player].hand_cards)
            break
        # check kong
        kong_rst_card = players[current_player].check_concealed_kong()
        if kong_rst_card >= 0 and len(CardWalls.cards) > 0: # if CardWall.cards empty couldn't kong ! 
            print('player '+str(current_player)+ ' kong ' + str(kong_rst_card))
            players[current_player].do_concealed_kong(kong_rst_card)
            players[current_player].get_reversed_card()
            continue

        # debug
        current_cost = get_cost_for_all(check_total_cost(players[current_player].hand_cards))
        print(str(players[current_player].hand_cards) + ' current cost = ' + str(current_cost) + ' key_cnt = ' + str(players[current_player].key_cnt))

        # here no action need to discard
        intent_discard_card = players[current_player].get_random_min_discard()
        players[current_player].discard_by_idx(intent_discard_card)
        # need check other 3 players
        # check_win_pong_kong(current_player,discard_card) return nextplayer_index, if != -1 continue

        if len(CardWalls.cards) == 0:
            print('CardWall.card empty Game over !!!!!!!')
            break
        # nothing happend go next player
        current_player = get_next_player(current_player)
        players[current_player].get_card()
        players[current_player].release_key_cards()

init() #init only do one time

start()

# cnt_test_times = 0
print(time.asctime( time.localtime(time.time()) ))

print(time.asctime( time.localtime(time.time()) ))


