import unittest
# from testcases.send_money.settlement_center.send_money_import import SendMoneyImport
from testcases.labor_template_pq.namelist_management.real_record import Real_record
from common.lib.venv.var import *
import logging
from common.lib.pip_install.BeautifulReport import BeautifulReport

if __name__ == '__main__':
    # unittest.main()
    logging.basicConfig(filename=log_name, level=logging.DEBUG)
    # test1 = [SendMoneyImport('test_get_entlist'),SendMoneyImport('test_get_excel_import'),SendMoneyImport('test_preview_import_success'),SendMoneyImport('test_preview_import_empty')]
    test1 = [Real_record('test_record_manually'), Real_record('test_set_who_give_me'), Real_record('test_set_intsts'),
             Real_record('test_get_namelist')]
    suite = unittest.TestSuite()
    suite.addTests(test1)
    BeautifulReport(suite).report(filename=report_name, description='test', log_path=report_path)