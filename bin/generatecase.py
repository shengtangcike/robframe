#coding=utf-8
import os
import xlrd

class Generatecase(object):
    def __init__(self, file_path,sheetname):
        '''
        :param file_path: excel文件
        :param sheetname: sheet名称
        '''
        self.file_path = file_path
        self.sheetname = sheetname
        current_path = os.path.abspath(__file__)
        father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..").replace("\\","/")
        self.rob_path = father_path+"/"+file_path.split("/")[-1][:-5].replace(".","/")
        print(self.rob_path)
        self.mkdir(self.rob_path)
        self.load_excel()
        self.for_list()
    def mkdir(self,path):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("---创建新文件夹---")
        else:
            print("---文件夹已存在不需要创建---")

    def load_excel(self):
        try:
            self.data = xlrd.open_workbook(self.file_path)
            self.sheet_list = self.data.sheet_names()
        except Exception as e:
            print(u"读表格错误")
            print(e)
    def for_list(self):
        '''
        生成robot的文件
        '''
        for name in self.sheet_list:
            if name == self.sheetname:
                self.table = self.data.sheet_by_name(name)
                self.nrows = self.table.nrows
                # print(self.rob_path+"/"+name+'.txt')
                #如果文件存在就先删除，防止重复生成用例
                if os.path.exists(self.rob_path+"/"+name+'.txt'):
                    # os.remove(self.rob_path+"/"+name+'.txt')
                    print("测试文件：===》"+name+".txt《===已存在，如果要重新创建请先删除原文件")
                else:
                    f = open(self.rob_path+"/"+name+'.txt',"a",encoding="UTF-8")
                    for i in range(1,self.nrows):
                        if i ==1:
                            f.write("*** Settings ***\nResource     ../../../../config_file/Data.txt\nResource     ../../../${data_env}/resource.txt\nResource     ../../../keyword/keyword.txt\nLibrary    lib\nTest Template     HttpApi\nSuite Setup     \n\n*** Test Cases ***\n" )
                        f.write("case%s\n    [Documentation]    %s\n    [Tags]    %s\n"%(i,self.table.row_values(i)[1],self.table.row_values(i)[9]))
                        f.write("    %s    %s    %s    %s"%(self.table.row_values(i)[2],self.table.row_values(i)[3],self.table.row_values(i)[4],self.table.row_values(i)[5]))
                        f.write("    %s    %s    %s\n"%(self.table.row_values(i)[6],self.table.row_values(i)[7],self.table.row_values(i)[8]))
                    f.close()


if __name__=="__main__":
    path = "D:/PyWorkSpace/rob_frame/qutouwang/testcase/qutouwang.App.api.登录相关.xlsx"
    sheetname = "授权金额期限字段展示"
    a = Generatecase(path,sheetname)


