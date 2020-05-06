#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : analyze_result.py
# @Author   : yht
# @Date     : 2019/12/24
# @Desc     : 公共方法



def get_api_result(result_, *args):
    """
    拆分接口返回参数
    :param query_result:
    :param args:
    :return:
    """
    data = result_['Data']
    if not args:
        return data
    else:
        for key, value in data.items():
            if isinstance(value, list):
                res = data[key]
                count = len(res)
                key_list = []
                if isinstance(args[0], int):
                    return res[args[0]]
                else:
                    for k in (args):
                        for i in range(count):
                            r = res[i][k]
                            key_list.append(r)
                    # key_list.sort()
                return key_list
