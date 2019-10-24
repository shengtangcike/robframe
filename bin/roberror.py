# coding=utf-8
import os
import sys, getopt
from common.ReadXML import ReadXML
from common.ReadAndWriteFiles import ReadAndWriteFiles

def roberror():
    rx = ReadXML()
    list1 = rx.report_error_txt()
    print(list1 == [])
    if list1 == []:
        print("report目录下面的报告中没有报错的文件，所以不需要执行")
    else:
        rwf = ReadAndWriteFiles()
        cmd = "pybot -d %s/reporterror"%rwf.pathrob
        for i in list1:
            cmd = cmd + " " + i
        print(cmd)
        os.system(cmd)


if __name__ == "__main__":
    roberror()
