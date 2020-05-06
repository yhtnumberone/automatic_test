#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import random

# <editor-fold desc="""公用变量""">
"""公用变量"""
# PATH
base_path = os.getcwd()
case_path = '/testcase/'
file_path = '/common/test_file/'
log_path = '/result/log/'
report_path = '/result/report/'

# 测试账号
zaoruzhi= '17897897897'
zhouyu = '18716546132'
broker_user = "13330000001" # 招聘端测试账号
shop_manager_user = '13330000002'
Recruit_boss_user = '13330000003'
send_boss_user = '13340000001' # 派遣端测试账号--老板角色
factorier = '13360000001' # 派遣端测试账号--普通驻厂角色
phonenum1 = "15995627659" #

phonenum = broker_user

# 基础来源去向定义
agentName = '自动化测试供应商'

#文件命名规则
namerule = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

# 获取当前路径
curPath = os.path.abspath(os.path.dirname(__file__))
# 获取根路径
rootPath = curPath[:curPath.find("automatic_test")+len("automatic_test")]


# 阿里云相关变量
# bucketname
bucketname = 'woda-app-private-test'
# region
region = 'http://oss-cn-shanghai.aliyuncs.com'
# 代垫发上传后的文件名
myObjectName_sendmoney = 'dajiaying/web/sendMoneyImport' + namerule + str(random.randint(1000, 9999))
# 代垫发上传的本地文件名
myLocalFile_sendmoney = os.path.abspath(rootPath) + file_path + 'sendMoneyImporttemplate.xlsx'
# 可预支导入后文件名
myObjectName_advance = 'dajiaying/web/weeklyWageManager/import/' + namerule + str(random.randint(1000, 9999))
# 可预支导入本地文件名
myLocalFile_advance = os.path.abspath(rootPath) + file_path + 'advanceimport.xlsx'
# 月薪导入本地文件名
myLocalFile_month = os.path.abspath(rootPath) + file_path + 'monthimport.xlsx'
# 月薪倒入后文件名
myObjectName_month = 'dajiaying/web/monthlyWageManager/import/' + namerule + str(random.randint(1000, 9999))

# 测试报告路径
report_path = os.path.abspath(rootPath) + report_path
report_name = '测试报告'+namerule + '.html'

# 日志路径
log_name = os.path.abspath(rootPath) + log_path +'测试日志'+ namerule + '.log'
# </editor-fold>


# <editor-fold desc="名单相关变量">
# 面试日期
nowtime = datetime.datetime.now().strftime('%Y-%m-%d')
time0201 = '2020-02-01'

#小程序相关变量
# IdCardFile = os.path.abspath(os.path.join(os.getcwd(), "..")) + file_path + 'idcard.jpg'
IdCardFile = rootPath + file_path + 'idcard.jpg'
# bankCardFile = os.path.abspath(os.path.join(os.getcwd(), "..")) + file_path + 'bankcard.jpg'
bankCardFile = rootPath + file_path + 'bankcard.jpg'
# workCardFile = os.path.abspath(os.path.join(os.getcwd(), "..")) + file_path + 'workcard.jpg'
workCardFile = rootPath + file_path + 'workcard.jpg'
# </editor-fold>
