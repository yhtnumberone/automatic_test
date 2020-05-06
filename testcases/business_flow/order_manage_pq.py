#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from common.lib.comm_func.orders import Order
from common.lib.pip_install import unittest
from common.lib.venv.var import send_boss_user,agentName
from common.lib.module_tools.analyze_result import get_api_result

class OrderFlow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ordermanage = Order()
        cls.ordermanage.login(send_boss_user)

    def test_create_order_flow(self):
        """
        1、创建五个工种不一样的订单
        2、审核订单
        3、分配订单
        """
        entborrows = ['淳华工种1','郑鹏工种1','复扬工种1','建大工种1','明基工种1']
        # 创建订单
        for entborrow in entborrows:
            self.ordermanage.create_order_pq(entbrorrowname=entborrow,ReceiverType=2,PriceUnit=1)

        #查询订单
        get_order_res = self.ordermanage.get_orders(CreatedBy=self.ordermanage.zt_guid,OrderStatus=1)

        # 审核订单
        orderids = get_api_result(get_order_res,'RcrtMainOrderId')
        print(orderids)
        for orderid in orderids:
            self.ordermanage.Judge_Order(auditsts=2,orderid=orderid)

        # 获取供应商
        self.ordermanage.get_agent(agentname=agentName)

        # 订单分配供应商
        for orderid in orderids:
            self.ordermanage.order_allocation_pq(agentname=agentName,OrderId=orderid)


if __name__=='__main__':
    unittest.main()