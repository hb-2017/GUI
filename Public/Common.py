#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)

import pickle
import re
import time
from Public.Logger import Logger


class WhidowsInfo():
    '''
    电脑环境信息
    '''
    logger = Logger('WhidowsInfo').getlog()
    def root_coordinate(self,root):
        '''
        窗口坐标
        获取电脑的分辨率，并判断中间位置
        :param root: 主窗口控件
        :return:返回屏幕中间坐标
        '''
        ws = root.winfo_screenmmwidth()
        hs = root.winfo_screenheight()
        x = (ws/2)+400
        y = (hs/2)-250
        self.logger.info('当前屏幕分辨率为%sx%s,中间坐标为%s,%s'%(ws,hs,x,y))
        return x,y


    def get_window_time(self):
        '''
        获取本地时间
        :return:
        '''
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 格式化当前时间
        return now


class Pickle():
    '''
    二进制文件读取
    '''
    logger = Logger('Pickle').getlog()
    def load(self,file_path):
        '''
        读取二进制文件
        :return:
        '''
        try:
            f = open(file_path, 'rb')
            file_datas = pickle.load(f)  # 读出文件的数据个数
            f.close()
        except Exception as e:
            self.logger.error('读取二进制文件【%s】失败,无法自动填写账号密码,错误信息:%s'%(file_path,e))
            file_datas =False
        return file_datas


    def dump(self,obj,path):
        '''
        写入文件
        :param obj: 写入文件的对象
        :param path: 路劲
        :return:
        '''
        try:
            f = open(path, 'wb')  # 以写模式打开二进制文件
            pickle.dump(obj,f)
            f.close()
            return True
        except Exception as e:
            self.logger.error('写入二进制文件【%s】失败,错误异常:%s' % (path, e))
            return False


class Str_manager():
    logger = Logger('Str_manager').getlog()
    # 检验字符串是否包含汉字
    def check_contain_chinese(self,check_str):
        '''
        判断传入字符串是否包含中文
        :param word: 待判断字符串
        :return: None:不包含中文 False:输入的不是字符串
        '''
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        try:
            match = zh_pattern.search(check_str)
            return match
        except:
            return False
