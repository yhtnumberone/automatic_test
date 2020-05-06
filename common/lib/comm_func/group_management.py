#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.login.web_login import Web_Login
from common.lib.venv.api_path import GetEntBorrowList,GetCoopList

class GroupManagement(Web_Login):
    def getEntBorrowList(self,EntShortName='',EntName='',BEntName='',IsEnabled=-9999,RcrtType=-9999,RecordIndex=0,RecordSize=10):
        result = self.create_api(GetEntBorrowList,
                                    EntShortName=EntShortName,
                                    EntName=EntName,
                                    BEntName=BEntName,
                                    IsEnabled=IsEnabled,
                                    RcrtType=RcrtType,
                                    RecordIndex=RecordIndex,
                                    RecordSize=RecordSize)
        res = result.json()
        return res

    def getcooplist(self,NickName='',Principal='',Mobile='',CooperationStatus=-9999,RspsUserId=-9999,RecordIndex=0,RecordSize=10):
        result = self.create_api(GetCoopList,
                                       NickName=NickName,
                                       Principal=Principal,
                                       Mobile=Mobile,
                                       CooperationStatus=CooperationStatus,
                                       RspsUserId=RspsUserId,
                                       RecordIndex=RecordIndex,
                                       RecordSize=RecordSize
                                       )
        res = result.json()
        return res