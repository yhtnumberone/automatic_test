#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : send_money_import.py
# @Author   : yht
# @Date     : 2019/12/24
# @Desc     : 测试导入发款单场景




from common.lib.comm_func.common_function import Invoke_Api
import unittest
from common.lib.database.mysql_db import OperateMDdb
from common.lib.venv.var import *
import oss2
from common.lib.comm_func.common_function import get_api_result
import time

class SendMoneyImport(unittest.TestCase):
    def setUp(self) -> None:
        self.invoke_api_ = Invoke_Api('15000000000')

    def test_get_entlist(self):
        """
        测试查询条件：标准企业下拉列表
        """
        # 获取接口返回结果
        res_result = self.invoke_api_.invoke_api(url=get_pay_salary_entList_api, CoopSts=1, RecordIndex=0, RecordSize=10)
        # 断言--检查status_code
        self.assertEqual(res_result.status_code, 200)
        # 查询数据库对应数据
        # sql_result = OperateMDdb().selectsql('t_ent_id', 'ent_id', 'ent_full_name', table='tenant_ent',
        #                                      condition='where tenant_id =' + TId)

        # sql_count = OperateMDdb().selectsql('count(*)', table='tenant_ent', condition='where tenant_id =' + TId)
        # 获取接口返回特定数据
        api_result = get_api_result(res_result, ' ', 'EntId', 'EntName')
        api_coun = res_result.json()['Data']['RecordCount']
        # 断言--实际结果与预期结果比较
        # self.assertEqual((sql_result, int(sql_count[0])), (api_result, api_coun))
        # 获取entid用于其他用例
        api_result = get_api_result(res_result, 'EntId')
        self.entid = api_result[0]
        return self.entid

    def test_get_excel_import(self):
        """
        测试基本功能：上传发款单到阿里云
        :return:
        """
        # 调用接口
        res_result = self.invoke_api_.invoke_api(url=wd_ali_getalists_api)
        # 获取参数
        api_resuil = get_api_result(res_result)
        # 定义变量
        AccessKeyId = api_resuil['AccessKeyId']
        AccessKeySecret = api_resuil['AccessKeySecret']
        SecurityToken = api_resuil['SecurityToken']
        # 上传excel到阿里云
        auth = oss2.StsAuth(AccessKeyId, AccessKeySecret, SecurityToken)
        bucket = oss2.Bucket(auth, region, bucketname)
        bucket.put_object_from_file(myObjectName, myLocalFile)
        print('myLocalFile',myLocalFile)
        # 断言--检查status_code
        self.assertEqual(res_result.status_code, 200)

    def test_preview_import_success(self):
        """
        测试基本功能：成功导入发款单
        :return:
        """
        entid = int(SendMoneyImport.test_get_entlist(self))
        # 获取预览令牌
        res_result = self.invoke_api_.invoke_api(url=get_preview_token_api, ali_bucket=bucketname, ali_object=myObjectName, sheet='sheet1',
                               ent_id=entid,
                               settle_start_dt='2019-12-01', settle_end_dt='2019-12-31', salary_typ=1,
                               ali_object_md5='2019-12-31')
        time.sleep(2)
        preview_token = res_result.json()['Data']['preview_token']
        # 断言--检查status_code
        self.assertEqual(res_result.status_code, 200)

        # 获取预览统计
        # 接口GetPreviewStats
        for i in range(20):
            res_result = self.invoke_api_.invoke_api(url=get_preview_stats_api, prev_token=preview_token)
            if res_result.json()['Desc'] == '成功':
                break
        # 断言--检查status_code
        self.assertEqual(res_result.status_code, 200)
        # #获取预览结果
        # # 接口GetPreviewResult
        res_result = self.invoke_api_.invoke_api(url=get_preview_result_api, prev_token=preview_token, record_index=0, record_size=10)
        api_count = res_result.json()['Data']['record_cnt']
        payment_import_id = OperateMDdb().selectsql('payment_import_id', table='payment_import',
                                                    condition='order by payment_import_id desc limit 1')[0]
        sql_count = OperateMDdb().selectsql('count(*)', table='payment_import_detail',
                                            condition='where payment_import_id = ' + payment_import_id)
        # 断言--检查status_code
        self.assertEqual(res_result.status_code, 200)
        # 断言--检查导入预览数量
        self.assertEqual(api_count, int(sql_count[0]))
        # 提交预览结果
        res_result = self.invoke_api_.invoke_api(url=preview_result_commit_api, prev_token=preview_token)
        # 断言--检查status_code
        self.assertEqual(res_result.status_code, 200)
        # 断言--检查Desc
        self.assertEqual(res_result.json()['Desc'], '成功')

    def test_preview_import_empty(self):
        """
        测试异常场景：参数为空导入发款单
        :return:
        """
        entid = int(SendMoneyImport.test_get_entlist(self))
        # 测试参数全空导入发款单
        # 获取预览令牌
        res_result = self.invoke_api_.invoke_api(url=get_preview_token_api, ali_bucket='', ali_object='',
                                sheet='',
                                ent_id=0,
                                settle_start_dt='', settle_end_dt='', salary_typ=1,
                                ali_object_md5='')
        # 检查预期结果
        self.assertEqual(res_result.json()['Desc'],'输入参数错误')
        self.assertEqual(res_result.status_code,200)
        self.assertEqual(res_result.json()['Code'],50001)

        # 测试参数ali_bucket为空值
        res_result = self.invoke_api_.invoke_api(url=get_preview_token_api, ali_bucket='', ali_object=myObjectName, sheet='sheet1',
                               ent_id=entid,
                               settle_start_dt='2019-12-01', settle_end_dt='2019-12-31', salary_typ=1,
                               ali_object_md5='2019-12-31')
        # 检查预期结果
        self.assertEqual(res_result.json()['Desc'],'输入参数错误')
        self.assertEqual(res_result.status_code,200)
        self.assertEqual(res_result.json()['Code'],50001)

        #测试参数ali_object为空值
        res_result = self.invoke_api_.invoke_api(url=get_preview_token_api, ali_bucket=bucketname, ali_object='', sheet='sheet1',
                               ent_id=entid,
                               settle_start_dt='2019-12-01', settle_end_dt='2019-12-31', salary_typ=1,
                               ali_object_md5='2019-12-31')
        # 检查预期结果
        self.assertEqual(res_result.json()['Desc'],'输入参数错误')
        self.assertEqual(res_result.status_code,200)
        self.assertEqual(res_result.json()['Code'],50001)

        # 测试sheet参数为空值
        res_result = self.invoke_api_.invoke_api(url=get_preview_token_api, ali_bucket=bucketname, ali_object=myObjectName, sheet='',
                               ent_id=entid,
                               settle_start_dt='2019-12-01', settle_end_dt='2019-12-31', salary_typ=1,
                               ali_object_md5='2019-12-31')

        print('res_result:',res_result.json())
    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
