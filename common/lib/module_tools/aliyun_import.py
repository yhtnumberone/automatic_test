from common.lib.pip_install import oss2
from common.lib.venv.api_path import *
from common.lib.login.web_login import Web_Login
from common.lib.module_tools.analyze_result import get_api_result


class AlImport(Web_Login):
    def ali_import(self,myObjectName,myLocalFile,region = 'http://oss-cn-shanghai.aliyuncs.com',bucketname= 'woda-app-private-test'):
        # 调用接口
        res = self.create_api(url=ALI_GetAliSTS).json()
        # 获取参数
        api_resuil = get_api_result(res)
        # 定义变量
        AccessKeyId = api_resuil['AccessKeyId']
        AccessKeySecret = api_resuil['AccessKeySecret']
        SecurityToken = api_resuil['SecurityToken']
        # 上传excel到阿里云
        auth = oss2.StsAuth(AccessKeyId, AccessKeySecret, SecurityToken)
        bucket = oss2.Bucket(auth, region, bucketname)
        bucket.put_object_from_file(myObjectName, myLocalFile)
