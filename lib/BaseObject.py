#coding=utf-8
import requests
import json
from common.aes import *
from common.ReadAndWriteFiles import ReadAndWriteFiles


class BaseObject(object):
    def __init__(self):
        self.reques = requests.Session()
        rwf = ReadAndWriteFiles()
        self.urlbase = rwf.ini_read(rwf.pathhosturl, "qwt_app_url")
    def HttpApi(self,path,method,headers,data,username,password,exception):
        '''
        :param path:
        :param method:
        :param headers:
        :param data:
        :param username:
        :param password:
        :param exception:
        :return:
        '''
        self.path = path                 #请求路径
        self.method = method             #请求方法
        self.headers = headers             #请求头信息
        self.data = data                 #请求信息
        self.username = username         #用户名
        self.password = password         #密码
        self.exception = exception       #期望断言

        # self.reques = requests.Session()

        #处理headers
        if "dict" not in str(self.headers.__class__):
            self.headers = json.loads(self.headers)
        else:
            self.headers = self.headers

        #处理data
        if self.data == "None":
            self.data = None
        else:
            if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
                self.data = json.loads(self.data)
            if self.headers["Content-Type"] == "application/json":
                pass

        #登录系统
        if self.username != "None":
            self.login(self.username,self.password)
            self.headers["accessToken"] = self.accessToken
            if self.headers["Content-Type"] == "application/x-www-form-urlencoded":
                self.data["userId"] = self.userId

        #执行测试
        print("==================执行测试=====================")
        print(self.urlbase+self.path)
        print(self.data)
        print(self.headers)
        r = self.reques.post(url=self.urlbase+self.path, data=self.data, headers=self.headers)
        self.r = r
        print(r.status_code)
        print("期望值：",self.exception)
        print("实际值",r.text)
        if self.exception in r.text:
            pass
        else:
            raise Exception("实际结果：%s，不符合期望的值：%s"%(r.text,self.exception))


    def login(self,username,password):
        '''
        登录系统
        '''
        pc = PrpCrypt('hqtw-' + username)  # 初始化密钥
        password = pc.encrypt(password)  # 新密码加密后的密码
        login_data = {}
        login_data["account"] = username
        login_data["password"] = password
        print(login_data)
        print("================"+login_data["account"]+"账户登录================")
        login_header = {"Content-Type": "application/x-www-form-urlencoded"}
        print(self.urlbase+"/api/userAuth/login")
        rslt = self.reques.post(url=self.urlbase+"/api/userAuth/login",data = login_data,headers=login_header)
        rslt = json.loads(rslt.text)
        print(rslt)
        self.accessToken = rslt["data"]["access_token"]
        print(self.accessToken)
        self.userId = rslt["data"]["userId"]



if __name__=="__main__":
    path = "/api/risk/saveRisk"
    method = "post"
    header = '{"Content-Type": "application/json"}'
    data = '{"userId":"9","totalScore":48,"questions":[{"question":{"value":"1-3","score":3}},{"question":{"value":"2-1","score":1}},{"question":{"value":"3-2","score":2}},{"question":{"value":"4-4","score":4}},{"question":{"value":"5-3","score":3}},{"question":{"value":"6-1","score":1}},{"question":{"value":"7-4","score":4}},{"question":{"value":"8-4","score":4}},{"question":{"value":"9-4","score":4}},{"question":{"value":"10-5","score":5}},{"question":{"value":"11-4","score":4}},{"question":{"value":"12-5","score":5}},{"question":{"value":"13-4","score":4}},{"question":{"value":"14-4","score":4}}]}'
    username = "15600000001"
    password = "a1234567"
    exception = "查询成功"
    a = BaseObject()
    a.HttpApi(path,method,header,data,username,password,exception)
