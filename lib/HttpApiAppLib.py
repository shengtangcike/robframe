#coding=utf-8
import requests
import time
import re
from lib.BaseObject import BaseObject
from common.aes import PrpCrypt
from common.createIdcard import CreateIdCard
from common.ReadAndWriteFiles import ReadAndWriteFiles

class HttpApiLib(BaseObject):

    def regular(self,regex, content, index=1):
        regex = str(regex)
        content = str(content)
        '''
        :param regex: ex,正则表达式,ex,验证码：(.+?)，
        :param content: 字符串
        :param index:
        :return: 根据正则表达式的值提取的内容
        '''
        search_result = '0'
        search = re.compile(regex)
        message = search.search(content)
        if message:
            search_result = message.group(index)
        return search_result

    def phone_aes(self,phone):
        '''
        :param phone:
        :return: 加密后的手机号
        '''
        pc = PrpCrypt('hqtw-%s'%phone)  # 初始化密钥
        phone_aes = pc.encrypt("%s"%phone)  # 加密
        return phone_aes
    def password_aes(self,phone,passwoed):
        '''
        :param phone:
        :param passwoed:
        :return: 加密后的密码
        '''
        print(phone,passwoed)
        pc = PrpCrypt('hqtw-%s' % phone)  # 初始化密钥
        password_aes = pc.encrypt("%s" % passwoed)  # 加密
        return password_aes

    def phone_time(self):
        '''
        :return: 生成类手机号字符串
        '''
        pt = str(time.time())
        pt = pt.split(".")
        phone_time = pt[0] + pt[1][0]
        print(phone_time)
        return phone_time

    def createid(self):
        '''
        :return: 按照规则生成的身份证号码
        '''
        CIC = CreateIdCard()
        idcard = CIC.gennerator()
        return idcard
    def update_resourse_orderidzx(self,par1):
        '''
        :return: 更新resourse.txt中${order_id_zx}的值
        '''
        self.rwf = ReadAndWriteFiles()
        self.rwf.update_resourse("resourse","${order_id_zx}", par1)


    def assert_invest(self):
        print(self.r.text)


    def tesx(self):
        self.tx = 1111
        return self.tx

    def tesy(self):
        print(self.tx)


if __name__=="__main__":
    # path = "/api/userRegister/checkPhone"
    # method = "post"
    # header = '{"Content-Type": "application/x-www-form-urlencoded"}'
    # data = '{"userId": "9"}'
    # username = "None"
    # password = "None"
    # exception = "查询成功"
    a = HttpApiLib()
    print(a.password_aes("15600000004","a1234567"))
    # a.HttpApi(path,method,header,data,username,password,exception)

