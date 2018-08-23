#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)

import logging
import os.path
import time

from Public.Path_manager import Root_xpath


class Logger(object):

    def __init__(self, logger):
        '''''
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中，当天的日志存在一个txt文件，不同月份，用目录区分
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 获取日志保存的路劲
        logs_path = Root_xpath().logger_path()
        # 切分系统当前时间，用于区分二级目录保存
        month = time.strftime("%m", time.localtime(time.time()))
        day = time.strftime("%d", time.localtime(time.time()))
        logs_path = logs_path + r'/' + month + '月'
        report_statu = os.path.exists(logs_path)
        if report_statu == False:
            os.makedirs(logs_path)
        logs_path = logs_path + '/' + day +'日日志' + '.log'
        #创建日志输入端，fh输入到日志文件，ch输出到控制台，定义日志级别为info
        fh = logging.FileHandler(logs_path,encoding='utf-8')
        fh.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s[line:%(lineno)d] - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


    def getlog(self):
        return self.logger

