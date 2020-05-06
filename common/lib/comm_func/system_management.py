#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : mem_information_manag_func.py
# @Author   : qiuhaojian
# @Date     : 2020/03/09
# @Desc     : 系统管理模块公共方法



from common.lib.login.web_login import *
from common.lib.login.applet_login import *
import pprint

class Sys_Manage_Func(Web_Login):
    #获取配置项状态方法
    def get_config_staus(self,keyname):
        res=self.create_api(Get_All_Config)
        keylist=res.json()['Data']['RecordList']
        pprint.pprint(keylist)
        keystatus=None
        for one in keylist:
            if one['Key']==keyname:
                keystatus=one['Value']

        if keystatus==None:
            raise Exception('未获取到keyvalue值')
        return keystatus
    #修改配置状态方法
    def update_config_staus(self,keyname,keyvalue,namespace='tech.user-info'):
        res=self.create_api(Modify_Config,
                            Key=keyname,
                            Value=keyvalue,
                            Comment='',
                            NameSpace=namespace)
        respone=res.json()
        return respone


