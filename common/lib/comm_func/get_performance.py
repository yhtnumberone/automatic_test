#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.login.web_login import Web_Login
from common.lib.venv.api_path import *
class GetPerformance(Web_Login):
    def getPerformanceDetailList(self,StDate,EndDate):




        res = self.create_api(url=url_GetPerformanceDetailList,
                                FromAppOrWeb=1,
                                 StDate=StDate,
                                 EndDate=EndDate,
                                 SearchKey="",
                                 WorkStatus=0,
                                 SearchType=1,
                                 PerformanceBrokerId=2390,
                                 RecordIndex=0,
                                 RecordSize=10)


        print(res.json())
        self.record_count = res.json()['Data']['RecordCount']




