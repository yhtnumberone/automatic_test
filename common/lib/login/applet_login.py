#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : applet_login.py
# @Author   : qiuhaojian
# @Date     : 2020/02/23
# @Desc     : 公共方法


from common.lib.login.login_basic import *
from common.lib.module_tools.set_config import Set_Section
import pprint

# 获取appkey
getenv = Set_Section(section_name='environment',filename='test_env_conf')
app_key = getenv.read_section('applet_appkey')
# 获取测试环境
environment = getenv.read_section('env')
# 获取appid
appid = getenv.read_section('applet_appid')

class Applet_Login():
#小程序登录
    def applogin(self,phone=None):
        if environment=='sit' or environment=='alpha':
            #获取验证码
            result = djy_get_vcode(phone,appid,app_key)
            pprint.pprint(result)
            vcode = result
            result = applet_login(phone, vcode,appid,app_key)
            self.Guid = result['Data']['user_id']
            self.Name = result['Data']['member_name']
            # self.TId = result['Data']['zt_tid']
            self.access_token = result['Data']['access_token']
            self.client_id = result['Data']['client_id']
            self.client_secret = result['Data']['client_secret']
            self.expires_in = result['Data']['expires_in']
            self.refresh_token = result['Data']['refresh_token']
            self.zt_token = result['Data']['zt_access_token']
            self.uuid = result['Data']['uuid']
        else:
            loginfo = Set_Section(filename='login_info',section_name='applet_login_info')
            self.Guid = loginfo.read_section('user_id')
            self.Name = loginfo.read_section('member_name')
            self.access_token = loginfo.read_section('access_token')
            self.client_secret = loginfo.read_section('client_secret')
            self.expires_in = loginfo.read_section('expires_in')
            self.refresh_token = loginfo.read_section('refresh_token')
            self.zt_token = loginfo.read_section('zt_token')
            self.uuid = loginfo.read_section('uuid')

    def create_api(self,url, **kwargs):
        """
        构造接口的函数
        :param url:
        :param kwargs:
        :return:
        """
        #构建data参数
        kwargs = {key: value for key, value in kwargs.items() if value is not None}
        data = str(kwargs).replace('\'', '\"')
        # 构建body参数

        api_name = url.split("/")[-1]
        # if api_name == 'GetTenantEntListByName':
        #     req_body = body(data, guid=self.Guid, token=self.zt_token,app_id='1000006')
        # else:
        req_body = body(data, guid=self.Guid, token=self.zt_token, app_key='JFFApp',app_id='1000006')

        logger.info(f'接口{api_name}请求body：{req_body}')

        result = requests.post(url=url, json=req_body, verify=False)
        logger.info(f'接口{api_name} 返回参数：{result.json()}')
        return result


