#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.login.web_login import Web_Login
from common.lib.module_tools.edit_excel import edit_exc
from common.lib.module_tools.aliyun_import import AlImport
from common.lib.venv.var import *
from common.lib.venv.api_path import *
import time


class AdvanceManage(Web_Login):
    # 可预支管理
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

    def advance_import(self, entname, SettleBeginDate, name, SettleEndDate, idcadnum, workcard, workdate,
                       workstatus='在职', workday=6):
        """
        # 可预支导入
        :param entname: 标准企业名称 必填
        :param SettleBeginDate: 预支周期开始日期，必填
        :param name:会员名称，必填
        :param SettleEndDate:预支周期结束日期，必填
        :param idcadnum:会员身份证号码，必填
        :param workcard:会员工牌，必填
        :param workdate:会员入职日期，必填
        :param workstatus:会员在职状态，选填，默认在职
        :param workday:上班天数，选填，默认6天
        :return:
        """

        self.SettleBeginDate = SettleBeginDate
        self.SettleEndDate = SettleEndDate
        # 编辑可预支导入模板
        edit_exc(t1=name, t2=idcadnum, t3=workcard, t4=workdate, t5=workstatus, t7=workday, )
        # 将目标导入阿里云
        alimport = AlImport()
        alimport.login(self.login_phone)
        alimport.ali_import(myLocalFile=myLocalFile_advance, myObjectName=myObjectName_advance)
        # 获取标准企业id
        self.get_ent(entname=entname)
        # 导入预览
        req = self.create_api(url=WeekBillGen_ImportCheck, SheetName='Sheet1', BucketKey=bucketname,
                              EnterpriseID=self.entid,
                              FileName=myObjectName_advance, SettleBeginDate=SettleBeginDate,
                              SettleEndDate=SettleEndDate)

        try:
            BizID = req.json()['Data']['BizID']
            # 等待预览加载完毕
            for i in range(5):
                req = self.create_api(WeekBillGen_GetImportCheckResult, BizID=BizID, EnterpriseID=self.entid)
                time.sleep(1)
                if req.json()['Data']['State'] == 2:
                    break
            # 提交保存
            req = self.create_api(WeekBillGen_GenerateBatchByBizID, ImportBizID=BizID, EnterpriseID=self.entid)
            bizid = req.json()['Data']['BizID']
            print(bizid)
            # 等待保存完毕
            for i in range(5):
                req = self.create_api(WeekBillGen_GetGenerateBatchResult, BizID=bizid, EnterpriseID=self.entid)
                time.sleep(1)
                if req.json()['Data']['State'] == 2:
                    break
        except Exception as e:
            # 导入预览失败，打印失败信息
            print(e,req.json())




    def select_weekbill(self, agentname=None, BeginDt=None, EndDt=None, BillAudit=1, Entname=None, Operator=None):
        """
        # 查询可预支账单
        :param agentname: 来源名称，可选，默认None
        :param BeginDt:预支周期开始日期，可选，默认None
        :param EndDt:预支周期结束日期，可选，默认None
        :param BillAudit:账单审核状态，可选，默认1：待审核，2已审核，3审核不通过
        :param Entname:
        :param Operator:
        :return:
        """
        if BeginDt is None or EndDt is None:
            BeginDt = self.SettleBeginDate
            EndDt = self.SettleEndDate

        if Entname is not None:
            self.get_ent(Entname)
            EntId = self.entid
        else:
            EntId = -9999

        if Operator is None:
            Operator = self.Name

        if agentname is None:
            SrceSpId = -9999
        else:
            SrceSpId = self.get_agent(agentname)

        req = self.create_api(WeekBill_Select, BeginDt=BeginDt, EndDt=EndDt, BillWeeklyBatchId=-9999, EntId=EntId,
                              SrceSpId=SrceSpId, BillAudit=BillAudit, BillSrce=-9999, Operator=Operator, TrgtSpId=-9999,
                              RecordIndex=0, RecordSize=10)
        print(req)
        print(req.json())
        self.billid = req.json()['Data']['RecordList'][0]['BillWeeklyBatchId']
        return self.billid

    def audit_weekbill(self, agentname, status=1):
        """
        审核可预支订单
        :param agentname: 来源名称，必填
        :param status: 审核状态，可选，默认 1：审核通过，2：审核不通过
        :return:
        """
        req = {}
        billid = self.select_weekbill(agentname=agentname)
        if status == 1:
            req = self.create_api(WeekBill_Confirm, BillWeeklyBatchId=billid)
        elif status == 2:
            req = self.create_api(WeekBill_UnConfirm, BillWeeklyBatchId=billid)
        result = req.json()['Desc']
        return result


