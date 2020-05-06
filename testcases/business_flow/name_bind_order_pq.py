#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.comm_func.namelist import NameList
from common.lib.pip_install import unittest
from common.lib.venv.var import send_boss_user
from common.lib.module_tools.analyze_result import get_api_result



class NameBindOrderFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.namemanage = NameList()
        cls.namemanage.login(send_boss_user)
    def test_name_bind_order(self):
        """名单绑订单"""
        # 定义企业列表
        entborrows = ['淳华工种1','郑鹏工种1','复扬工种1','建大工种1','明基工种1']
        # 在企业列表循环
        for entborrow in entborrows:
            # 根据企业查询名单
            get_name_res = self.namemanage.get_nameList(ScannerMobile=send_boss_user,SpEntName=entborrow,
                                                        ScannerUserID=self.namemanage.zt_guid, RecordSize=1000)
            # 解析查询结果获取姓名列表和id列表
            names = get_api_result(get_name_res, 'Name')
            nameids = get_api_result(get_name_res, 'NameID')
            # 根据姓名获取待绑定的订单id
            self.namemanage.get_waitbindorder_pq(names=names)
            # 名单绑定订单
            self.namemanage.bind_order(orderid=self.namemanage.wait_bind_orderids[0],NameIdList=nameids)


if __name__=='__main__':
    unittest.main()