#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : set_config.py
# @Author   : yht
# @Date     : 2020/02/23
# @Desc     : 公共方法


import configparser
import os


# 获取当前路径
curPath = os.path.abspath(os.path.dirname(__file__))
# 获取根路径
rootPath = curPath[:curPath.find("automatic_test")+len("automatic_test")]



class Set_Section:
    def __init__(self, section_name,filename='namelist'):
        self.section_name = section_name
        self.config = configparser.ConfigParser()
        self.file = rootPath + f'/common/configuration/{filename}.ini'
        self.config.read(self.file,encoding='utf-8')
    def add_section(self,key='',value=''):
        self.config.add_section(self.section_name)
        self.config.set(self.section_name, key, value)
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def read_section(self,key=''):
        # print('read',self.section_name)
        # print(key)
        value = self.config.get(self.section_name,key)
        # print(value)
        return value
    def edit_section(self,key='',value=''):
        self.config.set(self.section_name, key, value)
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def remove_section(self,key='',value=''):
        self.config.remove_option(self.section_name,key)
        self.config.remove_section(self.section_name)
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def is_exit(self):
        result = self.config.has_section(self.section_name)
        return result

class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        # print(d)
        for k in d:
            d[k] = dict(d[k])
        # print(d)

        return d

