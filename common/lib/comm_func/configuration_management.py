#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : configuration_management.py
# @Author   : yht
# @Date     : 2020/02/28
# @Update   : 日期加名称
# @Desc     : 配置项管理

from common.lib.venv.api_path import *
from common.lib.login.web_login import Web_Login


class ModifyConfig(Web_Login):
    def modify_config(self,key,value,comment='',namespace='tech.name'):
        res_result = self.create_api(modifyconfig,Key=key,Value=value,Comment=comment,NameSpace=namespace)
        return res_result.json()