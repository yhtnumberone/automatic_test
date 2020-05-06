from common.lib.venv.var import *
from common.lib.pip_install.openpyxl import Workbook,load_workbook


def edit_exc(t1,t2,t3,t4,t5,t7,t6=None,t8=None):
    wb = None
    try:
        if not os.path.exists(myLocalFile_advance):
            wb = Workbook()
            ws = wb.create_sheet('Sheet1')
        else:
            wb = load_workbook(myLocalFile_advance)
            ws = wb['Sheet1']
        value1 = ['姓名','身份证号码','工号','入职日期','在职状态','离职/转正/自离日期','上班天数','备注']
        value2 = [t1,t2,t3,t4,t5,t6,t7,t8]
        for i in range(1,9):
            ws.cell(1, i).value = value1[i-1]
        for i in range(1,9):
            ws.cell(2, i).value = value2[i-1]
    finally:
        if wb:
            wb.save(myLocalFile_advance)


def edit_exctwo(t1,t2,t3,t4,t5,t6,t9,t7=None,t8=None):
    wb = None
    try:
        if not os.path.exists(myLocalFile_month):
            wb = Workbook()
            ws = wb.create_sheet('Sheet1')
        else:
            wb = load_workbook(myLocalFile_month)
            ws = wb['Sheet1']
        value1 = ['姓名','身份证号码','工号','实发工资','入职日期','在职状态','离职/转正/自离日期','备注','出勤小时数']
        value2 = [t1,t2,t3,t4,t5,t6,t7,t8,t9]
        for i in range(1,9):
            ws.cell(1, i).value = value1[i-1]
        for i in range(1,9):
            ws.cell(2, i).value = value2[i-1]
    finally:
        if wb:
            wb.save(myLocalFile_month)


