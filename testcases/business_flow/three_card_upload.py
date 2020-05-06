from common.lib.comm_func.applet_func import Applet_func
from common.lib.comm_func.mem_information_manag_func import Member_information_management_func
from common.lib.comm_func.namelist import NameList
from common.lib.venv.var import send_boss_user,nowtime
from common.lib.module_tools.tool import create_workcardno,create_bankcard
from common.lib.module_tools.analyze_result import get_api_result
from common.lib.pip_install import unittest

bankname = '兴业银行'

class ThreeCardFlow(unittest.TestCase):

    def test_threecardflow(self):
        # 先获取当天录入的名单手机号码，姓名，身份证号
        namemanage = NameList()
        namemanage.login(send_boss_user)
        namemanage.get_nameList(starttime=nowtime,endtime=nowtime,ScannerMobile=send_boss_user,RecordSize=1000)
        mobiles = namemanage.getMobilelist
        names = namemanage.getrealnamelist
        idcardnums = namemanage.getidcardlist
        ents = namemanage.getentlist
        # 初始化审核身份证对象，并登陆
        mem_manage = Member_information_management_func()
        mem_manage.login(send_boss_user)
        # 根据获取的手机号码依次登陆上传三卡并认证
        n = len(mobiles)
        for i in range(n):
            # 登陆
            member = Applet_func()
            member.applogin(mobiles[i])
            # 上传身份证
            member.upload_idcard()
            # 审核身份证
            mem_manage.audit_idcard(idcardnum=idcardnums[i], rname=names[i], phone=mobiles[i])
            # 断言-检查身份证审核状态
            idcard_res = mem_manage.get_idcardlist(phone=mobiles[i],RegTimeBegin=nowtime,RegTimeEnd=nowtime)
            AuditSts = get_api_result(idcard_res,'AuditSts')[0]
            self.assertEqual(AuditSts,2)
            # 上传银行卡
            member.upload_bankcard(bankname=bankname)
            # 审核银行卡
            bankcardnum = create_bankcard()
            mem_manage.audit_bankcard(bankcardnum=bankcardnum, bankname=bankname, phone=mobiles[i])
            # 断言-检查银行卡审核状态
            bank_res = mem_manage.get_bankcardlist(phone=mobiles[i],UploadTimeBegin=nowtime,UploadTimeEnd=nowtime)
            AuditSts = get_api_result(bank_res,'AuditSts')[0]
            self.assertEqual(AuditSts,2)
            # 上传工牌
            member.upload_workcard(entname=ents[i])
            # 审核工牌
            workcardno = create_workcardno()
            mem_manage.audit_workcard(entshortname=ents[i], workcardno=workcardno, phone=mobiles[i])
            workcar_res = mem_manage.get_workcardlist(phone=mobiles[i],UploadTimeBegin=nowtime,UploadTimeEnd=nowtime)
            AuditSts = get_api_result(workcar_res,'AuditSts')[0]
            self.assertEqual(AuditSts,2)

if __name__=='__main__':
    unittest.main()