#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : standard_enterprise_management.py
# @Author   : yht
# @Date     : 2019/12/25
# @Desc     : 标准企业管理场景用例


import unittest
from common.lib.database.mysql_db import OperateMDdb
from common.lib.comm_func.common_function import get_api_result


class Tenant_Ent(unittest.TestCase):

    def setUp(self):
        # 获取ent list
        res_result = create_api(get_std_ent_infol_ist, RecordIndex=0, RecordSize=999, IsEnabled=-9999)
        self.api_result = get_api_result(res_result, 'StdEntId')

    def test_create_tenant_ent_success(self):
        #查找未创建过标准企业的entid
        ent_id = ''
        for e_id in self.api_result:
            sql_result = OperateMDdb().selectsql('*',table='tenant_ent',condition='where ent_id = {e_id}'.format(e_id=e_id))
            if not sql_result:
                ent_id = int(e_id)
                break
        # 使用未创建标准企业的entid创建标准企业
        # ent_id = Tenant_Ent.setUp()
        print('test_create_tenant_ent_success entid:',ent_id)
        res_result = create_api(add_pay_salary_ent, EntId=ent_id, TenantId=TId, PayBegin=1,
                                PayEnd=31, PayDt= 10)
        # 从数据库查询刚落入的数据
        sql = "select * from tenant_ent where ent_id={ent_id} and tenant_id={t_id}".format(ent_id=ent_id,t_id=TId)
        sql_result = OperateMDdb().selectsql(sql)
        # 断言--检查status_code
        self.assertEqual(res_result.status_code,200)
        # 断言--检查接口返回成功参数
        self.assertEqual(res_result.json()['Desc'],'成功')
        # 断言--检查是否落表成功
        self.assertTrue(sql_result)
        sql = "DELETE FROM tenant_ent where ent_id = {e_id} and tenant_id ={t_id}".format(e_id=globals()['ent_id'],t_id=TId)
        OperateMDdb().deletesql(sql)
    def test_create_tenant_ent_exit(self):
        #获取tenant ent list
        res_result = create_api(url=get_pay_salary_entList_api, CoopSts=1, RecordIndex=0, RecordSize=10)
        api_result = get_api_result(res_result, 'TEntId')
        #查找已创建过标准企业的entid
        ent_id = int(api_result[0])
        # 使用已创建标准企业的entid创建标准企业
        # ent_id = Tenant_Ent.setUp()
        print('test_create_tenant_ent_exit entid:',ent_id)
        res_result = create_api(add_pay_salary_ent, EntId=ent_id, TenantId=TId, PayBegin=1,
                                PayEnd=31, PayDt= 10)
        # 从数据库查询刚落入的数据
        # sql_result = OperateMDdb().selectsql('*',table='tenant_ent',condition='where ent_id = {ent_id}'.format(ent_id=ent_id))
        # 断言--检查status_code
        self.assertEqual(res_result.status_code,200)
        print('test_create_tenant_ent_exit res_result:',res_result.json())
        # 断言--检查接口返回成功参数
        # self.assertEqual(res_result.json()['Desc'],'记录已存在')
        # 断言--检查是否落表成功
        # self.assertFalse(sql_result)
    # @classmethod
    # def tearDown(cls):
    #     # ent_id = Tenant_Ent.setUp()
    #     print('teardown ent_id:',globals()['ent_id'])
    #     sql = "DELETE FROM tenant_ent where ent_id = {e_id} and tenant_id ={t_id}".format(e_id=globals()['ent_id'],t_id=TId)
    #     print(sql)
    #     OperateMDdb().deletesql(sql)

if __name__ == '__main__':
    unittest.main()
