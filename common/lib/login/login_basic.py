#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : login_basic.py
# @Author   : yinhaitao
# @Date     : 2020/02/23
# @Desc     : 公共方法


from common.lib.pip_install import requests
import string
import time
import hashlib
import random
from common.lib.venv.api_path import get_vcode_api,labor_pre_login_api,labor_weblogin_api,applet_Login_api
from common.lib.module_tools.LogHandler import logger
import uuid



def databuild(**kwargs):
    """
    公用的函数，构造data参数
    :param kwargs:
    :return:
    """
    data = str(kwargs).replace('\'', '\"')
    return data


def body(data: str, guid=0, app_id='1000001', app_key='DJYWeb', token='', sign='', ) -> dict:
    # 获取时间戳，先转换成整形，再转换字符串
    t = int(time.time())
    timestamp = str(t)
    # 构造nonce_str
    nonce_str = str(uuid.uuid1())
    # 通用请求头
    dic = {
        'app_id': app_id,
        'timestamp': timestamp,
        'nonce_str': nonce_str,
        'token': token,
        'sign': sign,
        'data': data
    }
    # 去除空值的键,构造新字典
    dic = {key: value for key, value in dic.items() if value}
    # 对key做字典升序排序，得到有序参数列表ascending_order_dic
    ascending_order_dic = sorted(dic.items(), key=lambda d: d[0], reverse=False)
    # 按照URL键值对的格式拼接成字符串
    list_str = ""
    for k, v in ascending_order_dic:
        list_str += k + '=' + v + '&'
    # 进行MD5运算
    m = hashlib.md5()
    m.update(list_str.encode('UTF-8'))
    strMD5 = m.hexdigest()
    # 字符串转大写，得到请求签名signature
    signature = strMD5.upper()
    # 构造body
    body = {
        'app_id': app_id,
        'guid': guid,
        'timestamp': timestamp,
        'nonce_str': nonce_str,
        'token': token,
        'app_key': app_key,
        'data': data,
        'signature': signature,
    }

    return body


def djy_get_vcode(phonenum,app_id,app_key):
    """
    大佳营模板获取验证码
    :param phonenum:
    :param url:
    :return: vcode
    """
    data = databuild(SPhone=phonenum)
    Body = body(data=data, guid=0, app_id=app_id, app_key=app_key)
    response = requests.post(url=get_vcode_api, json=Body)
    try:
        vcode = response.json()['Data']
        logger.info(f'获取到验证码：{vcode}')
        return vcode
    except Exception:
        logger.error(f'未获取到验证码，请定位,{response.json}')


def labor_pre_login(phonenum, vcode,app_key):
    """
    大佳营模板预登陆接口
    :param phonenum:
    :param vcode:
    :param url:
    :return: tenanttype
    """
    data = databuild(Mobile=phonenum, VerifyCode=vcode)
    Body = body(data=data, guid=0, app_id='1000001', app_key=app_key)
    response = requests.post(url=labor_pre_login_api, json=Body)
    try:
        tenanttype = response.json()['Data']['TenantType']
        logger.info(f'预登陆成功，tenanttype为{tenanttype}')
        return tenanttype
    except Exception:
        logger.error(f'预登陆失败，请定位，{response.json}')


def labor_weblogin(phonenum,app_key):
    """
    劳务模板登陆接口
    :param phonenum:
    :return: Data
    """
    vcode = djy_get_vcode(phonenum=phonenum, app_id='1000001', app_key=app_key)
    tenanttype = labor_pre_login(phonenum=phonenum,vcode=vcode,app_key=app_key)
    data = databuild(Mobile=phonenum, VerifyCode=vcode, tenanttype=tenanttype)
    Body = body(data=data, guid=0, app_id='1000001', app_key=app_key)
    response = requests.post(url=labor_weblogin_api, json=Body)
    try:
        Data = response.json()['Data']
        # access_token = Data['access_token']
        # zt_tid = Data['zt_tid']
        # Guid = str(Data['Guid'])
        # zt_access_token = Data['zt_access_token']
        # zt_guid = str(Data['zt_guid'])
        # set_ = Set_Section(section_name=phonenum,filename='login_info')
        # isexit = set_.is_exit()
        # if isexit:
        #     # print('jinruhun')
        #     set_.edit_section('access_token',access_token)
        #     set_.edit_section('zt_tid',zt_tid)
        #     set_.edit_section('Guid', Guid)
        #     set_.edit_section('zt_access_token', zt_access_token)
        #     set_.edit_section('zt_guid', zt_guid)
        # else:
        #     set_.add_section('access_token',access_token)
        #     set_.edit_section('zt_tid', zt_tid)
        #     set_.edit_section('Guid',Guid)
        #     set_.edit_section('zt_access_token', zt_access_token)
        #     set_.edit_section('zt_guid', zt_guid)
        logger.info(f'登陆成功，Data{Data}')
        return Data
    except Exception:
        logger.error(f'登陆失败，请定位，{response.json()}')


def jff_get_vcode(phonenum, url):
    """
    代发垫发获取验证码
    :param phonenum:
    :param url:
    :return: vcode
    """
    data = databuild(SPhone=phonenum)
    Body = body(data=data, guid=0, app_id='1000001', app_key='JFFAPP')
    response = requests.post(url=url, json=Body)
    try:
        result = response.json()
        return result
    except Exception:
        print("未获取到验证码，请定位")


def jff_logn_djylogin(phonenum, vcode, url, typ=-1, ptype=1):
    """
    代发垫发登陆
    :param phonenum:
    :param vcode:
    :param url:
    :param typ:
    :param ptype:
    :return:
    """
    data = databuild(Mobile=phonenum, VerifyCode=vcode, Type=typ, PType=ptype)
    Body = body(data=data, guid=0, app_id='1000001', app_key='JFFAPP')
    response = requests.post(url=url, json=Body)
    try:
        result = response.json()
        return result
    except Exception:
        print("登陆失败，请定位")

#小程序登录
def applet_login(phonenum,vcode,appid,appkey):
    #构建data
    data = databuild(mobile=phonenum, vcode=vcode)
    #构建body体
    Body = body(data=data, guid=0, app_id=appid, app_key=appkey)
    print(Body)
    response = requests.post(url=applet_Login_api, json=Body,verify=False)
    print(response.json())
    try:
        result = response.json()
        return result
    except Exception:
        print("登陆失败，请定位")


