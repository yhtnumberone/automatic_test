# coding=utf-8
from common.lib.login.web_login import *
from common.lib.comm_func.namelist import *
from common.lib.comm_func.system_management import *
from common.lib.venv.var import *
from common.lib.module_tools.tool import *
from common.lib.database.mysql_db import *
from common.lib.comm_func.orders import *
import unittest


class Manger_Namelist(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # 初始化测试数据变量
        self.inview_dt = nowtime
        self.sex = 1
        self.IdCard_indate = '2030-02-11'
        self.addr = '测试地址'
        self.nation = '汉'
        self.entname = '神达小时工'
        self.LaborName = '奇迹劳务'
        # 实例化NameList对象
        self.broker = NameList()
        # 实例化Sys_Manage_Func对象
        sys = Sys_Manage_Func()
        sys.login('13340000001')
        # 获取招聘端录入的名单自动同步至派遣端实接记录配置状态
        sync_keystatus = sys.get_config_staus('zp_sync_info_pq')
        # 开启招聘端录入的名单自动同步至派遣端实接记录配置
        if sync_keystatus == 'false':
            res = sys.update_config_staus('zp_sync_info_pq', 'true')
            assert res['Code']==0
            assert res['Desc']=='成功'
        # 获取开启招聘端名单同步至派遣端时，同步手机号码设置配置状态
        sync_mobile_keystatus = sys.get_config_staus('zp_sync_mobile_pq')
        # 开启招聘端名单同步至派遣端时，同步手机号码设置配置
        if sync_mobile_keystatus == 'false':
            res = sys.update_config_staus('zp_sync_mobile_pq', 'true')
            assert res['Code'] == 0
            assert res['Desc'] == '成功'
        #开启招聘端身份证、手机、银行卡信息展示不脱敏
        res=sys.update_config_staus('zp_not_tm', 'true')
        print(res)
        assert res['Code'] == 0
        assert res['Desc'] == '成功'
        #开启派遣端身份证、手机、银行卡信息展示不脱敏
        res = sys.update_config_staus('pq_not_tm', 'true')
        assert res['Code'] == 0
        assert res['Desc'] == '成功'
        # 调用登录方法
        self.broker.login(broker_user)
        # 获取brokeruserid
        self.brokeruserid = None
        self.brokeruserid = self.broker.Guid
        if self.brokeruserid == None:
            raise Exception('获取brokeruserid失败')
        # 加载企业
        self.broker.get_entbrorrow(self.entname)
        self.ent_id = None
        self.ent_id = self.broker.entbrorrowid
        if self.ent_id == None:
            raise Exception('获取ent_id失败')
        # 加载去向
        self.broker.get_labor(get_vlabor_zp, self.LaborName)
        self.labor_id = None
        self.labor_id = self.broker.TargetSpId
        if self.labor_id == None:
            raise Exception('获取labor_id失败')
        # 生成手机号码
        self.phone = create_phone()
        # 生成身份证号码
        self.idcard = gennerator()
        # 生成姓名
        self.name = create_name()
        # 调用手工录入接口，手工录入名单
        res = self.broker.create_api(add_interview,
                                     InterviewDate=self.inview_dt,
                                     RealName=self.name,
                                     Gender=self.sex,
                                     IDCardNum=self.idcard,
                                     IdCardExprDt=self.IdCard_indate,
                                     RsdtAddr=self.addr,
                                     Nation=self.nation,
                                     Mobile=self.phone,
                                     BrokerUserID=self.brokeruserid,
                                     EntID=self.ent_id,
                                     EntName=self.entname,
                                     LaborID=self.labor_id,
                                     LaborName=self.LaborName,
                                     InputType=2)
        pprint.pprint(res.json())
        # 检查接口返回的desc和code
        assert res.json()['Code'] == 0
        assert res.json()['Desc'] == '成功'
        # 获取名单ID
        self.InterviewID = res.json()['Data']['InterviewID']
        self.JFFNameListId = res.json()['Data']['JFFNameListId']
        print('初始化化成功')

    def test_sync_intv_sts(self):
        #初始化招聘端老板角色的name_list对象
        zp_manger=NameList()
        zp_manger.login('13330000003')
        #面试名单商务页面获取录入的名单的信息
        res=zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        re_list=res[0]
        #筛选面试名单（商务）页面返回到名单信息赋值给list
        zp_namelist=[re_list['InterviewDate'],
                       re_list['MemberName'],
                       re_list['MemberMobile'],
                       re_list['MemberIDCardNum'],
                       re_list['Gender'],
                       re_list['Nation'],
                       re_list['RsdtAddr'],
                       re_list['EntName'],
                       re_list['EntID'],
                       re_list['LaborID'],
                       re_list['LaborName'],
                       re_list['StoreId'],
                       re_list['BrokerRealName'],
                       re_list['BrokerName'],
                       re_list['JFFNameListId'],]

        #获取store_id,brokerrealname,brokername
        sql=f'SELECT store_user.store_id,user_cert.real_name,user.name_cn FROM store_user,user,user_cert where store_user.user_id=user.user_id and store_user.user_cert_id=user_cert.user_cert_id and user.user_id={self.brokeruserid}'
        # 初始化模板数据库对象
        djydb = djy_db()
        res=djydb.realsql(sql)
        self.assertNotEqual(res, ())
        store_id = res[0][0]
        brokerrealname=res[0][1]
        brokername=res[0][2]
        # 构造对比数据
        name_comparelist=[self.inview_dt,
                          self.name,
                          self.phone,
                          self.idcard,
                          self.sex,
                          self.nation,
                          self.addr,
                          self.entname,
                          self.ent_id,
                          self.labor_id,
                          self.LaborName,
                          store_id,
                          brokerrealname,
                          brokername,
                          self.JFFNameListId]
        #校验输入的参数和面试名单（商务）页面数据是否一致
        pprint.pprint(zp_namelist)
        pprint.pprint(name_comparelist)
        self.assertEqual(zp_namelist,name_comparelist)
        #初始化派遣端老板角色的name_list对象
        pq_manger=NameList()
        pq_manger.login('13340000001')
        # 派遣端实接记录页面获取同步的名单的信息
        res=pq_manger.get_nameList(name=self.name,idcardnum=self.idcard)
        pqre_list=res['Data']['RecordList'][0]
        #记录派遣端namelist_id
        pq_namelist_id=pqre_list['NameID']
        # 筛选实接记录页面返回到名单信息赋值给list
        pq_namelist=[pqre_list['InterviewDate'],
                     pqre_list['SpEntName'],
                     pqre_list['Name'],
                     pqre_list['Mobile'],
                     pqre_list['IDCardNum'],
                     pqre_list['FromSpName'],
                     pqre_list['Gender'],
                     pqre_list['Nation'],
                     pqre_list['Addr'],
                     pqre_list['IDCardExprDate'],
                     pqre_list['SpName']
                     ]
        # 构造对比数据
        pq_comparenamelist=[self.inview_dt,
                            self.entname,
                            self.name,
                            self.phone,
                            self.idcard,
                            '奇迹招聘',
                            self.sex,
                            self.nation,
                            self.addr,
                            self.IdCard_indate,
                            self.LaborName]
        #校验实接记录页面名单数据是否正确
        self.assertEqual(pq_namelist,pq_comparenamelist)
        #修改实接记录页面名单的面试状态
        res=pq_manger.create_api(SetIntvSts,IntvSts=2,NameIdList=[pq_namelist_id])
        pprint.pprint(res.json())
        #判断接口返回值
        self.assertEqual(res.json()['Code'], 0)
        self.assertEqual(res.json()['Desc'], '成功')
        #获取名单修改后的面试状态
        res = pq_manger.get_nameList(name=self.name, idcardnum=self.idcard)
        after_intv_staus=res['Data']['RecordList'][0]['InterviewStatus']
        self.assertEqual(after_intv_staus,2)
        #招聘端面试名单（商务）页面同步面试状态
        res=zp_manger.Sync_InterviewStatus([self.InterviewID])
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        #获取同步面试状态后名单的面试状态
        res = zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        sync_intv_staus=res[0]['InterviewState']
        self.assertEqual(sync_intv_staus,2)

        #再次修改派遣端实接记录页面名单的面试状态
        res = pq_manger.create_api(SetIntvSts, IntvSts=3, NameIdList=[pq_namelist_id])
        pprint.pprint(res.json())
        # 判断接口返回值
        self.assertEqual(res.json()['Code'], 0)
        self.assertEqual(res.json()['Desc'], '成功')
        # 获取名单修改后的面试状态
        res = pq_manger.get_nameList(name=self.name, idcardnum=self.idcard)
        after_intv_staus = res['Data']['RecordList'][0]['InterviewStatus']
        self.assertEqual(after_intv_staus, 3)

        # 招聘端面试名单（商务）页面同步面试状态
        res = zp_manger.Sync_InterviewStatus([self.InterviewID])
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 获取同步面试状态后名单的面试状态
        res = zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        sync_intv_staus = res[0]['InterviewState']
        self.assertEqual(sync_intv_staus, 2)


    def test_modfiy_intv_staus(self):
        # 初始化招聘端老板角色的name_list对象
        zp_manger = NameList()
        zp_manger.login('13330000003')
        #修改名单面试状态为面试通过
        res=zp_manger.Modfiy_Zp_InterviewStatus(1,[self.InterviewID])
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')

        # 获取修改面试状态后名单的面试状态
        res = zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        intv_staus = res[0]['InterviewState']
        self.assertEqual(intv_staus,1)

        #修改名单面试状态为面试不通过
        res = zp_manger.Modfiy_Zp_InterviewStatus(3, [self.InterviewID],interviewstscode=4)
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 获取修改面试状态后名单的面试状态
        res = zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        intv_staus = res[0]['InterviewState']
        self.assertEqual(intv_staus, 3)
        #获取name_list_performance表名单的real_intv_state、intv_sts_code
        # 初始化模板数据库对象
        djydb = djy_db()
        sql=f"SELECT real_intv_state,intv_sts_code FROM name_list_performance where name_list_performance_id={self.InterviewID}"
        res=djydb.realsql(sql)
        real_intv_state=res[0][0]
        intv_sts_code=res[0][1]
        self.assertEqual(real_intv_state,3)
        self.assertEqual(intv_sts_code,4)


    def test_set_labour(self):
        # 初始化招聘端老板角色的name_list对象
        zp_manger = NameList()
        zp_manger.login('13330000003')
        # 获取名单当前劳务id和名称
        res = zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        current_laborid=res[0]['LaborID']
        current_laborname=res[0]['LaborName']

        #修改名单的去向劳务
        res=zp_manger.Set_Trgtlabour('测试劳务',[self.InterviewID])
        # 判断接口返回值
        self.assertEqual(res[0]['Code'], 0)
        self.assertEqual(res[0]['Desc'], '成功')
        #获取返回的labor_id
        inut_laborid=res[1]
        # 获取名单修改后劳务id和名称
        res = zp_manger.get_business_interview_list(membername=self.name, memberidcardnum=self.idcard)
        after_laborid=res[0]['LaborID']
        after_laborname=res[0]['LaborName']
        #校验劳务id和名称与之前不相等
        self.assertNotEqual(current_laborid,after_laborid)
        self.assertNotEqual(current_laborname,after_laborname)
        #校验劳务id和名称与输入的一致
        self.assertEqual(after_laborid,inut_laborid)
        self.assertEqual(after_laborname,'测试劳务')

        # 初始化模板数据库对象
        djydb = djy_db()
        # 初始化中台数据库对象
        ztdb = OperateMDdb()
        #获取name_list_performance表劳务id和名称
        sql=f"SELECT labor_id,labor_name FROM name_list_performance where name_list_performance_id={self.InterviewID}"
        res=djydb.realsql(sql)
        db_laborid=res[0][0]
        db_laborname=res[0][1]
        #校验name_list_performance表劳务id和名称是否正确
        self.assertEqual(after_laborid, db_laborid)
        self.assertEqual(after_laborname, db_laborname)
        # 获取中台name_list表劳务id和名称
        sql1=f"select trgt_tenant_coop_id,trgt_sp_short_name from name_list where name_list_id={self.JFFNameListId}"
        res=ztdb.realsql(sql1)
        zt_laborid=res[0][0]
        zt_laborname=res[0][1]
        # 校验中台name_list表劳务id和名称是否正确
        self.assertEqual(after_laborid, zt_laborid)
        self.assertEqual(after_laborname, zt_laborname)

        # 恢复名单的去向劳务
        res = zp_manger.Set_Trgtlabour('奇迹劳务', [self.InterviewID])
        # 判断接口返回值
        self.assertEqual(res[0]['Code'], 0)
        self.assertEqual(res[0]['Desc'], '成功')

    def test_band_collect_order(self):
        # 初始化招聘端老板角色的name_list对象
        zp_manger = NameList()
        zp_manger.login('13330000003')
        #初始化Order对象
        pq_order=Order()
        pq_order.login('13340000001')
        #创建派遣端订单
        res=pq_order.create_order_pq(self.entname)
        pq_orderid=int(res)
        self.assertNotEqual(pq_orderid,None,msg='创建订单失败')
        #审核通过订单
        res=pq_order.Judge_Order(2,pq_orderid)
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 初始化模板数据库对象
        djydb = djy_db()
        #获取名单的门店id
        sql = f'SELECT store_user.store_id FROM store_user,user,user_cert where store_user.user_id=user.user_id and store_user.user_cert_id=user_cert.user_cert_id and user.user_id={self.brokeruserid}'
        res = djydb.realsql(sql)
        self.assertNotEqual(res, ())
        store_id = res[0][0]
        #订单分配门店
        res=pq_order.Edit_Order_Store(pq_orderid,2,[store_id])
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        #获取store_order表数据
        store_order_sql=f"SELECT utd_store_id,shop_usr_fee_rate,shop_mgr_fee_rate FROM store_order where rcrt_order_main_id={pq_orderid}"
        res=djydb.realsql(store_order_sql)
        #获取名单的门店对应的utd_store_id,shop_usr_fee_rate,shop_mgr_fee_rate
        db_storeid=None
        db_shop_usr_fee_rate=None
        db_shop_mgr_fee_rate=None
        for one in res:
            if one[0]==store_id:
                db_storeid=one[0]
                db_shop_usr_fee_rate=one[1]
                db_shop_mgr_fee_rate=one[2]
                break
        #判断db_storeid是否落入表中
        self.assertNotEqual(db_storeid,None,msg='未查找到db_storeid')
        #校验utd_store_id,shop_usr_fee_rate,shop_mgr_fee_rate是否正确
        self.assertEqual(store_id,db_storeid)
        self.assertEqual(db_shop_usr_fee_rate, 350)
        self.assertEqual(db_shop_mgr_fee_rate, 30)
        #获取名单绑收单的订单列表
        res=zp_manger.zp_collect_orderlist(self.entname,self.inview_dt,self.labor_id,store_id)
        #校验订单id是否在返回的结果中
        mainorderdilist=[]
        for one in res:
            mainorderdilist.append(one['MainOrderId'])

        self.assertIn(pq_orderid,mainorderdilist,msg='创建的订单不在名单的收单列表中')
        #名单绑定收单
        res=zp_manger.zp_bind_order([self.JFFNameListId],pq_orderid,2)
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        #校验订单id是否落到name_list_performance表
        namelistperformancesql=f"SELECT std_order_id,std_order_tenant_type FROM name_list_performance where name_list_performance_id={self.InterviewID}"
        res=djydb.realsql(namelistperformancesql)
        std_order_id=res[0][0]
        std_order_tenant_type=res[0][1]
        self.assertEqual(std_order_id,pq_orderid,msg='订单id错误')
        self.assertEqual(std_order_tenant_type, 2,msg='订单类型错误')

    def test_band_send_order(self):
        # 初始化招聘端老板角色的name_list对象
        zp_manger = NameList()
        zp_manger.login('13330000003')
        # 初始化招聘端Order对象
        zp_order = Order()
        zp_order.login('13330000004')
        #创建招聘端订单,获取返回的订单id
        res=zp_order.create_order_zp(self.entname,LaborName=self.LaborName)
        zp_order_id=int(res)
        #审核通过创建的订单
        res = zp_order.Judge_Order(2, zp_order_id)
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 初始化模板数据库对象
        djydb = djy_db()
        # 获取名单的门店id
        sql = f'SELECT store_user.store_id FROM store_user,user,user_cert where store_user.user_id=user.user_id and store_user.user_cert_id=user_cert.user_cert_id and user.user_id={self.brokeruserid}'
        res = djydb.realsql(sql)
        self.assertNotEqual(res, ())
        store_id = res[0][0]
        #订单分配门店
        res = zp_order.Edit_Order_Store(zp_order_id, 1, [store_id])
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 获取store_order表数据
        store_order_sql = f"SELECT utd_store_id,shop_usr_fee_rate,shop_mgr_fee_rate FROM store_order where rcrt_order_main_id={zp_order_id}"
        res = djydb.realsql(store_order_sql)
        # 获取名单的门店对应的utd_store_id,shop_usr_fee_rate,shop_mgr_fee_rate
        db_storeid = None
        db_shop_usr_fee_rate = None
        db_shop_mgr_fee_rate = None
        for one in res:
            if one[0] == store_id:
                db_storeid = one[0]
                db_shop_usr_fee_rate = one[1]
                db_shop_mgr_fee_rate = one[2]
                break
        # 判断db_storeid是否落入表中
        self.assertNotEqual(db_storeid, None, msg='未查找到db_storeid')
        # 校验utd_store_id,shop_usr_fee_rate,shop_mgr_fee_rate是否正确
        self.assertEqual(store_id, db_storeid)
        self.assertEqual(db_shop_usr_fee_rate, 350)
        self.assertEqual(db_shop_mgr_fee_rate, 30)
        #获取名单绑发单的订单列表
        res=zp_manger.zp_send_orderlist(self.ent_id,self.labor_id,self.inview_dt,store_id)
        # 校验订单id是否在返回的结果中
        mainorderdilist = []
        for one in res:
            mainorderdilist.append(one['MainOrderId'])

        self.assertIn(zp_order_id, mainorderdilist, msg='创建的订单不在名单的收单列表中')
        # 名单绑定收单
        res = zp_manger.zp_bind_order([self.JFFNameListId], zp_order_id, 1)
        # 判断接口返回值
        self.assertEqual(res['Code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 校验订单id是否落到name_list_performance表
        namelistperformancesql = f"SELECT std_order_id,std_order_tenant_type FROM name_list_performance where name_list_performance_id={self.InterviewID}"
        res = djydb.realsql(namelistperformancesql)
        std_order_id = res[0][0]
        std_order_tenant_type = res[0][1]
        self.assertEqual(std_order_id, zp_order_id, msg='订单id错误')
        self.assertEqual(std_order_tenant_type, 1, msg='订单类型错误')

        #校验订单id是否落到name_lsit表
        # 初始化中台数据库对象
        ztdb = OperateMDdb()
        ztname_list_sql=f"SELECT trgt_rcrt_order_id,trgt_rcrt_order_vid FROM name_list where name_list_id={self.JFFNameListId}"
        res=ztdb.realsql(ztname_list_sql)
        trgt_rcrt_order_id=res[0][0]
        trgt_rcrt_order_vid=int(res[0][1])
        self.assertEqual(trgt_rcrt_order_id,zp_order_id,msg='订单id不匹配')
        self.assertEqual(trgt_rcrt_order_vid, zp_order_id,msg='订单id不匹配')









if __name__ == '__main__':
    unittest.main()
    # # 构造测试集
    # suite = unittest.TestSuite()
    # suite.addTest(Manger_Namelist("test_band_send_order"))
    # # 执行测试
    # runner = unittest.TextTestRunner()
    # runner.run(suite)

