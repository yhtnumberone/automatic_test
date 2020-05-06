# coding=utf-8
from common.lib.login.web_login import *
from common.lib.comm_func.namelist import *
from common.lib.comm_func.system_management import *
from common.lib.venv.var import *
from common.lib.module_tools.tool import *
from common.lib.database.mysql_db import *
import unittest



class Broker_Namelist(unittest.TestCase):

    @classmethod
    def setUp(self):
        pass


    def test_Record_manually(self):
        #初始化测试数据变量
        inview_dt=nowtime
        sex=1
        IdCard_indate='2030-02-11'
        addr='测试地址'
        nation='汉'
        entname='神达小时工'
        LaborName='奇迹劳务'
        # 实例化NameList对象
        self.broker = NameList()
        #实例化Sys_Manage_Func对象
        sys = Sys_Manage_Func()
        sys.login('13340000001')
        #获取招聘端录入的名单自动同步至派遣端实接记录配置状态
        sync_keystatus = sys.get_config_staus('zp_sync_info_pq')
        # 开启招聘端录入的名单自动同步至派遣端实接记录配置
        if sync_keystatus=='false':
            res=sys.update_config_staus('zp_sync_info_pq','true')
            self.assertEqual(res['Code'], 0)
            self.assertEqual(res['Desc'], '成功')
        #获取开启招聘端名单同步至派遣端时，同步手机号码设置配置状态
        sync_mobile_keystatus = sys.get_config_staus('zp_sync_mobile_pq')
        #开启招聘端名单同步至派遣端时，同步手机号码设置配置
        if sync_mobile_keystatus=='false':
            res=sys.update_config_staus('zp_sync_mobile_pq','true')
            self.assertEqual(res['Code'], 0)
            self.assertEqual(res['Desc'], '成功')
        # 调用登录方法
        self.broker.login(broker_user)
        #获取brokeruserid
        brokeruserid=None
        brokeruserid = self.broker.Guid
        if brokeruserid==None:
            raise Exception('获取brokeruserid失败')
        # 加载企业
        self.broker.get_entbrorrow(entname)
        ent_id=None
        ent_id=self.broker.entbrorrowid
        if ent_id==None:
            raise Exception('获取ent_id失败')
        # 加载去向
        self.broker.get_labor(get_vlabor_zp, LaborName)
        labor_id=None
        labor_id=self.broker.TargetSpId
        #生成手机号码
        phone = create_phone()
        #生成身份证号码
        idcard = gennerator()
        #生成姓名
        name = create_name()
        if labor_id==None:
            raise Exception('获取labor_id失败')
        #调用手工录入接口，手工录入名单
        res=self.broker.create_api(add_interview,
                                   InterviewDate=inview_dt,
                                   RealName=name,
                                   Gender=sex,
                                   IDCardNum=idcard,
                                   IdCardExprDt=IdCard_indate,
                                   RsdtAddr=addr,
                                   Nation=nation,
                                   Mobile=phone,
                                   BrokerUserID=brokeruserid,
                                   EntID=ent_id,
                                   EntName=entname,
                                   LaborID=labor_id,
                                   LaborName=LaborName,
                                   InputType=2)
        #检查接口返回的desc和code
        self.assertEqual(res.json()['Code'],0)
        self.assertEqual(res.json()['Desc'], '成功')
        # 获取名单ID
        InterviewID = res.json()['Data']['InterviewID']
        JFFNameListId = res.json()['Data']['JFFNameListId']
        #初始化模板数据库对象
        djydb=djy_db()
        #初始化中台数据库对象
        ztdb=OperateMDdb()
        #获取中台center_user表会员的guid
        sql1=f"select guid from center_user where login_name={phone}"
        res=ztdb.realsql(sql1)
        self.assertNotEqual(res,())
        zt_guid=res[0][0]

        #获取模板user_member的guid,user_member_id
        sql2=f"select guid,user_member_id from user_member where mobile={phone}"
        res = djydb.realsql(sql2)
        self.assertNotEqual(res, (),msg='查询结果为空')
        djy_user_member_id=res[0][1]
        djy_guid = res[0][0]

        #判断zt_guid==djy_guid
        self.assertEqual(zt_guid, djy_guid)
        #获取broker_mbr_notebook表的录入名单会员的broker_user_id
        sql4=f"select broker_user_id from broker_mbr_notebook where member_id={djy_user_member_id}"
        res=djydb.realsql(sql4)
        self.assertNotEqual(res, (), msg='查询结果为空')
        djy_broker_user_id=res[0][0]
        #判断broker_mbr_notebook表的broker_user_id是否与录入名单的broker_user_id相等
        self.assertEqual(djy_broker_user_id, brokeruserid)

        #获取name_list_performance表数据
        sql3=f'''SELECT jff_namelist_id,intv_dt,member_idcard_num,guid,real_name,gender,mobile,nation,idcard_valid_date,address,broker_user_id,ent_id,ent_name,labor_id,labor_name
FROM
	name_list_performance 
WHERE
	name_list_performance_id={InterviewID}'''
        res=djydb.realsql(sql3)

        name_list_performance_dblist=list(res[0])
        #打印查询的结果
        pprint.pprint(name_list_performance_dblist)
        #构造输入参数列表
        input_param_list=[JFFNameListId,
                          switch_date(inview_dt),
                          idcard,
                          djy_guid,
                          name,
                          sex,
                          phone,
                          nation,
                          switch_date(IdCard_indate),
                          addr,
                          brokeruserid,
                          ent_id,
                          entname,
                          labor_id,
                          LaborName]
        #校验name_list_performances数据
        self.assertEqual(name_list_performance_dblist, input_param_list,msg='数据不相等')
        #获取中台招聘端name_list表数据
        sql5=f"SELECT name_list_id,intv_dt,mbr_id_card_num,real_name,mobile,gender,nation,rsdt_addr,id_card_expr_dt,rec_input_typ,sp_id,sp_ent_id,sp_ent_name,rcrt_typ,trgt_sp_id,trgt_tenant_coop_id,trgt_sp_short_name FROM name_list where mbr_id_card_num={idcard} and tenant_id=1000006"
        res=ztdb.realsql(sql5)
        self.assertEqual(len(res),1,msg='查询出数据库错误')
        zp_zt_namelist=list(res[0])
        pprint.pprint(zp_zt_namelist)
        #构造对比数据
        zp_zt_comparlist=[JFFNameListId,
                          switch_date(inview_dt),
                          idcard,
                          name,
                          phone,
                          sex,
                          nation,
                          addr,
                          switch_date(IdCard_indate),
                          2,
                          23060,
                          ent_id,
                          entname,
                          2,
                          23309,
                          labor_id,
                          LaborName]
        pprint.pprint(zp_zt_comparlist)
        #校验招聘name_list表数据
        self.assertEqual(zp_zt_namelist, zp_zt_comparlist, msg='数据不匹配')

        #获取中台name_list_sync表数据
        sql6=f"select intv_dt,mbr_id_card_num,real_name,gender,nation,rsdt_addr,id_card_expr_dt,sp_id,sp_ent_id,sp_ent_name,srce_sp_id,srce_sp_short_name,trgt_sp_id,is_sync from name_list_sync where name_list_id={JFFNameListId}"
        res=ztdb.realsql(sql6)
        self.assertEqual(len(res), 1, msg='查询出数据库错误')
        zt_name_sync_list=list(res[0])
        pprint.pprint(zt_name_sync_list)

        # 构造对比数据
        zt_namesync_comparlist=[switch_date(inview_dt),
                                idcard,
                                name,
                                sex,
                                nation,
                                addr,
                                switch_date(IdCard_indate),
                                23309,
                                ent_id,
                                entname,
                                23060,
                                '奇迹招聘',
                                0,
                                2]

        pprint.pprint(zt_namesync_comparlist)
        #校验name_list_sync表数据
        self.assertEqual(zt_name_sync_list, zt_namesync_comparlist, msg='数据不匹配')

        #获取同步到派遣端名单name_list数据
        sql7=f"SELECT intv_dt,mbr_id_card_num,real_name,mobile,gender,nation,rsdt_addr,id_card_expr_dt,rec_input_typ,sp_id,sp_ent_id,sp_ent_name,rcrt_typ,srce_sp_id,srce_tenant_coop_id,srce_sp_short_name FROM name_list where mbr_id_card_num={idcard} and tenant_id=1000005"
        res=ztdb.realsql(sql7)
        self.assertEqual(len(res), 1, msg='查询出数据库错误')
        pq_zt_namelist = list(res[0])
        pprint.pprint(pq_zt_namelist)

        #根据招聘端sp_ent_id获取派遣端sp_ent_id
        sql8=f"SELECT sp_ent_id FROM sp_ent_mapping where srce_sp_id=23060 and srce_sp_ent_id={ent_id}"
        res=ztdb.realsql(sql8)
        self.assertEqual(len(res), 1, msg='查询出数据库错误')
        pq_sp_ent=res[0][0]
        #构造对比数据
        pq_zt_name_comparlist=[switch_date(inview_dt),
                          idcard,
                          name,
                          phone,
                          sex,
                          nation,
                          addr,
                          switch_date(IdCard_indate),
                          4,
                          22699,
                          pq_sp_ent,
                          entname,
                          2,
                          23082,
                          23321,
                          '奇迹招聘']
        pprint.pprint(pq_zt_name_comparlist)
        # 校验派遣name_list表数据
        self.assertEqual(pq_zt_namelist, pq_zt_name_comparlist, msg='数据不匹配')


if __name__ == "__main__":
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(Broker_Namelist("test_Record_manually"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
