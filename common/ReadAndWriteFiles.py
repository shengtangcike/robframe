#coding=utf-8
import os
import configparser as cparser

class ReadAndWriteFiles(object):
    def __init__(self):
        self.path_data()
        self.path_resourse()
        self.path_idcard()
        self.test_environment()
        self.path_mysql()
        self.path_redis()
        self.path_hosturl()
        self.path_headimg()
        self.path_report_xml()
        self.path_rob()
        self.path_loansysinto()
        self.path_report_email()

    def path_data(self):
        '''
        :return: 返回Data.txt的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/Data.txt')
        pathdata = config_file_path.replace("\\", "/")
        self.pathdata = pathdata
    def path_resourse(self):
        '''
        :return: 返回resourse.txt的绝对路径
        '''
        data_env = self.read_resourse("Data","${data_env}")
        current_path = os.path.abspath(__file__)
        pathresourse = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'qutouwang/'+data_env+'/resource.txt')
        pathresourse = pathresourse.replace("\\", "/")
        self.pathresourse = pathresourse

    def path_loansysinto(self):
        '''
        :return: 返回loansysinto.xlsx的绝对路径
        '''
        data_env = self.read_resourse("Data","${data_env}")
        current_path = os.path.abspath(__file__)
        pathloansysinto = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'qutouwang/'+data_env+'/loansysinto.xlsx')
        pathloansysinto = pathloansysinto.replace("\\", "/")
        self.pathloansysinto = pathloansysinto


    def path_idcard(self):
        '''
        :return: 返回districtcode.txt的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        idcard_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'common/districtcode.txt')
        idcard_path = idcard_path.replace("\\", "/")
        self.idcard_path = idcard_path
    def test_environment(self):
        '''
        :return: 返回环境变量
        '''
        current_path = os.path.abspath(__file__)
        pathenv = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/env.ini')
        pathenv = pathenv.replace("\\", "/")
        self.pathenv = pathenv
        cfa = cparser.ConfigParser()
        cfa.read(pathenv, encoding="utf-8-sig")
        self.env = cfa.get("environment", "env")

    def path_mysql(self):
        '''
        :return: 返回MysqlDB.ini的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/MysqlDB.ini')
        pathmysql = config_file_path.replace("\\", "/")
        self.pathmysql = pathmysql

    def path_redis(self):
        '''
        :return: 返回MysqlDB.ini的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/RedisDB.ini')
        pathredis = config_file_path.replace("\\", "/")
        self.pathredis = pathredis

    def path_headimg(self):
        '''
        :return: 返回HeadImg的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/HeadImg.png')
        pathheading = config_file_path.replace("\\", "/")
        self.pathheading = pathheading

    def path_hosturl(self):
        '''
        :return: 返回HostUrl.ini的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        config_file_path = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/HostUrl.ini')
        pathhosturl = config_file_path.replace("\\", "/")
        self.pathhosturl = pathhosturl
    def path_report_xml(self):
        '''
        :return: 返回HostUrl.ini的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        pathreportxml = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'report/output.xml')
        pathreportxml = pathreportxml.replace("\\", "/")
        self.pathreportxml = pathreportxml
    def path_report_email(self):
        '''
        :return: 返回email.ini绝对路径
        '''
        current_path = os.path.abspath(__file__)
        pathemailini = os.path.join(os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".."),'config_file/Email.ini')
        pathemailini = pathemailini.replace("\\", "/")
        self.pathemailini = pathemailini

    def path_rob(self):
        '''
        :return: 返回HostUrl.ini的绝对路径
        '''
        current_path = os.path.abspath(__file__)
        pathrob = os.path.abspath(os.path.dirname(current_path) + os.path.sep + "..")
        pathrob = pathrob.replace("\\", "/")
        self.pathrob = pathrob

    def read_resourse(self,path, par):
        '''
        :param path: 选择要读取的文件，传参Data读取Data.txt文件//传参resourse读取resourse.txt文件
        :param par: 选择要读取的内容，ex."${data_env}"
        :return:
        '''
        if path == "Data":
            path_res = self.pathdata
        elif path == "resourse":
            path_res = self.pathresourse
        else:
            print("请选择要查询的文件，查询Data.txt文件path参数传入【Data】，查询resourse.txt文件path参数传入【resourse】")
            path_res = None
        # 读取文件
        f1 = open(path_res, "r", encoding="utf-8")
        datas = f1.readlines()
        value = ""
        for i in range(len(datas)):
            datas[i] = datas[i].split("    ")
            if datas[i][0] == par:
                value = datas[i][-1]
                break
        f1.close()
        value = value.replace("\n", "")
        return value

    #更新resourse的值
    def update_resourse(self,path,par,value):
        '''
        param value: 选择要读取的文件，传参Data读取Data.txt文件//传参resourse读取resourse.txt文件
        :param par: 选择要写入的内容，ex."${data_env}"
        :param value: 写入的值
        :return:
        '''
        if path == "Data":
            path_res = self.pathdata
        elif path == "resourse":
            path_res = self.pathresourse
        else:
            print("请选择要查询的文件，查询Data.txt文件path参数传入【Data】，查询resourse.txt文件path参数传入【resourse】")
            path_res = None
        f1 = open(path_res,"r",encoding="utf-8")
        datas = f1.readlines()
        #读取文件
        for i in range(len(datas)):
            datas[i] = datas[i].split("    ")
            if datas[i][0] == par:
                datas[i][-1] = value + "\n"
            datas[i] = "    ".join(datas[i])
        f1.close()
        #重新写入
        datas = "".join(datas)
        f2 = open(path_res,"w",encoding="utf-8")
        f2.write(datas)
        f2.close()

    def ini_read(self,filepath,value):
        '''
        :param filepath: 加载文件地址
        :param value: 读取的键
        :return: 对应键的值
        '''
        cfb = cparser.ConfigParser()
        cfb.read(filepath, encoding="utf-8-sig")
        v = cfb.get(self.env, value)
        return v
    def ini_write(self,filepath,section,key,value):
        '''
        :param filepath: 加载文件地址
        :param value: 读取的键
        :return: 对应键的值
        '''
        cfb = cparser.ConfigParser()
        cfb.read(filepath, encoding="utf-8-sig")
        cfb.set(section,key,value)
        cfb.write(open(filepath, "r+"))



if __name__=="__main__":
    # update_resourse("${ord}","222")
    a = ReadAndWriteFiles()
    # print(a.pathdata)
    # print(a.pathresourse)
    print(a.idcard_path)
    # print(a.env)
    # print(a.pathmysql)
    # b = a.ini_read(a.pathmysql,"mysql_host")
    # print(b)
    # print(a.read_resourse("Data","${data_env}"))
    # print(a.read_resourse("resourse","${Newphone1_aes}"))
    # print(a.update_resourse("${Newphone1_aes}","1222"))
    # a.ini_write(a.pathenv, "environment", "env", "auto")