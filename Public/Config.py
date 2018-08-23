#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-01-31 18:33:22
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import configparser
import os
from Public.Path_manager import Root_xpath
from Public.Logger import Logger

logger = Logger(logger='Config').getlog()


class Config():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_xpath = Root_xpath().config_path() + '/'

    def get_config_data(self, config_name, config_section, config_options):
        '''
        获取配置文件信息
        参数
        config_name  配置文件名称
        config_title 配置文件组名
        config_value 配置文件键名
        返回值
        False 获取配置文件失败，值为空
        values 配置文件信息
        '''
        values = []
        try:
            if len(config_name) > 1:
                config_xpath = self.config_xpath + config_name + '.ini'
                self.config.read(config_xpath, encoding="utf-8-sig")
                # 单组配置读取
                if len(config_section) == 1:
                    value = []
                    for item in config_options:
                        item = self.config.get(config_section[0], item)
                        values.append(item)
                    logger.info('获取单组配置信息：%s 成功' % values)
                # 多组配置读取
                elif len(config_section) > 1:
                    for title in config_section:
                        value = []
                        for item in config_options:
                            item = self.config.get(title, item)
                            value.append(item)
                        values.append(value)
                        logger.info('获取多组配置信息：%s 成功 ' % values)
                elif len(config_section) == 0 or len(config_section) == None or len(config_options) == 0 or len(
                        config_options) == None:
                    logger.error('配置文件组名或组键为空,获取配置失败...')
                    return False
                else:
                    logger.error('配置文件路劲为空,获取配置失败...')
                    return False
        except Exception as e:
            logger.error('获取配置信息失败:%s' % e)
            return False
        finally:
            return values


    def config_file_is_exist(self, config_name):
        '''
        判断配置文件是否存在
        :param config_name: 配置文件名称
        :return:file_True：存在  file_False 不存在  e 异常信息
        '''
        try:
            file_statu = os.path.exists(self.config_xpath + config_name + '.ini')
            if file_statu == True:
                return 'file_True'
            else:
                return 'file_False'
        except Exception as e:
            return e


    def config_section_is_exist(self, config_name, config_section):
        '''
        判断配置文件的单个section是否存在
        :param config_name: 配置文件名称
        :param config_section:section名称
        :return:section_True 存在  section_False不存在  file_False配置文件不存在
        '''

        config_exist = self.config_file_is_exist(config_name)
        if config_exist == 'file_True':
            self.config.read(self.config_xpath + config_name + '.ini', encoding='utf-8-sig')  # 读取ini配置文件
            section_exist = self.config.has_section(config_section)
            if section_exist == True:
                return 'section_True'
            else:
                return 'section_False'
        else:
            return 'file_False'


    def config_option_is_exist(self, config_name, config_section, config_option):
        '''
        判断配置文件中section的单个options的是否存在
        :param config_name:
        :param config_section:
        :param config_options:
        :return:option_True 存在  option_False不存在
        '''
        section_exist = self.config_section_is_exist(config_name, config_section)
        option_exist_list = []
        if section_exist == 'section_True':
            self.config.read(self.config_xpath + config_name + '.ini')  # 读取ini配置文件
            # 单个options
            if type(config_option) == str:
                option_exist = self.config.has_option(config_section, config_option)
                if option_exist == True:
                    option_exist_list.append('option_True')
                    return option_exist_list
                else:
                    option_exist_list.append('option_False')
                    return option_exist_list
            # 多个options循环判断返回列表
            elif type(config_option) == list:
                for i in config_option:
                    option_exist = self.config.has_option(config_section, i)
                    if option_exist == True:
                        option_exist_list.append('option_True')
                    else:
                        option_exist_list.append('option_False')
                return option_exist_list
        else:
            return section_exist


    def add_section(self, config_name, config_section):
        '''
        新增section
        :param config_name:
        :param config_section:
        :param config_option:
        :return:True 增加成功  False 增加失败  section_True 存在  section_False不存在  file_False配置文件不存在
        '''
        section_exist = self.config_section_is_exist(config_name, config_section)
        if section_exist == 'section_False':
            try:
                self.config.read(self.config_xpath + config_name + '.ini')  # 读取ini配置文件
                self.config.add_section(config_section)
                # 写入文件
                with open(self.config_xpath + config_name + '.ini', 'w') as fw:
                    self.config.write(fw)
                fw.close()
                return True
            except:
                return False
        else:
            return section_exist


    def add_option(self, config_name, config_section, config_option, value):
        '''
        增加option
        :param config_name:
        :param config_section:
        :param config_option:
        :return: option_type_error：config_option,value类型不相同   value_number_error：config_option,value 数量不一致
                 True：单个option增加成功 ['True','True'] 多个增加成功，一个列代表一个option
                 section_False:section不存在  file_False:配置文件不存在 option_True:option已存在
        '''
        option_exist = self.config_option_is_exist(config_name, config_section, config_option)
        if type(option_exist) == list:
            self.config.read(self.config_xpath + config_name + '.ini')  # 读取ini配置文件
            # 判断option是单个还是多个
            if type(config_option) == list and type(value) == list:
                if len(config_option) == len(value):
                    # 循环判断各个option的状态并处理
                    option = []
                    for item, i in enumerate(option_exist):
                        if i == 'option_False' or option_exist == 'section_True':
                            self.config.set(config_section, config_option[item], value[item])
                            # 写入文件
                            with open(self.config_xpath + config_name + '.ini', 'w') as fw:
                                self.config.write(fw)
                            fw.close()
                            option.append('True')
                        else:
                            option.append(i)
                    return option
                else:
                    return 'value_number_error'
            # 单个处理
            elif type(config_option) == str and type(value) == str:
                if option_exist[0] == 'option_False' or option_exist == 'section_True':
                    self.config.set(config_section, config_option, value)
                    # 写入文件
                    with open(self.config_xpath + config_name + '.ini', 'w') as fw:
                        self.config.write(fw)
                    fw.close()
                    return True
                else:
                    return option_exist[0]
            else:
                return 'option_type_error'
        else:
            return option_exist

    def updata_option(self, config_name, config_section, config_option, value):
        '''
        增加option
        :param config_name: 日志名称
        :param config_section: 需要更改的section
        :param config_option:  需要更改的option
        param： value：更改的值
        :return: option_type_error：config_option,value类型不相同   value_number_error：config_option,value 数量不一致
                 True：单个option增加成功 ['True','True'] 多个增加成功，一个列代表一个option
                 section_False:section不存在  file_False:配置文件不存在  option_False:optionbu 不存在
        '''
        option_exist = self.config_option_is_exist(config_name, config_section, config_option)
        if type(option_exist) == list:
            self.config.read(self.config_xpath + config_name + '.ini')  # 读取ini配置文件
            # 判断option是单个还是多个
            if type(config_option) == list and type(value) == list:
                if len(config_option) == len(value):
                    # 循环判断各个option的状态并处理
                    option = []
                    for item, i in enumerate(option_exist):
                        if i == 'option_True':
                            self.config.set(config_section, config_option[item], value[item])
                            # 写入文件
                            with open(self.config_xpath + config_name + '.ini', 'w') as fw:
                                self.config.write(fw)
                            fw.close()
                            option.append('True')
                        else:
                            option.append(i)
                    return option
                else:
                    return 'value_number_error'
            # 单个处理
            elif type(config_option) == str and type(value) == str:
                if option_exist[0] == 'option_True':
                    self.config.set(config_section, config_option, value)
                    # 写入文件
                    with open(self.config_xpath + config_name + '.ini', 'w') as fw:
                        self.config.write(fw)
                    fw.close()
                    return True
                else:
                    return option_exist[0]
            else:
                return 'option_type_error'
        else:
            return option_exist

    def section_all_data(self, config_name, config_section):
        '''
        返回单个section中所有的键和值
        :param config_name: 配置文件名称
        :param config_section: 配置块
        :return: 字典形式的键和值
        '''
        section_data = {}
        section_state = self.config_section_is_exist(config_name, config_section)
        if section_state == 'section_True':
            self.config.read(self.config_xpath + config_name + '.ini', encoding='utf-8-sig')
            options = self.config.options(config_section)
            for option in options:
                option_value = self.config.get(config_section, option)
                section_data[option] = option_value
            return section_data
        else:
            return section_state