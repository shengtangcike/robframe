#coding=utf-8
import time
import json
from xml.etree.ElementTree import parse
from common.ReadAndWriteFiles import ReadAndWriteFiles
# 解析XML
class ReadXML(object):
    def readx(self,path):
        '''
        :param path:
        :return: xml文件的测试结果
        '''
        rwf = ReadAndWriteFiles()
        print(rwf.pathreportxml)
        doc = parse(rwf.pathreportxml)
        # 获取根节点
        root = doc.getroot()

        # 获取根节点下面的下一节点
        # 初始化result的值
        result = {"base":{},"func":{}}
        list1 = []
        for data in root.findall('statistics'):
            for report in data.findall('suite'):
                for targets in report.findall('stat'):
                    if targets.attrib['id'].count("-") == 3:
                        if targets.attrib['id'][0:5] == "s1-s1":
                            if targets.attrib['fail'] == "0":
                                res_fail = 0
                                res_pass = 1
                            else:
                                res_fail = 1
                                res_pass = 0
                            result["func"][".".join(targets.text.split(".")[-2:])] = [res_pass, res_fail]
                        else:
                            if targets.attrib['fail'] == "0":
                                res_fail = 0
                                res_pass = 1
                            else:
                                res_fail = 1
                                res_pass = 0
                            result["base"][targets.text.split(".")[-1]] = [res_pass, res_fail]

        count_fail = 0
        count_pass = 0
        for k,v in result["base"].items():
            if v[0] == 1:
                count_pass += 1
            if v[1] == 1:
                count_fail += 1
        for k,v in result["func"].items():
            if v[0] == 1:
                count_pass += 1
            if v[1] == 1:
                count_fail += 1
        result["pass"] = count_pass
        result["fail"] = count_fail
        return result



    def report_error_txt(self):
        '''
        :return: report报告中所有发生错误txt的集合
        '''
        rwf = ReadAndWriteFiles()
        print(rwf.pathreportxml)
        doc = parse(rwf.pathreportxml)
        # 获取根节点
        root = doc.getroot()

        # 获取根节点下面的下一节点
        # 获取total的值
        list1 = []
        for data in root.findall('statistics'):
            for report in data.findall('suite'):
                for targets in report.findall('stat'):
                    if targets.attrib['id'].count("-") == 3 and targets.attrib['fail'] != "0":
                        list1.append(rwf.pathrob+"/qutouwang/"+targets.text.replace(".","/").replace("Api","api")+".txt")
                        # print(targets.text)
        return list1



if __name__=="__main__":
    ob= ReadXML()
    path = 'D:/PyWorkSpace/rob_frame/report/output.xml'
    res = ob.readx(path)
    print(res)

    # b = a.report_error_txt()
    # print(b)





