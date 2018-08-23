#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)

import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from Business.Check import login_check, sign_up_check
from Business.Notice import notice
from Public.Common import *
from Public.Path_manager import Root_xpath
from Public.Logger import Logger
from Interface.Index import index


logger = Logger('login').getlog()
class login():

    def __init__(self):
        Remember_statu='0'
        # 获取系统路劲
        self.root_x = Root_xpath()
        self.img_xpath=self.root_x.picture_path()
        self.account_path = self.root_x.config_path()+'/账号.dat'
        account_info = Pickle().load(self.account_path)         # 读取账号密码
        # 创建窗体
        self.root = tk.Tk()
        self.root.title('登录')
        self.root.iconbitmap(self.img_xpath+'/login_title2.ico')
        self.root.resizable(0, 0)  # 阻止Python GUI的大小调整
        self.x, self.y = WhidowsInfo().root_coordinate(self.root)
        self.root.geometry("530x350+%d+%d" % (self.x, self.y))
        #利用Canvas设置登录背景图片
        canvas = tk.Canvas(self.root, width=530, height=350, bg='white')  # 指定Canvas组件的背景色
        image = Image.open(self.img_xpath+"/login_bg.jpg")
        im = ImageTk.PhotoImage(image)
        canvas.create_image(348,130, image=im)  # 使用create_image将图片添加到Canvas组件中
        canvas.pack()  # 将Canvas添加到主窗口
        # 账号密码lable
        self.usr_name = tk.Label(self.root,text='账号:',bg='LightSkyBlue',font=("黑体", 13)).place(x=120,y=150)
        self.usr_pwd = tk.Label(self.root, text='密码:', bg='LightSkyBlue', font=("黑体", 13)).place(x=120, y=190)
        # 登录界面输入控件组创建
        self.var_usr_name = tk.StringVar()  # 设置按钮组，用于set账号密码
        self.var_usr_pwd = tk.StringVar()
        self.entry_usr_name = tk.Entry(self.root, textvariable=self.var_usr_name,bg='LightSkyBlue')
        self.entry_usr_name.place(x=190,y=150)
        self.entry_usr_pwd = tk.Entry(self.root,textvariable=self.var_usr_pwd,show='*',bg='LightSkyBlue')
        self.entry_usr_pwd.place(x=190,y=193)
        # 登录注册按钮
        self.login = tk.Button(self.root,text='登录',bg='DodgerBlue',command=self.usr_login).place(x=160,y=235)
        self.register = tk.Button(self.root, text='注册', bg='DodgerBlue',command=self.usr_sign_up).place(x=280, y=235)
        # 记住密码
        self.checkbox1 = tk.IntVar()
        self.remember_pwd = tk.Checkbutton(self.root,text='记住密码',variable=self.checkbox1,bg='Azure').place(x=350, y=190)
        # self.remember_pwd = tk.Checkbutton(self.root, text='忘记密码', variable=self.checkbox2, bg='DodgerBlue').place(x=350, y=147)
        self.input_accout_info(account_info)

        self.root.mainloop()


    def input_accout_info(self,account_info):
        '''
        输入账号密码信息
        :return:
        '''
        if account_info==False or account_info==None:
            pass
        else:
            # 自动输入账号
            self.var_usr_name.set(account_info['Account'])
            # 自动输入密码
            self.var_usr_pwd.set(account_info['Password'])
            # 勾选记住密码
            self.checkbox1.set(1)


    def save_accout_info(self,usr_name,usr_pwd):
        '''
        存入账号信息
        :param usr_name: 用户名
        :param usr_pwd: 密码
        :return:
        '''
        account_info={}
        account_info['Account'] = usr_name
        account_info['Password'] = usr_pwd
        save_state = Pickle().dump(account_info,self.account_path)  # 存账号密码
        if save_state==True:
            logger.info('账号信息保存成功!!')
        else:
            logger.info('账号信息保存失败!!')


    def usr_login(self):
        '''
        开始登录
        :return:
        '''
        # 获取输入的账号密码
        usr_name = self.entry_usr_name.get()
        usr_pwd = self.entry_usr_pwd.get()
        #实例化类
        log_chevk = login_check()
        # 判断账户信息
        statu = log_chevk.check_user_state(usr_name,usr_pwd)
        if statu == True:
            usr_Rad = self.checkbox1.get()
            if usr_Rad == 1 or usr_Rad == '1':  # 登陆成功判断用户是否记住密码
                self.save_accout_info(usr_name, usr_pwd)
            else:
               if os.path.exists(self.account_path):
                    os.remove(self.account_path)
            notice_text = notice().get_new_notice()     #获取公告
            tk.messagebox.showinfo(title='公告',
                                   message=notice_text)
            self.root.destroy()  # 隐藏登陆界面
            logger.info('%s登录成功' % usr_name)
            In =index()
        elif statu == False:
            tk.messagebox.showwarning(message='对不起，输入错误，请重试！')
        elif statu == None:
            is_sign_up = tk.messagebox.askquestion('Welcome', '您还没有注册，是否现在注册呢？')
            if is_sign_up == 'yes':
                self.usr_sign_up()
            else:
                pass
        elif statu=='chinese_error':
            tk.messagebox.showwarning(title='错误',message='账号密码不能含有中文字符')
        elif statu=='len_error':
            tk.messagebox.showwarning(title='错误', message='账号密码长度错误，请输入5-15个非中文字符！')

    # 用户注册
    def usr_sign_up(self):

        def sign_to_Pyhon():
            np = new_pwd.get()  #密码
            npc = new_pwd_confirm.get() #密码确认
            nn = new_name.get()  #账号
            phone = phone_confirm.get() #手机
            if len(np)!=0 and  len(npc)!=0 and len(nn)!=0 and len(phone)!=0:
                if npc == np:
                    sign_up = sign_up_check()
                    statu = sign_up.input_user_pwd(nn,np,phone)
                    if statu == 1 or statu=='1':
                        tk.messagebox.showinfo(title='注册成功', message='注册账号成功，请登陆')
                        window_sign_up.destroy()  # 隐藏窗口
                    elif statu == 0 or statu=='0':
                        tk.messagebox.showwarning(title='注册失败', message='注册失败，请稍后再试')
                    elif statu == 'username_exite':
                        tk.messagebox.showwarning(title='注册失败', message='注册账号已存在，请重新输入')
                    elif statu == 'phone_exite':
                        tk.messagebox.showwarning(title='注册失败', message='手机号码已存在，请更换手机注册')
                    elif statu == 'Legality_error':
                        tk.messagebox.showwarning(title='注册失败', message='账号密码长度错误，请输入5-15个非中文字符！')
                    elif statu == 'phone_len_error':
                        tk.messagebox.showwarning(title='注册失败', message='手机号码长度错误，请重新输入')
                    else:
                        tk.messagebox.showwarning(title='注册失败', message='未知异常，请重试~')
                else:
                    tk.messagebox.showwarning(title='注册失败', message='两次输入的密码不一致')
            else:
                tk.messagebox.showerror(title='错误',message='所有信息都为必填项目，请检查后重新填写')
                self.usr_sign_up()

        # 创建top窗口作为注册窗口
        window_sign_up = tk.Toplevel(self.root)
        window_sign_up.geometry("450x300+%d+%d" % (self.x,self.y))  # 居中显示
        window_sign_up.geometry('350x200')
        window_sign_up.title('注册')
        window_sign_up.config(bg='LightSkyBlue')


        # 账号框
        new_name = tk.StringVar()
        new_name.set('例如：guyue')
        tk.Label(window_sign_up, text='账号:',bg='LightSkyBlue').place(x=60, y=10)
        entry_new_name = tk.Entry(window_sign_up, textvariable=new_name)  # textvariable 设置默认
        entry_new_name.place(x=130, y=10)

        # 密码框
        new_pwd = tk.StringVar()
        tk.Label(window_sign_up, text='密码:',bg='LightSkyBlue').place(x=60, y=50)
        entry_usr_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, show='*')  # show 显示为*
        entry_usr_pwd.place(x=130, y=50)

        # 密码确认框
        new_pwd_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='再次输入:',bg='LightSkyBlue').place(x=60, y=90)
        entry_usr_pwd_again = tk.Entry(window_sign_up, textvariable=new_pwd_confirm, show='*')
        entry_usr_pwd_again.place(x=130, y=90)

        # 手机框
        phone_confirm = tk.StringVar()
        tk.Label(window_sign_up, text='手机号码:',bg='LightSkyBlue').place(x=60, y=130)
        entry_phone = tk.Entry(window_sign_up, textvariable=phone_confirm)
        entry_phone.place(x=130, y=130)

        # 注册按钮
        btn_again_sign_up = tk.Button(window_sign_up, text='注册', command=sign_to_Pyhon,bg='DodgerBlue')
        btn_again_sign_up.place(x=160, y=170)

t = login()