#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.pip_install import unittest
from common.lib.comm_func.namelist import NameList
from common.lib.venv.var import send_boss_user,agentName,nowtime
from common.lib.module_tools.analyze_result import get_api_result
from common.lib.comm_func.group_management import GroupManagement
from common.lib.database.mysql_db import OperateMDdb


class NameManage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 初始化名单对象
        cls.namemanage = NameList()
        cls.namemanage.login(send_boss_user)
        # 初始化集团管理对象
        cls.groupmanage = GroupManagement()
        cls.groupmanage.login(send_boss_user)


    def test_add_name_flow(self):
        """
        1、创建150个无来源的名单
        2、对步骤1创建的名单设置来源
        3、创建50个有来源的名单
        """
        entborrows = ['淳华工种1','郑鹏工种1','复扬工种1','建大工种1','明基工种1']
        # 录名单时不带来源
        for entborrowname in entborrows:
            for i in range(30):
                self.namemanage.add_name_pq(entbrorrowname=entborrowname)
        # 查询录入的名单
        res = self.namemanage.get_nameList(ScannerMobile=send_boss_user, ScannerUserID=self.namemanage.zt_guid,RecordSize=1000)
        # 断言-检查名单数量
        count = res['Data']['RecordCount']
        self.assertEqual(count,150)
        # 断言-检查名单企业
        entborrowlist = get_api_result(res,'SpEntName')
        entborrowlist = list(set(entborrowlist))  # 去重
        self.assertEqual(sorted(entborrows),sorted(entborrowlist))
        # 断言-检查名单标准企业
        entids = []
        for entborrowname in entborrows:
            res_getentborrow = self.groupmanage.getEntBorrowList(BEntName=entborrowname)
            entid = get_api_result(res_getentborrow,'EntId')[0]
            entids.append(entid)
        entidlist = get_api_result(res,'EntId')
        entidlist = list(set(entidlist))
        self.assertEqual(sorted(entidlist),sorted(entids))
        # 断言-检查来源
        for name in res['Data']['RecordList']:
            agentname = name['FromSpName']
            agentid = name['FromSpID']
            self.assertEqual(agentname,'')
            self.assertEqual(agentid,0)
        # 断言-检查数据库落表数量
        selectdb = OperateMDdb()
        sql = f"""SELECT count(*) FROM name_list WHERE intv_dt = '2020-04-25' and scanner_id = {self.namemanage.zt_guid} and tenant_id = '{self.namemanage.zt_tid}'"""
        sqlcount = selectdb.selectsql(sql)[0][0]
        self.assertEqual(sqlcount,count)
        # 设置来源
        NameListIds = [self.namemanage.getnameidlist[i:i + 100] for i in range(0, len(self.namemanage.getnameidlist), 100)]
        a = len(self.namemanage.getnameidlist)
        if a%100!=0:
            num = a//100+1
        else:
            num = a//100
        for i in range(num):
            self.namemanage.set_source(FromSpName=agentName,NameListIds=NameListIds[i])
        # 查询名单，重新获取数据
        res = self.namemanage.get_nameList(ScannerMobile=send_boss_user, ScannerUserID=self.namemanage.zt_guid,RecordSize=1000)
        # 断言-检查来源
        result = self.groupmanage.getcooplist(NickName= agentName)
        agentID = get_api_result(result,'ZtVspId')[0]
        for name in res['Data']['RecordList']:
            agentname = name['FromSpName']
            agentid = name['FromSpID']
            self.assertEqual(agentname,agentName)
            self.assertEqual(agentid,agentID)
        # 录名单时带来源
        for entborrowname in entborrows:
            for i in range(10):
                self.namemanage.add_name_pq(entbrorrowname=entborrowname,FromSpName=agentName)
        # 查询录入的名单
        res = self.namemanage.get_nameList(ScannerMobile=send_boss_user, ScannerUserID=self.namemanage.zt_guid,RecordSize=1000)
        # 断言-检查名单数量
        count = res['Data']['RecordCount']
        self.assertEqual(count,200)
        # 断言-检查落表数据量
        sql = f"""SELECT count(*) FROM name_list WHERE intv_dt = '2020-04-25' and scanner_id = {self.namemanage.zt_guid} and tenant_id = '{self.namemanage.zt_tid}'"""
        sqlcount = selectdb.selectsql(sql)[0][0]
        self.assertEqual(sqlcount,count)
        # 断言-检查来源
        for name in res['Data']['RecordList']:
            agentname = name['FromSpName']
            agentid = name['FromSpID']
            self.assertEqual(agentname,agentName)
            self.assertEqual(agentid,agentID)


if __name__=='__main__':
    unittest.main()