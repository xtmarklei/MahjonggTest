# -*- coding: UTF-8 -*-
# 递归算法：
# 每次减少三个元素，直到数组中所有的元素都不大于0
# 

def check_finished(cards_list):
    # check cards_list 如果所有元素都不大于0说明递归结束
    for i in cards_list:
        if i > 0:
            return False
    return True

def get_cost(cards_list):
    tmp = 0
    for i in cards_list:
        if i < 0:
            tmp -= i
    return tmp
def get_cost_for_all(l_cards_list):
    tmp = 0
    for i in l_cards_list:
        tmp += get_cost(i)
    return tmp

def try_type_s(cards_list):
    # copy 一份cards_list
    copy_list = cards_list[:]
    # 找出cards_list中第一个大于0的元素的index
    current_index = 9
    for i in range(0,9):
        if copy_list[i] > 0:
            current_index = i
            break
    if current_index < 7:
        copy_list[current_index] -=1
        copy_list[current_index+1] -=1
        copy_list[current_index+2] -=1
    elif current_index == 7:
        copy_list[current_index-1] -=1
        copy_list[current_index] -=1
        copy_list[current_index+1] -=1
    else:
        copy_list[current_index-2] -=1
        copy_list[current_index-1] -=1
        copy_list[current_index] -=1
    return copy_list

def try_type_t(cards_list):
    # copy 一份cards_list
    copy_list = cards_list[:]
    # 找出cards_list中第一个大于0的元素的index
    current_index = 9
    for i in range(0,9):
        if copy_list[i] > 0:
            current_index = i
            break
    copy_list[current_index] -=3
    return copy_list

# type_s = [1,1,1]
# type_t = [3]
# 递归找出最小cost
def check_s_cost(cards_list):
    # print cards_list
    if check_finished(cards_list):
        return cards_list
    l_type_s = check_s_cost(try_type_s(cards_list))
    l_type_t = check_s_cost(try_type_t(cards_list))
    cost_type_s = get_cost(l_type_s)
    cost_type_t = get_cost(l_type_t)
    if cost_type_s > cost_type_t:
        return l_type_t
    else:
        return l_type_s

def check_r_cost(cards_list):
    l_r_cost=[]
    min_cost = 99
    rst_cost = []
    for i in range(0,len(cards_list)):
        if cards_list[i] > 0:
            # copy 一份cards_list
            copy_list = cards_list[:]
            copy_list[i] -= 2
            l_r_cost.append(check_s_cost(copy_list))
    if len(l_r_cost)==0:
        return [-2,0,0,0,0,0,0,0,0]
    else:
        for r_cost in l_r_cost:
            crt_r_cost = get_cost(r_cost)
            if crt_r_cost < min_cost:
                rst_cost = r_cost
                min_cost = crt_r_cost
        return rst_cost
# suit_tup = ('dot','bamboo','character')
def format_checking_list(src_list):
    dot_list = [0,0,0,0,0,0,0,0,0]
    bamboo_list = [0,0,0,0,0,0,0,0,0]
    character_list = [0,0,0,0,0,0,0,0,0]
    tmp_list = [dot_list,bamboo_list,character_list]
    for i in src_list:
        tmp_list[int(i/9)][int(i%9)] += 1
    return tmp_list
def min_value(a,b):
    if a > b:
        return b
    else:
        return a
def check_total_cost(src_list):
    f_a_list = format_checking_list(src_list)
    # print(f_a_list)
    s_cost_list = []
    r_cost_list = []
    all_cost_list = [r_cost_list,s_cost_list]
    for i in f_a_list:
        s_cost_list.append(check_s_cost(i))
        r_cost_list.append(check_r_cost(i))
    tmp_total_cost = get_cost(r_cost_list[0])+ get_cost(s_cost_list[1])+get_cost(s_cost_list[2])
    rst_list = [r_cost_list[0],s_cost_list[1],s_cost_list[2]]
    if tmp_total_cost > (get_cost(s_cost_list[0])+ get_cost(r_cost_list[1])+get_cost(s_cost_list[2])):
        tmp_total_cost = get_cost(s_cost_list[0])+ get_cost(r_cost_list[1])+get_cost(s_cost_list[2])
        rst_list = [s_cost_list[0],r_cost_list[1],s_cost_list[2]]
    if tmp_total_cost > (get_cost(s_cost_list[0])+ get_cost(s_cost_list[1])+get_cost(r_cost_list[2])):
        tmp_total_cost = get_cost(s_cost_list[0])+ get_cost(s_cost_list[1])+get_cost(r_cost_list[2])
        rst_list = [s_cost_list[0],s_cost_list[1],r_cost_list[2]]
    # print rst_list,tmp_total_cost
    return rst_list


