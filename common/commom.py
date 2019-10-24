import xlrd
import re

def str_cmp(str1, str2):
    cmp_result = bool(re.fullmatch(str1, str2, re.IGNORECASE))
    return cmp_result

class ReadExcel(object):
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.table = self.load_excel()
        self.ncols = self.table.ncols
        self.nrows = self.table.nrows

    def load_excel(self):
        try:
            data = xlrd.open_workbook(self.file_path)
            table = data.sheet_by_name(self.sheet_name)
            return table
        except Exception as e:
            print(u"读表格错误")
            print(e)

    def get_col_number(self, row_number, row_name):
        # 表头名字为row_name的第row_number行，所对应的列
        for i in range(self.ncols):
            if str_cmp(self.table.row_values(row_number)[i], row_name):
                return i

    def get_value(self, row_number, row_name):
        # 表头名字为row_name的第row_number行，获得这一列
        try:
            head_number = self.get_col_number(0, row_name)
            value = self.table.col_values(head_number)[row_number]
            return value
        except Exception as e:
            print("getCellData(%s,%s)" % (row_number, row_name))
            print(e)

    def for_test(self, number):
        url = (configHttp.http(self.get_value(number, u"协议"), self.sheet_name)+self.get_value(number, u"请求URL"))
        data_list = [url,
                     self.get_value(number, u"参数"),
                     self.get_value(number, u"请求头"),
                     self.get_value(number, "数据格式")]
        return data_list

    def request_test(self, i, *par, **headers):
        default_header = eval(self.for_test(i)[2])
        print(headers, default_header)
        if len(headers) > 0:
            default_header.update(headers)
        header = default_header
        # else:
        #     header = default_header
        data = self.for_test(i)[1] % par
        print(self.for_test(i)[0], data, header)
        return RequestMethod(self.for_test(i)[0],
                             data,
                             header,
                             self.for_test(i)[3])