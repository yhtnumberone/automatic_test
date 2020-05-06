#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.module_tools.set_config import Set_Section

# 获取接口地址前缀域名
getpath = Set_Section(section_name='environment',filename='test_env_conf')
path = getpath.read_section('path')




# </editor-fold>

# <editor-fold desc="大佳营劳务模板登陆相关接口">
# 获取验证码
get_vcode_api = path+'api/v1/VCodeManager/GetVCode'
# web预登陆
labor_pre_login_api = path+'api/v1/DJY_Login/Labor_Pre_Login'
# web登陆
labor_weblogin_api = path+'api/v1/DJY_Login/Labor_WebLogin'
#小程序登录
applet_Login_api=path+'api/v1/DJY_Login/Mbr_MiniLogin'

# </editor-fold>

# <editor-fold desc="大佳营劳务模板阿里云获取token接口">
Aliyun = 'fw/api/v1/Aliyun/'
#阿里云地址
ALI_GetAliSTS= path + Aliyun + 'WD_ALI_GetAliSTS'


# </editor-fold>

# <editor-fold desc="大佳营劳务模板DJY_Name_Manager">
DJY_Name_Manager = 'api/v1/DJY_Name_Manager/'
# 派遣端手工录名单
add_name = path + DJY_Name_Manager + 'AddNameForOpenAPI'
# 实接记录获取名单列表
get_namelist = path + DJY_Name_Manager + 'GetNameList'
# 招聘端手工录名单
add_interview = path + DJY_Name_Manager + 'AddInterview'
# 招聘端录入获取虚拟劳务列表
get_vlabor_zp = path + DJY_Name_Manager + 'GetVLaborList'
#获取实接记录列表
getnamelist = path + DJY_Name_Manager+ 'GetNameList'
#获取面试名单（商务）名单列表
Get_Business_nameList=path+DJY_Name_Manager+ 'GetBusinessInterviewList'
# 派遣端名单设置来源
SetSpForOpenAPI = path+DJY_Name_Manager+ 'SetSpForOpenAPI'
# 名单设置面试状态
SetIntvSts = path+DJY_Name_Manager+ 'SetIntvSts'
# 获取来源虚拟sp
GetVAgentListAPI = path+DJY_Name_Manager+ 'GetVAgentListAPI'
# 派遣端同步名单
SyncNameList = path+DJY_Name_Manager+ 'SyncNameList'
#招聘端同步面试状态
Sync_InterviewState=path+DJY_Name_Manager+'SynchronizeInterviewState'
#招聘端面试名单（商务）修改面试状态
Set_Business_InterviewState=path+DJY_Name_Manager+'SetBusinessInterviewState'
#招聘端面试名单（商务）设置去向劳务
Set_Labor=path+DJY_Name_Manager+'SetLabor'
# </editor-fold>

# <editor-fold desc="大佳营劳务模板DJY_Base_Manager">
DJY_Base_Manager ='api/v1/DJY_Base_Manager/'
# 获取工种列表
get_entborrow = path + DJY_Base_Manager + 'GetEntBorrowByUserType'
# 获取合作中供应商列表
GetCoopList = path + DJY_Base_Manager + 'GetCoopList'
# 获取订单页面查询条件供应商
GetCoopListWithDirection = path + DJY_Base_Manager + 'GetCoopListWithDirection'
# 企业管理页面查询企业
GetEntBorrowList = path + DJY_Base_Manager + 'GetEntBorrowList'
# 供应商管理页面查询供应商
# </editor-fold>

# <editor-fold desc="大佳营劳务模板Present_Comm">
Present_Comm = 'fw/api/v1/Present_Comm/'
# 获取谁送给我虚拟
get_vagent = path + Present_Comm + 'GetVAgentListAPI'
# 获取谁送给我真是
get_agent = path + Present_Comm + 'GetAgentListAPI'
# 获取虚拟劳务列表
get_vlabor = path + Present_Comm + 'GetVLaborListAPI'
# 获取真实劳务列表
get_labor = path + Present_Comm + 'GetLaborListAPI'
#获取银行列表接口
GetBankList_Api= path + Present_Comm + 'GetBankList'
#获取工牌企业接口
GetPayableTenantList_Api= path + Present_Comm + 'GetPayableTenantListAPI'
# 获取标准企业
GetTenantEntListByName = path + Present_Comm + 'GetTenantEntListByName'
GetEcTenantEntListByName = path + Present_Comm + 'GetEcTenantEntListByName'
# </editor-fold>

# <editor-fold desc="大佳营劳务模板Present_Audit">
Present_Audit = 'fw/api/v1/Present_Audit/'
#上传身份证接口
UploadIDCard = path + Present_Audit + 'ZXX_UploadIDCard'
#上传银行卡接口
AddBankCard_Api = path + Present_Audit + 'ZXX_AddBankCard'
#上传工牌接口
UploadWorkCard_Api = path + Present_Audit + 'ZXX_UploadWorkCard'
#获取身份证信息列表接口
IDCardInfoList_Api= path + Present_Audit + 'ZXX_QueryIDCardInfoList'
#身份证信息审核接口
AuditIDCard_Api= path + Present_Audit + 'ZXX_AuditIDCard'
#身份证信息审核看不清接口
ZXX_GetNextIDCardPic_Api=path + Present_Audit + 'ZXX_GetNextIDCardPic'
#获取银行卡信息列表接口
BankCardInfoList_Api= path + Present_Audit + 'ZXX_QueryBankCardInfoList'
#银行卡审核接口
AuditBankCard_Api= path + Present_Audit + 'ZXX_AuditBankCard'
#获取工牌信息列表接口
WorkCardInfoList_Api= path + Present_Audit + 'ZXX_QueryWorkCardInfoList'
#工牌审核接口
AuditWorkCard_Api= path + Present_Audit + 'ZXX_AuditWorkCard'
# </editor-fold>

# <editor-fold desc="大佳营劳务模板Present_Clock">
Present_Clock = 'fw/api/v1/Present_Clock/'
#打卡接口
Clock_Api= path + Present_Clock +'ZXX_Clock'
#补卡接口
RepairClock_Api= path + Present_Clock +'ZXX_Clock_RepairClockBySelf'
#web端补卡接口
WebRepairClock_Api=path + Present_Clock +'ZXX_Clock_ReissueClock'
ZXX_Clock_EntByWorkCard = path + Present_Clock + 'ZXX_Clock_EntByWorkCard'


# </editor-fold>

# <editor-fold desc="大佳营劳务模板Present_Pay_Salary">
Present_Pay_Salary = 'fw/api/v1/Present_Pay_Salary/'
#会员信息管理接口-获取企业接口
GetPaySalaryEntList_Api= path + Present_Pay_Salary + 'GetPaySalaryEntList'

# </editor-fold>

# <editor-fold desc="大佳营劳务模板JFF_Comm">
JFF_Comm = 'fw/api/v1/JFF_Comm/'
# 获取录入面单界面面试不通过状态列表
get_view_status_feild = path + JFF_Comm + 'GetViewStatusFieldList'
# </editor-fold>

# <editor-fold desc="大佳营劳务模板DJY_Order_Manager">
DJY_Order_Manager = 'api/v1/DJY_Order_Manager/'
# 新建订单
add_order = path + DJY_Order_Manager + 'CreateZXXNewOrder'
# 名单绑订单
Send_BindOrder = path + DJY_Order_Manager + 'Send_BindOrder'
# 审核及作废订单
JudgeOrder = path + DJY_Order_Manager + 'JudgeOrder'
# 查询订单
QueryZXXOrderList = path + DJY_Order_Manager + 'QueryZXXOrderList'
# 订单分配供应商
GetOrderReceiveInfo = path + DJY_Order_Manager + 'GetOrderReceiveInfo'
#审核订单
Judge_Order_api= path + DJY_Order_Manager + 'JudgeOrder'
#招聘端绑单
Recruit_BindOrder_api=path + DJY_Order_Manager + 'Recruit_BindOrder'
#招聘端绑单收单列表
LGetWaitToBindZXXOrderList_api=path + DJY_Order_Manager + 'LGetWaitToBindZXXOrderList'
#招聘端绑单发单列表
# GetWaitToBindZXXOrderList_api=path + DJY_Order_Manager + 'GetWaitToBindZXXOrderList'
# 获取订单分配对象
GetZXXOrderReceiveCoop = path + DJY_Order_Manager + 'GetZXXOrderReceiveCoop'
# 派遣端分配订单
PublishOrderToSupplier = path + DJY_Order_Manager + 'PublishOrderToSupplier'
# 派遣端查询订单
QuerySendZXXOrderList = path + DJY_Order_Manager + 'QuerySendZXXOrderList'
# </editor-fold>

# </editor-fold>
# 招聘端订单分配门店
Edit_OrderStoreList_api=path +'api/v1/DJY_Store_Manager/EditOrderStoreList'

# <editor-fold desc="大佳营劳务模板DJY_ConfigRequestHelper">
DJY_ConfigRequestHelper ='v1/DJY_ConfigRequestHelper/'
# 配置管理接口
modifyconfig = path + DJY_ConfigRequestHelper + 'ModifyConfig'

# </editor-fold>

# <editor-fold desc="大佳营劳务模板JFF_WaitSyncNameSvr">
JFF_WaitSyncNameSvr = 'fw/api/v1/JFF_WaitSyncNameSvr/'
# 获取待同步名单列表
JFF_WaitSyncName_GetWaitSyncNameList = path+ JFF_WaitSyncNameSvr +'JFF_WaitSyncName_GetWaitSyncNameList'
# </editor-fold>

# <editor-fold desc="大佳营劳务模板Present_WeekBillGen">
Present_WeekBillGen = 'fw/api/v1/Present_WeekBillGen/'
# 可预支导入预览
WeekBillGen_ImportCheck = path + Present_WeekBillGen + 'WeekBillGen_ImportCheck'
WeekBillGen_GetImportCheckResult =  path + Present_WeekBillGen + 'WeekBillGen_GetImportCheckResult'
# 可预支导入提交保存
WeekBillGen_GenerateBatchByBizID = path + Present_WeekBillGen + 'WeekBillGen_GenerateBatchByBizID'
WeekBillGen_GetGenerateBatchResult = path + Present_WeekBillGen + 'WeekBillGen_GetGenerateBatchResult'

# </editor-fold>
Present_WeekBill = 'fw/api/v1/Present_WeekBill/'
# 查询可预支账单
WeekBill_Select =  path + Present_WeekBill + 'WeekBill_Select'
# 可预支审核通过
WeekBill_Confirm = path + Present_WeekBill + 'WeekBill_Confirm'
# 可预支审核不通过
WeekBill_UnConfirm = path + Present_WeekBill + 'WeekBill_UnConfirm'

# </editor-fold>
#派遣端获取配置项接口
Get_All_Config=path+'api/v1/DJY_ConfigRequestHelper/GetAllConfig'
#派遣端修改配置项状态接口
Modify_Config=path+'api/v1/DJY_ConfigRequestHelper/ModifyConfig'



# <editor-fold desc="大佳营劳务模板Present_MonthBillGen">
Present_MonthBillGen = 'fw/api/v1/Present_MonthBillGen/'
# 月薪导入预览
MonthBillGen_ImportCheck = path + Present_MonthBillGen + 'MonthBillGen_ImportCheck'
# 获取月薪导入预检测结果
MonthBillGen_GetImportCheckResult = path + Present_MonthBillGen + 'MonthBillGen_GetImportCheckResult'
# 月薪提交保存
MonthBillGen_GenerateBatchByBizID = path + Present_MonthBillGen + 'MonthBillGen_GenerateBatchByBizID'
# 获取保存结果
MonthBillGen_GetGenerateBatchResult = path + Present_MonthBillGen + 'MonthBillGen_GetGenerateBatchResult'

# </editor-fold>

# <editor-fold desc="大佳营劳务模板Present_MonthBill">
Present_MonthBill = 'fw/api/v1/Present_MonthBill/'
# 月薪账单
MonthBill_select = path + Present_MonthBill + 'MonthBill_GetMonthBatchBillList'
# 月薪审核通过或不通过
MonthBill_Confirm = path + Present_MonthBill + 'MonthBill_SetMonthBillAuditState'

# </editor-fold>

# <editor-fold desc="大佳营劳务模板DJY_UnionOrder_Manager">
DJY_UnionOrder_Manager = 'api/v1/DJY_UnionOrder_Manager/'
# 创建多模式订单
add_order_mult = path + DJY_UnionOrder_Manager + 'CreateZXXNewOrder'
# 查询可绑定的订单列表
GetWaitToBindZXXOrderList = path + DJY_UnionOrder_Manager + 'GetWaitToBindZXXOrderList'
# </editor-fold>

# <editor-fold desc="招聘端绩效相关url">
#服务名
DJY_PerformanceManager = 'api/v1/DJY_PerformanceManager'
# 经纪人我的绩效获取绩效明细
url_GetPerformanceDetailList = path+DJY_PerformanceManager+'/GetPerformanceDetailList'

# </editor-fold>


# <editor-fold desc="大佳营中心平台">
# </editor-fold>