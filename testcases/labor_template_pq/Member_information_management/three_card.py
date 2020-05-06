# coding=utf-8
from common.lib.login.web_login import *
from common.lib.comm_func.namelist import *
from common.lib.comm_func.system_management import *
from common.lib.venv.var import *
from common.lib.module_tools.tool import *
from common.lib.database.mysql_db import *
from common.lib.comm_func.orders import *
from common.lib.comm_func.applet_func import *
from common.lib.comm_func.mem_information_manag_func import *
import unittest


class Three_Card(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # 初始化测试数据变量
        self.inview_dt = nowtime
        self.sex = 1
        self.IdCard_indate = '2030-02-11'
        self.addr = '测试地址'
        self.nation = '汉'
        self.entname = '昆山昆达电脑'
        self.entbrorrowname='神达小时工'
        self.source='自动化测试供应商'
        # 生成身份证号码
        self.idcard = gennerator()
        # 生成姓名
        self.name = create_name()
        # 实例化OperateTMdb对象
        self.zt_db = OperateMDdb()
        #实例化Applet_func对象
        self.applet=Applet_func()
        #实例化Member_information_management_func对象
        self.webfunc=Member_information_management_func()
        #随机生成新的手机号码
        while True:
            self.phone=create_phone()
            #查询手机号码在center_user表是否存在
            centeruser_sql=f'select * from center_user where login_name={self.phone}'
            res=self.zt_db.realsql(centeruser_sql)
            if res==():
                break
        #登录web
        self.webfunc.login('13340000001')
        #登录小程序
        self.applet.applogin(self.phone)
        #实例化name_list对象并登陆
        self.web_namelist=NameList()
        self.web_namelist.login('13340000001')
        #web录入名单并绑定订单
        res=self.web_namelist.add_name_pq(entname=self.entname,
                                      entbrorrowname=self.entbrorrowname,
                                      mobile=self.phone,
                                      idnum=self.idcard,
                                      name=self.name,
                                      gender=self.sex,
                                      InterviewDate=self.inview_dt,
                                      FromSpName=self.source)
        #校验接口返回的结果
        assert res['Code'] == 0
        assert res['Desc'] == '成功'
        #获取NameListId
        self.NameListId=res['Data']['NameListId']
        # 初始化Order对象
        pq_order = Order()
        pq_order.login('13340000001')
        # 创建派遣端订单
        res = pq_order.create_order_pq(self.entbrorrowname,
                                       ReceiverType=2,
                                       SettlementTyp=1)
        orderid =res['Data']
        # 审核通过订单
        res = pq_order.Judge_Order(2, orderid)
        # 判断接口返回值
        assert res['Code'] == 0
        assert res['Desc'] == '成功'
        #订单分配供应商
        res=pq_order.order_allocation_pq(self.source,
                                     OrderId=orderid)
        # 判断接口返回值
        assert res['Code'] == 0
        assert res['Desc'] == '成功'
        #实接记录页面名单绑定订单
        res=self.web_namelist.bind_order(orderid,self.NameListId)
        # 判断接口返回值
        assert res['Code'] == 0
        assert res['Desc'] == '成功'
        time.sleep(30)
        #校验名单是否同步到name_list_settle表
        settle_sql=f'select * from name_list_settle where name_list_id={self.NameListId}'
        res=self.zt_db.realsql(settle_sql)
        if res==():
            raise Exception('名单同步到name_list_settle表失败')


    def test_idcard_audit(self):
        # 获取会员的guid
        user_guid = self.applet.Guid
        #验证center_user表数据
        centeruser_sql=f'select guid from center_user where login_name={self.phone}'
        res = self.zt_db.realsql(centeruser_sql)
        #校验guid是否正确
        self.assertEqual(user_guid,res[0][0],msg='guid不相同')
        #验证member_user表数据
        memberuser_sql=f'select uuid,guid from member_user where mobile={self.phone}'
        res = self.zt_db.realsql(centeruser_sql)
        self.assertEqual((0,user_guid),res[0],msg='member_user表数据有误')
        #会员上传身份证
        res=self.applet.upload_idcard()
        #校验接口返回结果
        self.assertEqual(res['code'],0)
        self.assertEqual(res['Desc'], '成功',msg='上传身份证失败')
        #获取member_user_idcard_audit数据
        idcardaudit_sql=f'select audit_sts,user_idcard_audit_id from member_user_idcard_audit where guid={user_guid}'
        res=self.zt_db.realsql(idcardaudit_sql)
        #校验数据不为空并且只存在一条
        self.assertEqual(len(res),1,msg='数据大于1条')
        #校验落表数据审核状态
        self.assertEqual(1,res[0][0],msg='审核状态有误')
        #获取user_idcard_audit_id
        idcardaudit_id=res[0][1]
        #获取身份证信息查询页面会员上传的身份证信息
        res=self.webfunc.get_idcardlist(phone=self.phone)
        #校验身份证信息是否正确
        self.assertEqual(res['data']['RecordCount'],1,msg='RecordCount返回有误')
        AuditSts=res['data']['RecordList'][0]['AuditSts']
        Mobile=res['data']['RecordList'][0]['Mobile']
        UserIdcardAuditId=res['data']['RecordList'][0]['UserIdcardAuditId']
        self.assertEqual([AuditSts,Mobile, UserIdcardAuditId],[1,self.phone,idcardaudit_id],msg='身份证信息返回有误')
        #审核不通过身份证
        res=self.webfunc.IDCardPic(UserIdcardAuditId)
        #校验接口返回参数
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['Desc'], '成功')
        # 获取member_user_idcard_audit数据
        idcardaudit_sql = f'select audit_sts from member_user_idcard_audit where user_idcard_audit_id={UserIdcardAuditId}'
        res = self.zt_db.realsql(idcardaudit_sql)
        #校验数据库审核状态
        self.assertEqual(3,res[0][0],msg='审核状态有误')
        # 获取身份证信息查询页面会员上传的身份证信息
        res = self.webfunc.get_idcardlist(phone=self.phone)
        AuditSts = res['data']['RecordList'][0]['AuditSts']
        # 校验列表审核状态
        self.assertEqual(3, AuditSts, msg='审核状态有误')
        # 会员再次上传身份证
        res = self.applet.upload_idcard()
        # 校验接口返回结果
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['Desc'], '成功', msg='上传身份证失败')
        # 获取member_user_idcard_audit数据
        idcardaudit_sql = f'select audit_sts,user_idcard_audit_id from member_user_idcard_audit where guid={user_guid} order by created_tm desc limit 1'
        res = self.zt_db.realsql(idcardaudit_sql)
        user_idcard_audit_id=res[0][2]
        # 校验落表数据审核状态
        self.assertEqual(1, res[0][0], msg='审核状态有误')
        #会员上传工牌
        res=self.applet.upload_workcard(self.entname)
        #校验接口返回结果
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['Desc'], '成功', msg='上传工牌失败')
        #获取工牌审核表数据
        workcardaudit_sql=f'select uuid,user_work_card_audit_id,audit_sts from member_user_work_card_audit where guid={user_guid} limit 1'
        res=self.zt_db.realsql(workcardaudit_sql)
        uuid=res[0][0]
        audit_sts=res[0][2]
        wordaudit_id=res[0][1]
        #校验工牌审核表数据
        self.assertEqual((0,1),(uuid,audit_sts),msg='工牌审核表数据有误')
        #会员打卡
        res=self.applet.colock_in(1)
        # 校验接口返回结果
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['Desc'], '成功', msg='打卡失败')
        # 获取打卡表数据
        clock_sql=f'select uuid from member_user_clock_rec where guid={user_guid}'
        res=self.zt_db.realsql(clock_sql)
        #校验打卡数据
        self.assertEqual(0,res[0][0],msg='uuid有误')
        #获取name_list_settle表数据
        settle_sql = f'select uuid from name_list_settle where name_list_id={self.NameListId}'
        res = self.zt_db.realsql(settle_sql)
        #校验name_list_settle表uuid数据
        self.assertEqual(0, res[0][0], msg='uuid有误')
        #审核身份证
        res=self.webfunc.audit_idcard(self.idcard,
                                  self.name,
                                  useridcardauditid=user_idcard_audit_id)
        # 校验接口返回结果
        self.assertEqual(res['code'], 0)
        self.assertEqual(res['Desc'], '成功', msg='审核身份证失败')
        # 获取member_user_idcard_audit数据
        idcardaudit_sql = f'select audit_sts from member_user_idcard_audit where user_idcard_audit_id={user_idcard_audit_id} order by created_tm desc limit 1'
        res = self.zt_db.realsql(idcardaudit_sql)
        #校验审核状态
        self.assertEqual(2,res[0][0],msg='审核状态错误')
        # 获取member_user_idcard数据
        idcard_sql=f'select real_name,id_card_num from member_user_idcard where guid={user_guid}'
        res=self.zt_db.realsql(idcard_sql)
        #校验member_user_idcard数据
        self.assertEqual((self.name,self.idcard),res[0],msg='member_user_idcard数据有误')
        #获取member_user_unique表数据
        unique_sql=f'select uuid,id_card_num,real_name from member_user_unique where id_card_num={self.idcard}'
        res = self.zt_db.realsql(unique_sql)
        #校验member_user_unique表数据
        self.assertNotEqual(res,(),msg='返回结果为空元组')
        id_card_num=res[0][1]
        real_name=res[0][2]
        uuid=res[0][0]
        self.assertEqual((self.idcard,self.name),(id_card_num,real_name),msg='身份证号码和姓名有误')
        #获取member_user数据
        memuser_sql=f'select uuid from member_user where guid={user_guid}'
        res=self.zt_db.realsql(memuser_sql)
        #校验member_user数据
        self.assertEqual(uuid,res[0][0],msg='uuid有误')
        # 获取name_list_settle表数据
        settle_sql = f'select uuid from name_list_settle where name_list_id={self.NameListId}'
        res = self.zt_db.realsql(settle_sql)
        # 校验name_list_settle表uuid数据
        self.assertEqual(uuid, res[0][0], msg='uuid有误')
        # 获取工牌审核表数据
        workcardaudit_sql = f'select uuid from member_user_work_card_audit where user_work_card_audit_id={wordaudit_id} limit 1'
        res = self.zt_db.realsql(workcardaudit_sql)
        #校验工牌审核数据
        self.assertEqual(uuid,res[0][0],msg='uuid有误')
        # 获取打卡表数据
        clock_sql = f'select uuid from member_user_clock_rec where guid={user_guid}'
        res = self.zt_db.realsql(clock_sql)
        # 校验打卡数据
        self.assertEqual(uuid, res[0][0], msg='uuid有误')


if __name__ == '__main__':
    unittest.main()