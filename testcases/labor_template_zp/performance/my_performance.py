import unittest
from common.lib.database.mysql_db import *
from common.lib.comm_func.get_performance import GetPerformance
from common.lib.venv.var import *


class MyPerformance(unittest.TestCase):

    mb_db = None

    @classmethod
    def setUpClass(cls):
        cls.object = GetPerformance()
        cls.object.login(zhouyu)
        cls.mb_db = djy_db()

    def test_GetPerformanceDetailList(self):
        #经纪人获取我的绩效
        self.object.getPerformanceDetailList('2020-03-09','2020-03-15')
        sql = f'select count(*) from salary_performance where bill_begin_dt = "2020-03-09"  and broker_user_id = 1360 '
        results = self.mb_db.selectsql(sql)
        self.assertEqual(self.object.record_count, results[0][0])


    @classmethod
    def tearDownClass(cls):
        cls.mb_db.close_db()


