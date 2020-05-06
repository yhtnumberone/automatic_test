#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : month_management.py
# @Author   : sam
# @Date     : 2020/03/30
# @Desc     : 月薪方法


from common.lib.login.web_login import Web_Login
from common.lib.module_tools.edit_excel import edit_exctwo
from common.lib.module_tools.aliyun_import import AlImport
from common.lib.venv.var import *
from common.lib.venv.api_path import *
import time


class MonthManage(Web_Login):
    # 月薪管理
    def get_agent(self, agentname):
        """
        获取来源id
        :param agentname: 来源名称
        :return: self.agentid 来源id
        """
        req = self.create_api(get_agent, CoopSts=1, RecordIndex=0, RecordSize=9999)
        agentlist = req.json()['Data']['RecordList']
        self.agentid = None
        for i in range(len(agentlist)):
            if agentname == agentlist[i]['LaborName']:
                self.agentid = agentlist[i]['SpId']
        return self.agentid

    def get_ent(self, entname):
        """
        获取标准企业id
        :param entname: 标准企业名称
        :return: self.entid 标准企业id
        """
        print(entname)
        req = self.create_api(GetPaySalaryEntList_Api, CoopSts=1, RecordIndex=0, RecordSize=9999)
        print(req.json())
        entlist = req.json()['Data']['RecordList']
        for i in range(len(entlist)):
            try:
                if entname == entlist[i]['EntShortName']:
                    self.entid = entlist[i]['EntId']
                    print(type(self.entid))
            except Exception as e:
                print(e, '未找到标准企业', entname)
        return self.entid

    def month_import(self,
                       entname,
                       monthdate,
                       name,
                       idcadnum,
                       workcard,
                       realpay,
                       workdate,
                       workhour,
                       workstatus='在职',
                       salarytype=1):
        """
        # 月薪导入
        :param entname: 标准企业名称 必填
        :param monthdate: 所属月份，必填
        :param salarytype: 月薪导入类型，必填
        :param name: 会员名称，必填
        :param idcadnum: 会员身份证号码，必填
        :param workcard: 会员工牌，必填
        :param realpay: 实发工资，必填
        :param workdate: 会员入职日期，必填
        :param workstatus: 会员在职状态，选填，默认在职
        :param workhour: 出勤小时数，必填
        :return:
        """

        self.monthdate = monthdate
        # self.phone = send_user
        # 编辑可预支导入模板
        edit_exctwo(t1=name, t2=idcadnum, t3=workcard, t4=realpay, t5=workdate, t6=workstatus, t9=workhour)
        # 将目标导入阿里云
        alimport = AlImport()
        alimport.login(self.login_phone)
        alimport.ali_import(myLocalFile=myLocalFile_month, myObjectName=myObjectName_month)
        # 获取标准企业id
        self.get_ent(entname=entname)
        # 导入预览
        req = self.create_api(MonthBillGen_ImportCheck, SheetName='Sheet1', BucketKey=bucketname,
                              EnterpriseID=self.entid,
                              FileName=myObjectName_month, Month=monthdate,
                              SalaryType=1)

        try:
            BizID = req.json()['Data']['BizID']
            # 等待预览加载完毕
            for i in range(5):
                req = self.create_api(MonthBillGen_GetImportCheckResult, BizID=BizID, EnterpriseID=self.entid)
                time.sleep(1)
                if req.json()['Data']['State'] == 2:
                    break
            # 提交保存
            # 请求数据
            req = self.create_api( MonthBillGen_GenerateBatchByBizID,
                                  ImportBizID=BizID,
                                  AgentID = get_agent('奇迹招聘'),
                                  EnterpriseID=self.entid,
                                  FileMd5='',
                                  FileName=myObjectName_month,
                                  OPType=1,
                                  Month=self.monthdate,
                                  SalaryType=salarytype,
                                  GeneratePayroll=2,
                                  BucketKey=bucketname)
            bizid = req.json()['Data']['BizID']
            print(bizid)
            # 等待保存完毕
            for i in range(5):
                req = self.create_api(MonthBillGen_GetGenerateBatchResult, BizID=bizid, EnterpriseID=self.entid)
                time.sleep(1)
                if req.json()['Data']['State'] == 2:
                    break
        except Exception as e:
            # 导入预览失败，打印失败信息
            print(e, req.json())


    def select_monthbill(self, agentname=None, monthdate=None, BillAudit=1, Entname=None, Operator=None):
        """
        # 查询月薪账单
        :param agentname: 来源名称，可选，默认None
        :param monthdate: 所属月份，可选，默认None
        :param EndDt:预支周期结束日期，可选，默认None
        :param BillAudit:账单审核状态，可选，默认1：待审核，2已审核，3审核不通过
        :param Entname: 标准企业名称，可选，默认None
        :param Operator:
        :return:
        """

        if monthdate is None:
            monthdate = self.monthdate

        if Entname is not None:
            self.get_ent(Entname)
            EntId = self.entid
        else:
            EntId = None

        if Operator is None:
            Operator = self.Name

        if agentname is None:
            SrceSpId = -9999
        else:
            SrceSpId = self.get_agent(agentname)

        req = self.create_api(MonthBill_select,
                              BillRelatedMoStart='',
                              BillRelatedMoEnd='',
                              BillMonthlyBatchId=-9999,
                              EntId=-9999,
                              TrgtSpId=-9999,
                              TrgtSpAuditSts=-9999,
                              BillSrce=-9999,
                              SalaryTyp=-9999,
                              SalaryPayer=-9999,
                              Operator='',
                              RecordIndex=0,
                              RecordSize=10)
        print(req)
        print(req.json())
        self.billid = req.json()['Data']['RecordList'][0]['BillMonthlyBatchId']
        return self.billid



    def audit_monthbill(self, agentname, status=1):
        """
        审核月薪订单
        :param agentname: 来源名称，必填
        :param status: 审核状态，可选，默认 1：审核通过，2：审核不通过
        :return:
        """
        req = {}
        billid = self.select_monthbill(agentname=agentname)
        if status == 1:
            req = self.create_api(MonthBill_Confirm, BillMonthlyBatchId=billid)
        elif status == 2:
            req = self.create_api(MonthBill_Confirm, BillMonthlyBatchId=billid)
        result = req.json()['Desc']
        return result

