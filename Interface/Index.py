#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)

import tkinter as tk
from PIL import Image, ImageTk
from Public.Logger import Logger
from Public.Path_manager import Root_xpath
from Public.Common import *

logger = Logger('index').getlog()
class index():

    def __init__(self):
        #实例化类
        self.root_x = Root_xpath()
        self.img_xpath = self.root_x.picture_path()   #图片存放路劲

        #创建窗体
        self.index = tk.Tk()
        self.index.title('古月')
        self.index.iconbitmap(self.img_xpath + '/login_title2.ico')
        self.index.resizable(0,0) # 阻止调整窗体大小
        self.a, self.b = WhidowsInfo().root_coordinate(self.index)
        self.index.geometry("830x550+%d+%d" % (self.a, self.b)) #设置窗体大小和位置
        # 创建画布
        canvas = tk.Canvas(self.index,width=830, height=550, bg='white')
        image = Image.open(self.img_xpath+'/index_bg.jpg')
        im = ImageTk.PhotoImage(image)
        canvas.create_image(348, 250, image=im)  # 使用create_image将图片添加到Canvas组件中
        canvas.pack()  # 将Canvas添加到主窗口

        # 创建菜单栏
        menubar = tk.Menu(self.index)
        fmenu1 = tk.Menu(self.index)  #创建菜单项(下拉选项)1
        for item in ['新建', '打开', '保存', '另存为']:
            fmenu1.add_command(label=item) # 循环添加到fmenu1下拉选项
        fmenu2 = tk.Menu(self.index)
        for item in ['编辑', '复制', '粘贴', '剪贴']:
            fmenu2.add_command(label=item)
        fmenu3 = tk.Menu(self.index)
        for item in [ '版权信息', '使用说明', '关于我们']:
            fmenu3.add_command(label=item)
        menubar.add_cascade(label="文件", menu=fmenu1)
        menubar.add_cascade(label="工具", menu=fmenu2)
        menubar.add_cascade(label="帮助", menu=fmenu3)
        self.index['menu'] = menubar  # 最后可以用窗口的 menu 属性指定我们使用哪一个作为它的顶层菜单

        self.index.mainloop()


