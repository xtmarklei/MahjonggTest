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
kong_flag = 0 # flag for kong
pong_flag = 0 # flag for pong, if is 1 means last loop is pong couldn't win directly.
discard_key_flag = 0 # flag for someone discard key card, if is 1 means only can win by himself.
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
        global discard_key_flag
        discard_key_flag = 0
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
        # this is the property use to set the player type
        # if property is 0 means pong or kong always happend
        # if property is 1 means pong or kong always not happend
        # if property is 2 means before pong or kong will check cost
        # if property is 3 means this player is a human
        self.auto_player_type = 0
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
        global pong_flag
        if pong_flag == 1: # last loop is self pong, so couldn't win
            return False
        pong_flag = 0
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
        if len(self.hand_cards) == 0:
            return CardWalls.key_card
        discard_choice_list = self.select_min_cost_list()
        return random.choice(discard_choice_list)
    def discard_by_idx(self,idx):
        self.hand_cards.remove(idx)
        self.discard_cards.append(idx)
        return idx
    def discard_key_card(self):
        global discard_key_flag
        discard_key_flag = 1
        self.key_cnt -=1

    # if has key card couldn't win
    # if someone had discard key card couldn't win
    def check_win_after_discard(self,idx):
        global discard_key_flag
        if discard_key_flag == 1:
            return False
        if self.key_cnt > 0:
            return False
        checking_list = self.hand_cards[:]
        checking_list.append(idx)
        checking_list.sort()
        win_cost = get_cost_for_all(check_total_cost(checking_list))
        return self.key_cnt >= win_cost
    def check_kong_after_discard(self,idx):
        tmp_cnt = 0
        for i in self.hand_cards:
            if i == idx:
                tmp_cnt += 1
        return tmp_cnt == 3
    def check_pong_after_discard(self,idx):
        tmp_cnt = 0
        for i in self.hand_cards:
            if i == idx:
                tmp_cnt += 1
        return tmp_cnt == 2
    def compare_cost_for_kong(self,idx): # judge it's worth kong or not
        if self.auto_player_type == 0:
            return 1
        elif self.auto_player_type == 1:
            return 0
        elif self.auto_player_type == 2:
            pass
            # calc cost then return
            return 0
        else:
            pass
            # human do the action then return
            return 1
    def check_cost_for_pong(self,idx): # judge it's worth pong or not
        if self.auto_player_type == 0:
            return 1
        elif self.auto_player_type == 1:
            return 0
        elif self.auto_player_type == 2:
            pass
            # calc cost then return
            return 0
        else:
            pass
            # human do the action then return
            return 1
    def do_exposed_kong(self,idx):
        for i in range(0,3):
            self.hand_cards.remove(idx)
        self.kong_cards.append(idx)
        return
    def do_action_pong(self,idx):
        for i in range(0,2):
            self.hand_cards.remove(idx)
        self.pong_cards.append(idx)
        return
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
    global player_header
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
# after discard check for other players win, pong or kong
# normal return 0 means will do next loop
# if return -1 means someone win the game and game over
# if return -2 means CardWall is empty
def check_win_pong_kong(player_index,discard_card):
    global current_player
    global pong_flag
    global kong_flag
    win_end_flag = 0
    for i in range(0,3):
        c_idx = (player_index+i+1)%4
        if players[c_idx].check_win_after_discard(discard_card):
            print('Player '+str(player_index) + ' lost &' + ' Player ' +str(c_idx) +' Win !!!!')
            print_cards(players[c_idx].hand_cards)
            print('Win for card is '+ str(discard_card))
            win_end_flag += 1
    if win_end_flag >= 1:
        return -1
    for i in range(0,3):
        c_idx = (player_index+i+1)%4
        # if CardWall.cards empty couldn't kong !
        if players[c_idx].check_kong_after_discard(discard_card) and len(CardWalls.cards) > 0:
            kong_cost = players[c_idx].compare_cost_for_kong(discard_card)
            if kong_cost == 1:# if kong cost < no action then kong
                players[c_idx].do_exposed_kong(discard_card)
                players[c_idx].get_reversed_card() # get a revert card then return
                players[c_idx].release_key_cards()
                current_player = c_idx
                kong_flag = 1
                print('Player ' +str(c_idx)+' Kong -->'+str(discard_card) )
                return 0
            else: # if kong cost > no action then do nothing
                pass
    for i in range(0,3):
        c_idx = (player_index+i+1)%4
        if players[c_idx].check_pong_after_discard(discard_card):
            pong_cost = players[c_idx].check_cost_for_pong(discard_card)
            if pong_cost == 1: # if pong cost < no action then pong
                players[c_idx].do_action_pong(discard_card)
                current_player = c_idx
                pong_flag = 1
                print('Player ' +str(c_idx)+' Pong -->'+str(discard_card) )
                return 0
            else: # pong cost > no action then do nothing
                pass
    if len(CardWalls.cards) == 0:
        print('CardWall.card empty Game over !!!!!!!')
        return -2
    # nothing happend go next player
    next_player = get_next_player(current_player)
    current_player = next_player
    players[current_player].get_card()
    players[current_player].release_key_cards()
    return 0

def play_loop():
    global current_player
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
            players[current_player].release_key_cards()
            continue

        # debug
        current_cost = get_cost_for_all(check_total_cost(players[current_player].hand_cards))
        print(str(players[current_player].hand_cards) + ' current cost = ' + str(current_cost) + ' key_cnt = ' + str(players[current_player].key_cnt))

        # here no action need to discard
        intent_discard_card = players[current_player].get_random_min_discard()
        if intent_discard_card == CardWalls.key_card: # if hand only has key card
            players[current_player].discard_key_card()
            players[current_player].get_reversed_card()
            players[current_player].release_key_cards()
            print('player '+str(current_player)+ ' discard key card !!!!!! ----> ' + str(intent_discard_card))
            continue
        

        players[current_player].discard_by_idx(intent_discard_card)
        # need check other 3 players
        # check_win_pong_kong(current_player,discard_card) return nextplayer_index, if != -1 continue
        play_flag = check_win_pong_kong(current_player,intent_discard_card)
        if play_flag == -1:
            break # game over
        elif play_flag == -2:
            break

init() #init only do one time

start()
