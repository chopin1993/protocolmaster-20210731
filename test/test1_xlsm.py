import xlrd
from xlrd import xldate_as_tuple
import datetime

workbook = xlrd.open_workbook(r'G:\ProtocolMaster\source\resource\数据标识分类表格.xls')
sheet = workbook.sheets()[0]

def print_sheet(sheet):
  for rown in range(5,sheet.nrows):
     print(sheet.cell_value(rown, 1),
           sheet.cell_value(rown, 2),
           sheet.cell_value(rown, 5),
           sheet.cell_value(rown, 6),
           sheet.cell_value(rown, 7),
           sheet.cell_value(rown, 8))



if __name__ == '__main__':
  print_sheet(sheet)