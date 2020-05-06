from common.lib.comm_func.namelist import NameList
from common.lib.comm_func.applet_func import Applet_func
from common.lib.pip_install import unittest
from common.lib.venv.var import send_boss_user


class MemberClockInFlow(unittest.TestCase):

    def test_member_clock_in_flow(self):
        namemanage = NameList()
        namemanage.login(send_boss_user)
        namemanage.get_nameList(ScannerMobile=send_boss_user,RecordSize=100000)
        mobiles = namemanage.getMobilelist
        n = len(mobiles)
        for i in range(n):
            member = Applet_func()
            member.applogin(mobiles[i])
            member.colock_in(clocktype=2)