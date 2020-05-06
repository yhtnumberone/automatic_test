#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : test_real_record.py
# @Author   : yht
# @Date     : 2020-02-11
# @Desc     : 测试实接记录

# from common.lib.api import *
# import unittest
from common.lib.pip_install import unittest
from common.lib.database.mysql_db import OperateMDdb
from common.lib.venv.var import *
from common.lib.comm_func.namelist import NameList
from common.lib.module_tools.analyze_result import get_api_result
from common.lib.venv.api_path import get_vagent
from common.lib.module_tools.LogHandler import logger


class RealrecordPq(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # 创建调用接口对象，初始化测试账号
        cls.suite = NameList()
        cls.suite.login(send_boss_user)
        # 连接数据库
        cls.zt_db = OperateMDdb()

    def test_record_manually(self):
        """手工录入"""
        # 调用接口手工录取名单
        self.suite.add_name_pq(entbrorrowname='中达自动化测试预支工种', FromSpName='奇迹招聘')

        # 断言-检查接口返回值
        self.assertEqual(self.suite.status_code, 200, f'调用接口失败,状态码为{self.suite.status_code}')
        self.assertEqual(self.suite.code, 0, f'接口返回code错误，实际返回{self.suite.code}')
        self.assertEqual(self.suite.desc, '成功', f'接口返回desc错误，实际返回{self.suite.desc}')
        self.assertEqual(self.suite.res_guid, 0, f'接口返回guid错误，实际返回{self.suite.res_guid}')
        self.assertEqual(self.suite.res_rcrttype, 2, f'接口返回rcrttype错误，实际返回{self.suite.res_rcrttype}')
        self.assertEqual(self.suite.res_uuid, 0, f'接口返回uuid错误，实际返回{self.suite.res_uuid}')
        # 断言-检查创建接口返回nameid和查询接口查询的nameid是否一致
        self.suite.get_nameList(name=self.suite.newname_pq, idcardnum=self.suite.newidnum_pq)
        self.assertEqual(self.suite.newnameid_pq, self.suite.getnameidlist[0], '新增名单接口返回的id和查询列表返回的id不一致')
        # 断言-检查查询名单接口返回的手机号码、身份证、姓名和录名单时一致
        self.assertEqual(self.suite.newmobile_pq, self.suite.getMobilelist[0], '手机号码不一致')
        self.assertEqual(self.suite.newidnum_pq, self.suite.getidcardlist[0], '身份证不一致')
        self.assertEqual(self.suite.newname_pq, self.suite.getrealnamelist[0], '姓名不一致')
        # 断言-检查数据落表
        sql = f'select * from name_list where name_list_id = {self.suite.newnameid_pq}'
        results = self.zt_db.selectsql(sql)
        self.assertNotEqual(results, (), msg='查询结果为空')
        self.assertIn(self.suite.newmobile_pq, results[0])
        self.assertIn(self.suite.newidnum_pq, results[0])
        self.assertIn(self.suite.newname_pq, results[0])

    def test_set_who_give_me(self):
        """设置来源"""
        # 调用接口设置来源
        req = self.suite.set_source(FromSpName='自动化测试供应商')
        isok = req['Data']['ResultList'][0]['IsOk']
        # 断言-检查isok字段
        self.assertEqual(isok, 1)
        # 断言-检查该名单绑单状况
        results = self.suite.get_nameList(name=self.suite.newname_pq)
        agent = get_api_result(results, 'FromSpName')
        agentid1 = get_api_result(results, 'FromSpID')
        self.suite.get_source(get_vagent, FromSpName='自动化测试供应商')
        agentid2 = self.suite.FromSpID
        self.assertEqual(agent[0], '自动化测试供应商')
        self.assertEqual(agentid1[0], agentid2)
        # 断言-检查数据落表
        sql = f'select srce_tenant_coop_id,srce_sp_short_name from name_list where name_list_id={self.suite.newnameid_pq}'
        res = self.zt_db.selectsql(sql)
        agentid = res[0][0]
        agentname = res[0][1]
        self.assertEqual(agentid, agentid2)
        self.assertEqual(agentname, '自动化测试供应商')

    def test_set_intsts(self):
        """设置面试状态"""
        # 调用接口，设置面试状态为面试通过
        res = self.suite.set_interview_state(IntvSts=2)
        # 断言-检查接口返回
        status = self.suite.status_code
        code = res['Code']
        desc = res['Desc']
        succcount = res['Data']['SuccCount']
        self.assertEqual(status, 200)
        self.assertEqual(code, 0)
        self.assertEqual(desc, '成功')
        self.assertEqual(succcount, 1)
        # 断言，查询名单检查接口面试状态
        res = self.suite.get_nameList(name=self.suite.newname_pq)
        intsts = get_api_result(res, 'InterviewStatus')
        self.assertEqual(intsts[0], 2)
        # 断言，检查数据落表
        sql = f'select intv_sts from name_list where name_list_id = {self.suite.newnameid_pq}'
        results = self.zt_db.selectsql(sql)
        intsts = results[0][0]
        self.assertEqual(intsts, 2)

    def test_get_namelist(self):
        """测试查询"""
        # 调用接口手工录取名单
        self.suite.add_name_pq(entbrorrowname='中达自动化测试预支工种', FromSpName='奇迹招聘')
        # 断言-全量查询当日数据
        res = self.suite.get_nameList()
        nameidlist = get_api_result(res, 'NameID')
        lenth = len(nameidlist)
        count = res['Data']['RecordCount']
        self.assertIn(self.suite.newnameid_pq, nameidlist)
        self.assertGreater(lenth, 0)
        self.assertGreater(count, 0)
        sql = 'select count(*) from name_list order by '
        # 断言-使用企业查询名单
        res = self.suite.get_nameList(SpEntName='中达自动化测试预支工种')
        self.assertIn(self.suite.newnameid_pq, nameidlist)
        entnamelist = get_api_result(res, 'SpEntName')
        entidlist = get_api_result(res, 'SpEntID')
        sql = f'select sp_ent_id from sp_ent where sp_ent_name="中达自动化测试预支工种"'
        results = self.zt_db.selectsql(sql)
        for entname in entnamelist:
            self.assertEqual(entname, '中达自动化测试预支工种')
        for entid in entidlist:
            self.assertEqual(entid, results[0][0])

    @classmethod
    def tearDownClass(cls):
        cls.zt_db.close_db()
        super().tearDownClass()

if __name__ == '__main__':
    unittest.main()
    # logging.basicConfig(filename=log_name, level=logging.DEBUG)
    # # test1 = [SendMoneyImport('test_get_entlist'),SendMoneyImport('test_get_excel_import'),SendMoneyImport('test_preview_import_success'),SendMoneyImport('test_preview_import_empty')]
    # test1 = [Real_record('test_record_manually'), Real_record('test_set_who_give_me'), Real_record('test_set_intsts'), Real_record('test_get_namelist')]
    # suite = unittest.TestSuite()
    # suite.addTests(test1)
    # BeautifulReport(suite).report(filename=report_name,description='test',log_path=report_path)
