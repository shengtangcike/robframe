import redis
from common.ReadAndWriteFiles import ReadAndWriteFiles

class RedisDB(object):
    '''
    python操作redis，删除库中的相关主键
    在qtw测试环境中使用redis集群主从结构，测试环境主是192.168.1.76:6379/26379
    pip install redis
    '''
    def initRD(self, conf_redis="qtw_Redis"):
        # ===========读取RedisDB.ini文件===========
        rwf = ReadAndWriteFiles()

        self.host = rwf.ini_read(rwf.pathredis, "redis_host")
        self.port = int(rwf.ini_read(rwf.pathredis, "redis_port"))

        # host是redis主机，需要redis服务端和客户端都启动 redis默认端口是6379
        self.red = redis.Redis(host=self.host, port=self.port, decode_responses=True)


    def delete_redis_register_phone_sms(self,phone):
        '''
        :return: 删除注册手机号发送短信验证码的次数的键
        '''
        self.initRD()
        phoneslist = self.red.keys(pattern='registCount*%s' % phone)
        print(phoneslist)  # 所有的registCount++phoned的全删，比较暴力
        for phone in phoneslist:
            self.red.delete(phone)

    def delete_redis_password_phone_sms(self,phone):
        '''
        :return: 删除忘记密码手机号发送短信验证码的次数的键
        '''
        self.initRD()
        phoneslist = self.red.keys(pattern='PasswordCount*%s' % phone)
        print(phoneslist)  # 所有的registCount++phoned的全删，比较暴力
        for phone in phoneslist:
            self.red.delete(phone)
    def delete_redis_loginerror_num(self,phone):
        '''
        :return: 删除登录错误次数的键
        '''
        self.initRD()
        phoneslist1 = self.red.keys(pattern='dayLoginError*%s' % phone)
        phoneslist2 = self.red.keys(pattern='loginError*%s' % phone)
        print(phoneslist1)  # dayLoginError++phoned的全删，比较暴力
        print(phoneslist2)  # loginError++phoned的全删，比较暴力
        for phone in phoneslist1:
            self.red.delete(phone)
        for phone in phoneslist2:
            self.red.delete(phone)
    def delete_redis_recharge(self,userid):
        '''
        :return: 删除充值超限的键
        '''
        self.initRD()
        phoneslist1 = self.red.keys(pattern='*%s*' % userid)
        print(phoneslist1)  # dayLoginError++phoned的全删，比较暴力
        for phone in phoneslist1:
            self.red.delete(phone)
    def read_redis_con(self):
        self.initRD()
        a = self.red.get('register_15600000003')
        print(a)
    def delete_redis_phone_update(self,userid):
        '''
        :return: 删除修改手机号的键
        '''
        self.initRD()
        phoneslist1 = self.red.keys(pattern='updateCheckPhoneCount*%s' % userid)
        print(phoneslist1)  # dayLoginError++phoned的全删，比较暴力
        for phone in phoneslist1:
            self.red.delete(phone)
        phoneslist2 = self.red.keys(pattern='updatePhoneCount*%s' % userid)
        print(phoneslist2)  # dayLoginError++phoned的全删，比较暴力
        for phone in phoneslist2:
            self.red.delete(phone)


if __name__=="__main__":
    phone = "15600000001"        #短信发送次数超限的手机号
    a = RedisDB()
    # a.delete_redis_register_phone_sms(phone)
    # a.delete_redis_loginerror_num(phone)
    # a.delete_redis_recharge("19061520965475")
    a.read_redis_con()
