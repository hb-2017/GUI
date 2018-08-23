#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : huxiansheng (you@example.org)


from Public.Mysqldb import Mysql

class notice():

    def __init__(self):
        self.sql = Mysql()

    def get_new_notice(self):
        '''
        获取最新的公告
        :return:select_text 最新公告内容   False无公告
        '''
        sql1 = 'select notice from notice order by caredtime limit 1'
        select_state,select_text = self.sql.open_sql(sql1)
        if select_state==1:
            return select_text
        else:
            return False