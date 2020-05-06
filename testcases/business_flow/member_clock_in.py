from common.lib.comm_func.mem_information_manag_func import Member_information_management_func
from common.lib.comm_func.applet_func import Applet_func
from common.lib.pip_install import unittest
from common.lib.venv.var import send_boss_user
from common.lib.module_tools.analyze_result import get_api_result


class MemberClockInFlow(unittest.TestCase):

    def test_member_clock_in_flow(self):
        mem_manage = Member_information_management_func()
        mem_manage.login(send_boss_user)
        res = mem_manage.get_workcardlist(RecordSize=10,auditsts=2)
        result = res['Data']['RecordList']
        mobiles = []

        for r in result:
            if r['AuditBy'] == mem_manage.Name:
                mobiles.append(r['Mobile'])
        n = len(mobiles)
        for i in range(n):
            member = Applet_func()
            member.applogin(mobiles[i])
            member.colock_in(clocktype=1)

if __name__=='__main__':
    unittest.main()