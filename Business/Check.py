#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)
from Public.Common import *
from Public.Mysqldb import Mysql


class login_check():
    '''
    登录的业务逻辑校验
    '''
    def __init__(self):
        self.sql = Mysql()

    def check_username_pwd_Legality(self,username,pwd):
        '''
        校验账号密码的合法性
        :param username:
        :param pwd:
        :return:None 账号密码长度不符  True没有包含中文字符  False包含中文字符
        '''
        if len(username)<5 or len(username)>15 or len(pwd)<5 or len(pwd)>15 :
            return None
        else:
            chinese_user = Str_manager().check_contain_chinese(username)
            chinese_pwd = Str_manager().check_contain_chinese(pwd)
            if chinese_user==None and chinese_pwd==None:
                return True
            else:
                return False


    def check_user_state(self,username,pwd):
        '''
        校验用户名的正确的，是否存在
        :param username: 用户名
        :param pwd: 密码
        :return:None 用户名不存在   True 账号密码正确  False 密码错误
        '''
        Legality = self.check_username_pwd_Legality(username,pwd)
        if Legality==True:
            select_satatu = self.sql.selete(table_name='user_info',check_field='pwd',condition="username='%s'"%username)
            if str(select_satatu)=='()':
                return None
            elif select_satatu[0][0]==pwd:
                return True
            else:
                return False
        elif Legality==False:
            return 'chinese_error'
        else:
            return 'len_error'



class sign_up_check():
    '''
    注册的业务逻辑校验
    '''
    def input_user_pwd(self,username,pwd,phone):
        '''
        插入注册信息
        :param username: 用户名
        :param pwd:密码
        :param phone:手机号码
        :return:add_state=1 注册成功  add_state=0 注册失败  username_exite 用户名已存在  phone_exite 手机已存在
        Legality_error 账号密码不合法  phone_len_error 手机号码长度不正确
        '''
        now = WhidowsInfo().get_window_time()
        log_check = login_check()
        Legality = log_check.check_username_pwd_Legality(username,pwd)
        # 验证注册信息的合法性
        if len(phone)==11 :
            if Legality==True:
                select_state = log_check.sql.selete(table_name='user_info',check_field='phone',condition='phone=%s'%phone)
                # 验证手机号码是否被注册
                if str(select_state) == '()':
                    select_state2 = log_check.sql.selete(table_name='user_info',check_field='username',condition='username=%s'%username)
                    if str(select_state2) == '()':
                        c1='username,pwd,creadtime,phone'
                        VALUES = "'%s','%s','%s','%s'"%(username,pwd,now,phone)
                        add_state = log_check.sql.add(table_name='user_info',field_str=c1,value_str=VALUES)
                        return add_state
                    else:
                        return 'username_exite'
                else:
                    return 'phone_exite'
            else:
                return 'Legality_error'
        else:
            return 'phone_len_error'