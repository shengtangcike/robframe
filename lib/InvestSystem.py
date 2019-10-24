#coding=utf-8
import json
import time,datetime
import requests
from common.ReadAndWriteFiles import ReadAndWriteFiles
from lib.BaseObject import BaseObject
from lib.MysqlDB import MysqlDB
rwf = ReadAndWriteFiles()
baseurl = rwf.ini_read(rwf.pathhosturl, "qwt_app_url")

class InvestSystem(BaseObject):

    def uploadheadImg(self,phone,password):
        '''
        :param phone:
        :param password:
        :return: 用户上传头像
        '''
        data = {}
        headers = {}
        self.login(phone,password)
        headers["accessToken"] = self.accessToken
        data["userId"] = self.userId
        req_url = baseurl + ("/api/personalCenter/uploadHeadImg")
        path1 = rwf.pathheading
        files = {"imgFile": ("test.png", open(path1, 'rb'))}
        result = self.reques.post(url=req_url, data=data, files=files, headers=headers)
        print(req_url)
        print(data)
        print(result.text)
        if '"code":0' in result.text:
            print("上传用户头像成功")
        else:
            raise Exception("上传用户头像失败")

    def read_resourse(self,code):
        '''
        :param code:
        :return: resourse.txt的查询信息
        '''
        code = rwf.read_resourse("resourse","${%s}"%code)
        return code

    def repaymentdebt(self,username,password,debtCode,num):
        '''
        :param username: 借款人账户
        :param password: 密码
        :param num: 还款期数
        :return:
        '''
        print("=====================借款人%s还款第%s期=======================" %(username,num))
        data1 = {"userId": "1122", "debtcode": debtCode, "termNum": num}
        data1 = json.dumps(data1)
        self.HttpApi("/api/loan/loanRepaymentShow","post",'{"Content-Type": "application/x-www-form-urlencoded"}',data1,username,password,'"code":0')
        print(self.r.text)
        res = json.loads(self.r.text)
        multiReturnSum = res["data"]["list"]["multiReturnSum"]
        print("第%s期的还款金额为%s" % (num, multiReturnSum))
        data2 = {"userId":"1122", "debtcode": debtCode, "termNum": num, "repaymentAmt": multiReturnSum}
        data2 = json.dumps(data2)
        self.HttpApi("/api/loan/loanRepaymentOperation", "post", '{"Content-Type": "application/x-www-form-urlencoded"}',data2, username, password, '"code":0')

    def earlyrepaymentoperation(self,username,password,debtCode):
        '''
        :param debtCode: 债权编号
        :return: 提前还款
        '''
        print("====================提前结清查询金额=========================")
        # 查询全部提前还款金额
        data1 = {"userId":"1122", "debtcode": debtCode}
        data1 = json.dumps(data1)
        self.HttpApi("/api/loan/earlyRepayment", "post", '{"Content-Type": "application/x-www-form-urlencoded"}',data1, username, password, '"code":0')
        tatalrepay = json.loads(self.r.text)["data"]["totalAmount"]
        print("全部提前还款总额%s" % tatalrepay)
        print("===================执行全部提前还款===================")
        data2 = {"userId":"1122", "debtcode": debtCode, "repaymentAmt": tatalrepay}
        data2 = json.dumps(data2)
        self.HttpApi("/api/loan/earlyRepaymentOperation", "post", '{"Content-Type": "application/x-www-form-urlencoded"}', data2,username, password, '"code":0')

    def changedebtplan(self,bidNocore):
        '''
        :param bidNocore: 标的编号
        :return: 更改放款时间和回款计划表
        '''
        #更改已满标的的放款时间，放款时间向前提前3个月2018-09-01
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        if now_month - 3 <= 0:
            month = str(12 + now_month - 3)
            if len(month) == 1:
                month = "0"+ month
            date0 = str(now_year-1)+"-"+month+"-"+"01"
        else:
            month = str(now_month-3)
            if len(month) == 1:
                month = "0"+ month
            date0 = str(now_year) + "-" + month + "-" + "01"

        if now_month - 2 <= 0:
            month = str(12 + now_month - 2)
            if len(month) == 1:
                month = "0"+ month
            date1 = str(now_year-1)+"-"+month+"-"+"01"
        else:
            month = str(now_month - 2)
            if len(month) == 1:
                month = "0"+ month
            date1 = str(now_year) + "-" + month + "-" + "01"

        if now_month - 1 <= 0:
            month = str(12 + now_month - 1)
            if len(month) == 1:
                month = "0"+ month
            date2 = str(now_year-1)+"-"+month+"-"+"01"
        else:
            month = str(now_month - 1)
            if len(month) == 1:
                month = "0"+ month
            date2 = str(now_year) + "-" + month + "-" + "01"
        if len(str(now_month)) == 1:
            month = "0" + str(now_month)
        else:
            month = str(now_month)
        date3 = str(now_year) + "-" + month + "-" + "01"
        #==============================
        if now_month + 1 > 12:
            month = str(now_month + 1 - 12)
            if len(month) == 1:
                month = "0"+ month
            date4 = str(now_year+1)+"-"+month+"-"+"01"
        else:
            month = str(now_month + 1)
            if len(month) == 1:
                month = "0"+ month
            date4 = str(now_year) + "-" + month + "-" + "01"

        if now_month + 2 > 12:
            month = str(now_month + 2 - 12)
            if len(month) == 1:
                month = "0"+ month
            date5 = str(now_year+1)+"-"+month+"-"+"01"
        else:
            month = str(now_month + 2)
            if len(month) == 1:
                month = "0"+ month
            date5 = str(now_year) + "-" + month + "-" + "01"
        if now_month + 3 > 12:
            month = str(now_month + 3 - 12)
            if len(month) == 1:
                month = "0"+ month
            date6 = str(now_year+1)+"-"+month+"-"+"01"
        else:
            month = str(now_month + 3)
            if len(month) == 1:
                month = "0"+ month
            date6 = str(now_year) + "-" + month + "-" + "01"


        #更改放款时间
        db = MysqlDB()
        db.sql_update('UPDATE qtw_invest_db.p2p_pact_issue SET fk_time = "%s" where pactissue_no = "%s"' % (date0,bidNocore))
        #更改还款计划
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 1' % (date1,bidNocore))
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 2' % (date2,bidNocore))
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 3' % (date3,bidNocore))
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 4' % (date4,bidNocore))
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 5' % (date5,bidNocore))
        db.sql_update('UPDATE qtw_invest_db.p2p_invest_return_plan SET open_date = "%s" where pactissue_no = "%s" AND term_num = 6' % (date6,bidNocore))
        time.sleep(20)

    def transferDebtapplyTransfer(self,username, password,bidNocore):
        '''
        :param username: 出借人账号
        :param password: 密码
        :param bidNocore: 标的编号
        :return: 申请债权转让
        '''
        db = MysqlDB()
        order_id = db.select_return_A_data('SELECT order_id FROM qtw_invest_db.p2p_invest_order WHERE pactissue_no = "%s"' % bidNocore)
        order_id = order_id[0]
        print("===================第一步，查询申请变现总额======================")
        data1 = {"userId": "1122", "orderId": order_id}
        data1 = json.dumps(data1)
        self.HttpApi("/api/transferDebt/investTranferDebtConfirm", "post", '{"Content-Type": "application/x-www-form-urlencoded"}',data1, username, password, '"code":0')
        rls = json.loads(self.r.text)
        # 申请债权转让的总额rePrincipal
        rePrincipal = rls["data"]["rePrincipal"]
        print("申请债权转让的总额%s" % rePrincipal)
        print("====================第二步，申请变现=========================")
        data2 = {"userId": "1122", "orderId": order_id}
        data2 = json.dumps(data2)
        self.HttpApi("/api/transferDebt/app/applyTransfer", "post",'{"Content-Type": "application/x-www-form-urlencoded"}', data2, username, password, '"code":0')
        print(self.r.text)
        time.sleep(10)
        return rePrincipal

    def transferDebtinvest(self,username, password,bidNocore,rePrincipal):
        '''
        :param username: 承接人账户
        :param password: 密码
        :param bidNocore: 标的编号
        :param rePrincipal: 出借金额
        :return: 承接人投资债权标
        '''
        print("====================第三步，承接人登录出借债转标,投满=========================")
        #通过标的编号查询出来债转标的主键
        #承接人登录
        db = MysqlDB()
        debt_id = db.select_return_A_data('SELECT debt_id FROM qtw_invest_db.p2p_loan_transfer WHERE pactissue_no = "%s"' % bidNocore)
        debt_id = debt_id[0]
        self.rwf = ReadAndWriteFiles()
        self.rwf.update_resourse("resourse", "${debt_id}", str(debt_id))
        self.rwf.update_resourse("resourse", "${bidNocore_debt_id}", str(bidNocore))
        data = {"userId": "1122", "bidId": debt_id,"investAmount":rePrincipal}
        data = json.dumps(data)
        self.HttpApi("/api/transferDebt/app/investProduct", "post", '{"Content-Type": "application/x-www-form-urlencoded"}', data, username, password, '"code":0')


if __name__=="__main__":
    username = "19800000013"
    password = "a1234567"
    bidNocore = "bd19073000005"
    rePrincipal = "5101.7"
    a = InvestSystem()
    # a.uploadheadImg(name,password)
    a.transferDebtinvest(username, password,bidNocore,rePrincipal)