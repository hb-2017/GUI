#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-31 18:23:36
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os

#项目路劲
class Root_xpath():
    '''
    返回值
    root_path 系统根目录路劲
    '''
    def __init__(self):
        '''
        获取项目的根目录
        :return:str 项目的根目录
        '''
        root_path_ = os.getcwd()
        _path = root_path_.split('GUI')
        self.root_path = _path[0] + 'GUI'


    def rootpath(self):
        '''
        项目的根目录
        :return:
        '''
        return self.root_path


    def logger_path(self):
        '''
        日志的根目录
        :return:
        '''
        logger_path = self.root_path + '/Data/log'
        return logger_path


    def config_path(self):
        '''
        配置文件的存放路劲
        :return:
        '''
        config_path = self.root_path + '/Data/Configs'
        return config_path


    def picture_path(self):
        '''
        图片的存放路劲
        :return:
        '''
        config_path = self.root_path + '/Data/picture'
        return config_path