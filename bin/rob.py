# coding=utf-8
import os
import sys, getopt
# from bin.init import func_init
from common.ReadAndWriteFiles import ReadAndWriteFiles
from common.ReadXML import ReadXML
from common.EmailSend import *


def main(argv):
    try:
        # 初始化方法，检查系统能否正常登录
        # func_init()
        #获取rob参数
        inputfile = ''
        outputfile = ''
        opt_p = ''
        opt_f = ''
        opt_d = ''
        opt_t = ''
        opt_tag = ''
        opt_email = ''
        opt_env = ''
        try:
            opts, args = getopt.getopt(argv, "hi:o:e:m:p:f:d:g:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print('获取参数异常')
            sys.exit(2)
        # 获取参数列表包括email，pybot，以及pybot的参数
        for opt, arg in opts:
            if opt == '-h':  # help，显示命令行格式
                print('te.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
            elif opt == "-e":  # 选择环境，可以使用test和auto
                opt_env = arg
            elif opt == "-m":  # 发送邮件，参数必须YES
                opt_email = arg
            elif opt == "-p":  # 选择解释器，可以使用pybot和robot
                opt_p = arg
            elif opt == "-f":  # 测试用例文件的目录
                opt_f = arg
            elif opt == "-d":  # 测试报告的目录
                opt_d = "-d " + arg
            # elif opt == "-t":  # 测试用例文件的目录
            #     opt_t = " -t " + arg
            elif opt == "-g":  # 测试用例tag
                opt_tag = "--include " + arg
            cmd = opt_p + " " + opt_d + " " + opt_tag + " " + opt_f + opt_t
            # 执行一整个项目（或测试用例集）ex，python rob.py -e test -m YES -p pybot -d ../report -f ../qutouwang/App/api  【设置环境】【发送邮件】
            # 执行一整个项目（或测试用例集）下面的某些个用例，ex,python rob.py -e test -p pybot -d ../report -t *2 ../qutouwang/App/api 【按测试用例名称执行】【已废弃】
            # 执行一整个项目，按照标签来执行，ex,python rob.py -e test -p pybot -d ../report -g Level1 -f ../qutouwang/App/api【按标签执行】
            #python rob.py -e test  -p pybot -d ../report -f ../qutouwang/App/api/登录相关  【设置环境
        #设置环境变量
        env = ["test","auto"]
        if opt_env not in env:
            raise Exception("字段-e 写入的参数值错误，请填写test或auto，test表示在测试环境进行测试，auto表示在自动化环境进行测试")

        rwf = ReadAndWriteFiles()
        rwf.update_resourse("Data","${data_env}","data_%senv"%opt_env)
        rwf.ini_write(rwf.pathenv,"environment","env",opt_env)

        print(cmd)
        os.system(cmd)
        if opt_email == "YES":
            print("发送邮件")
            # 在下面编写发送邮件的功能
            if opt_env == "test":
                send_mail("去投网2.0接口测试—测试环境")
            else:
                send_mail("去投网2.0接口测试—自动化环境")
    except Exception as msg:
        print("错误信息：%s"%msg)



if __name__ == "__main__":
    main(sys.argv[1:])
