import requests
import json
from common.aes import *
def func_init():
    '''初始化程序，如果系统不能登录，程序不再进行'''
    #=========================资金借款人登录=============================
    theborrower = requests.Session()    #借款人session
    phone16 = "19900000001"
    phone16_psw = "1234abcd"
    url_login = str(load_ini("qwt_test", "qwt_app_url") + "/api/userAuth/login")
    pc = PrpCrypt('hqtw-' + phone16)  # 初始化密钥
    phone16_aes = pc.encrypt(phone16_psw)  # 新密码
    theborrower_header = {"Content-Type": "application/x-www-form-urlencoded"}
    login = {"account": phone16, "password": phone16_aes}
    rslt = theborrower.post(url_login, data=login, headers=theborrower_header)
    # print(rslt.text)
    theborrower_userId = json.loads(rslt.text)["data_testenv"]["userId"]
    theborrower_header["accessToken"] = json.loads(rslt.text)["data_testenv"]["access_token"]
    # print(theborrower_userId)
    # print(theborrower_header)
    # print(rslt.text)
    if '"code":0' in rslt.text:
        print("资金借款人登录成功")
    else:
        print("资金借款人登录失败")
        raise Exception("Pc登录失败")
    #=========================资金出借人登录==============================
    thelender = requests.Session()    #出借人session
    phone15 = "19900000002"
    phone15_psw = "1234abcd"
    url_login = str(load_ini("qwt_test", "qwt_app_url") + "/api/userAuth/login")
    pc = PrpCrypt('hqtw-' + phone15)  # 初始化密钥
    phone15_aes = pc.encrypt(phone15_psw)  # 新密码
    thelender_header = {"Content-Type": "application/x-www-form-urlencoded"}
    login = {"account": phone15, "password": phone15_aes}
    rslt = thelender.post(url_login, data=login, headers=thelender_header)
    thelender_userId = json.loads(rslt.text)["data_testenv"]["userId"]
    thelender_header["accessToken"] = json.loads(rslt.text)["data_testenv"]["access_token"]
    # print(thelender_userId)
    # print(thelender_header)
    # print(rslt.text)
    if '"code":0' in rslt.text:
        print("资金出借人登录成功")
    else:
        print("资金出借人登录失败")
        raise Exception("Pc登录失败")
    #=========================资金承接人登录==============================
    thelrecipient = requests.Session()    #承接人session
    phone14 = "19900000003"
    phone14_psw = "1234abcd"
    url_login = str(load_ini("qwt_test", "qwt_app_url") + "/api/userAuth/login")
    pc = PrpCrypt('hqtw-' + phone14)  # 初始化密钥
    phone14_aes = pc.encrypt(phone14_psw)  # 新密码
    thelrecipient_header = {"Content-Type": "application/x-www-form-urlencoded"}
    login = {"account": phone14, "password": phone14_aes}
    rslt = thelrecipient.post(url_login, data=login, headers=thelrecipient_header)
    thelrecipient_userId = json.loads(rslt.text)["data_testenv"]["userId"]
    thelrecipient_header["accessToken"] = json.loads(rslt.text)["data_testenv"]["access_token"]
    # print(thelrecipient_userId)
    # print(thelrecipient_header)
    # print(rslt.text)
    if '"code":0' in rslt.text:
        print("资金承接人登录成功")
    else:
        print("资金承接人登录失败")
        raise Exception("Pc登录失败")
    # =========================垫付机构登录==============================
    thepaymentphone = requests.Session()  # 借款人session
    phone17 = "19900000004"
    phone17_psw = "1234abcd"
    url_login = str(load_ini("qwt_test", "qwt_app_url") + "/api/userAuth/login")
    pc = PrpCrypt('hqtw-' + phone17)  # 初始化密钥
    phone17_aes = pc.encrypt(phone17_psw)  # 新密码
    thepaymentphone_header = {"Content-Type": "application/x-www-form-urlencoded"}
    login = {"account": phone17, "password": phone17_aes}
    rslt = thepaymentphone.post(url_login, data=login, headers=thepaymentphone_header)
    thepaymentphone_userId = json.loads(rslt.text)["data_testenv"]["userId"]
    thepaymentphone_header["accessToken"] = json.loads(rslt.text)["data_testenv"]["access_token"]
    # print(thepaymentphone_userId)
    # print(thepaymentphone_header)
    # print(rslt.text)
    if '"code":0' in rslt.text:
        print("垫付机构登录成功")
    else:
        print("垫付机构登录失败")
        raise Exception("Pc登录失败")
    # #=========================资产系统登录================================
    # assets = requests.Session()
    # url_login = str(load_ini("qwt_test", "qwt_asset_url") + "/operate/user/login")
    # headers = {"Content-Type": "application/x-www-form-urlencoded"}
    # data_testenv = {"account": "admin", "password": "123456", "system": ""}
    # rslt = assets.post(url_login, data_testenv=data_testenv, headers=headers)
    # # print(rslt.text)
    # if '"errorCode":0' in rslt.text:
    #     print("资产系统登录成功")
    # else:
    #     print("资产系统登录失败")
    #     raise Exception("资产登录失败")
    #=========================借贷系统登录================================
    loan = requests.Session()
    url_deb = str(load_ini("qwt_test", "qwt_loan_url") + "/operate/user/login")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"account": "admin", "password": "123456", "system": ""}
    resl = loan.post(url_deb, data=data, headers=headers)
    # print(resl.text)
    if '"errorCode":0' in resl.text:
        print("借贷系统登录成功")
    else:
        print("借贷系统登录失败")
        raise Exception("资产登录失败")
    #=========================核心系统登录================================
    core = requests.Session()
    url1 = str(load_ini("qwt_test", "qwt_core_url") + "/random")
    data1 = {"cacheid": "0.49101218522027756"}
    header1 = {"Content-Type": "application/json"}
    core.get(url1,params=data1,headers=header1)
    url2 = str(load_ini("qwt_test", "qwt_core_url") + "/rest/user/back/accountLogin")
    data2 = {'callback': 'jQuery17209220007142597262_1541401333724', 'jsonParams': ''
    '{"method":"login","params":{"userAccount":"sysadmin","password":"123abc","randnumber":'
    '"0000","randnumKey":"0.49101218522027756","autoLogin":"FALSE","serviceUrl":null}}', '_': '1541401341903'}
    resl = core.get(url2, params=data2, headers=header1)
    # print(resl.text)
    if 'SUCCESS' in resl.text:
        print("核心系统登录成功")
    else:
        print("核心系统登录失败")
        raise Exception("资产登录失败")

if __name__=="__main__":
    func_init()

