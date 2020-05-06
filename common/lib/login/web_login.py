#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : web_login.py
# @Author   : qiuhaojian
# @Date     : 2020/02/23
# @Desc     : 公共方法


from common.lib.login.login_basic import labor_weblogin,body
from common.lib.module_tools.LogHandler import logger
from common.lib.module_tools.set_config import Set_Section
from common.lib.pip_install import requests

# 获取appkey
getenv = Set_Section(section_name='environment',filename='test_env_conf')
app_key = getenv.read_section('web_appkey')
# 获取测试环境
environment = getenv.read_section('env')

class Web_Login():
    # 登录web端
    def login(self, phone=None):
        if environment =='sit' or environment == 'alpha':
            # 登录获取返回结果
            result = labor_weblogin(phone,app_key)
            self.Guid = result['Guid']
            self.Name = result['Name']
            self.zt_tid = result['zt_tid']
            self.access_token = result['access_token']
            self.client_id = result['client_id']
            self.client_secret = result['client_secret']
            self.expires_in = result['expires_in']
            self.refresh_token = result['refresh_token']
            self.zt_token = result['zt_access_token']
            self.zt_guid = result['zt_guid']
            self.login_phone = phone
            return result
        else:
            loginfo = Set_Section(section_name='login_info',filename='web_login_info')
            self.Guid = loginfo.read_section('Guid')
            self.Name = loginfo.read_section('Name')
            self.zt_tid = loginfo.read_section('zt_tid')
            self.access_token = loginfo.read_section('access_token')
            self.zt_token = loginfo.read_section('zt_token')
            self.zt_guid = loginfo.read_section('zt_guid')
            self.login_phone = phone
            return

    def create_api(self, url, **kwargs):
        """
        构造接口的函数
        :param url:
        :param kwargs:
        :return:
        """
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        data = str(kwargs).replace('\'', '\"')
        # 如果接口地址包含fw则为中台接口，token使用中台token
        req_body = body(data, guid=self.Guid, token=self.access_token,app_key=app_key)
        if '/fw/' in url:
            req_body = body(data, app_id=self.zt_tid, guid=self.zt_guid, token=self.zt_token, app_key=app_key)
        api_name = url.split("/")[-1]
        logger.info(f'接口{api_name}请求body：{req_body}')
        result = requests.post(url=url, json=req_body, verify=False)
        if result.json()['Code'] in [50001]:
            logger.error(f'接口{api_name} 返回参数：{result.json()}')
        else:
            logger.info(f'接口{api_name} 返回参数：{result.json()}')
        return result
