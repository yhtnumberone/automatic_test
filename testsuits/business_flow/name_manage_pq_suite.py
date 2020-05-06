#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# 获取根路径
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("automatic_test")+len("automatic_test")]
# 将根目录加入path
import sys
sys.path.append(rootPath)

from common.lib.pip_install import unittest
from testcases.business_flow.name_manage_pq import NameManage
from common.lib.pip_install.BeautifulReport import BeautifulReport
from common.lib.venv.var import report_name,report_path


test1 = [NameManage('test_add_name_flow')]
suite = unittest.TestSuite()
suite.addTests(test1)
BeautifulReport(suite).report(filename=report_name, description='名单流程', log_path=report_path)
