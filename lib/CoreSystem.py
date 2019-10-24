# coding=utf-8
import requests
import time
import re
from common.ReadAndWriteFiles import ReadAndWriteFiles
from lib.MysqlDB import MysqlDB


class CoreSystem(object):
    '''
    去投网核心系统基本功能
    '''

    def coresyslogin(self):
        '''
        :return: 核心系统登录session
        '''
        print("核心系统登录")
        self.rwf = ReadAndWriteFiles()
        self.coreurlbase = self.rwf.ini_read(self.rwf.pathhosturl, "qwt_core_url")
        self.core = requests.Session()
        url1 = self.coreurlbase + "/random"
        data1 = {"cacheid": "0.49101218522027756"}
        header1 = {"Content-Type": "application/json"}
        self.core.get(url1, params=data1, headers=header1)
        url2 = self.coreurlbase + "/rest/user/back/accountLogin"
        data2 = {'callback': 'jQuery17209220007142597262_1541401333724', 'jsonParams': ''
                                                                                       '{"method":"login","params":{"userAccount":"sysadmin","password":"123abc","randnumber":'
                                                                                       '"0000","randnumKey":"0.49101218522027756","autoLogin":"FALSE","serviceUrl":null}}',
                 '_': '1541401341903'}
        resl = self.core.get(url2, params=data2, headers=header1)
        print(resl.text)

    def querydebtId(self, debtCode, type=None):
        '''
        :param debtCode: 债权编号
        :return: 债权的主键
        '''
        url3 = self.coreurlbase + "/rest/debt/queryAll"
        data3 = {'t': '1541756027711\n', 'callback': 'jQuery172011043902518311977_1541756012872\n',
                 'jsonParams': '{"method":"queryAll","params":{"page":{"conditions":"{\\"debtCode\\":\\"%s\\"}","pageNum":1,"pageSize":10}}}\n' % debtCode,
                 '_': '1541756027711'}
        header1 = {"Content-Type": "application/json"}
        resl = self.core.get(url3, params=data3, headers=header1)
        # print(resl.text)
        if "SUCCESS" in resl.text:
            pass
        else:
            raise Exception("借款端推送债权到核心失败")
        print(resl.text)
        debtIdcore = self.regular('"debtId":(.+?),', resl.text, 1)
        if type == "True":
            self.rwf.update_resourse("resourse", "${debtIdcore_zx}", debtIdcore)
        else:
            self.rwf.update_resourse("resourse", "${debtIdcore}", debtIdcore)
        print("债权主键为%s" % debtIdcore)

    def corecheckandfabiao(self, debtIdcore):
        '''
        :param debtIdcore: 债权主键
        :return: 发标
        '''
        print("创建散标=================")
        url3 = self.coreurlbase + "/rest/debt/batchCreate"
        data3 = {'_': '1543739780142', 't': '1543739780141\n', 'jsonParams': '{"method":'
                                                                             '"batchCreate","params":{"debtIds":"%s","type":"submit","param":"{\\"box\\":\\'
                                                                             '"52600043652\\",\\"effectTime\\":\\"5\\",\\"effectTimeUnit\\":\\"d\\",\\"minAmount'
                                                                             '\\":\\"100\\",\\"incrementalAmt\\":\\"100\\",\\"pubTime\\":\\"2018-12-02 16:36:05\\"}"}}\n' % debtIdcore,
                 'callback': 'jQuery172024506418937789642_1543739601832\n'}
        header1 = {"Content-Type": "application/json"}
        res2 = self.core.get(url3, params=data3, headers=header1)
        print(res2.text)
        print("=====================审核散标并发标========================")
        # 通过债权主键debtIdcore，查询标的的主键bidcore和标的的编号bidNocore
        db = MysqlDB()
        script = "select id,bidNo from qtw_core_db.core_product_scattered where debtId=%s" % debtIdcore
        result = db.select_return_A_data(script)
        self.rwf.update_resourse("resourse", "${bidcore}", str(result[0]))
        self.rwf.update_resourse("resourse", "${bidNocore}", str(result[1]))
        print("债权对应的标的主键", result[0])
        print("标的的编号", result[1])
        # ===============
        url4 = self.coreurlbase + "/rest/standardProd/batchApprovalSubmit"
        print(url4)
        data4 = {'t': '1542696230010\n', '_': '1542696230011',
                 'jsonParams': '{"method":"batchApprovalSubmit","params":{"debtIds":%s,"param":"{\\"bidId\\":\\"20000024408\\",\\"approval\\":\\"1\\"}"}}\n' %
                               result[0], 'callback': 'jQuery17206732644502681546_1542694420296\n'}
        res2 = self.core.get(url4, params=data4, headers=header1)
        print(res2.text)
        if "SUCCESS" in res2.text:
            print("核心发标成功")
        else:
            raise Exception("核心发标失败")
        time.sleep(5)

    def corereturnedmoney(self, debtCode, term_num):
        '''
        :param debtCode: 债权
        :param term_num: 回款期数
        :return: 回款
        '''
        db = MysqlDB()
        should_date = db.select_return_A_data(
            'SELECT should_date FROM qtw_loan_db.p2p_borrower_return_plan WHERE debtcode = "%s" AND term_num = %s' % (
            debtCode, term_num))
        should_date = str(should_date[0])
        print("=================跑手工任务给回款第%s期，给出借人，时间%s====================" % (term_num, should_date))
        url3 = self.coreurlbase + "/rest/testCrontabJob/testAutoCashBack"
        header1 = {"Content-Type": "application/json"}
        data3 = {'jsonParams': '{"method":"testAutoCashBack","params":{"cashBackDate":%s,"debtCode":"%s"}}\n' % (
            should_date, debtCode), '_': '1542807282908', 'callback': 'jQuery17204517549754820951_1542806876216\n',
                 't': '1542807282907\n'}
        print(data3)
        rels = self.core.get(url3, params=data3, headers=header1)
        print(rels.text)
        if "SUCCESS" in rels.text:
            print("核心交易执行手工正常回款任务成功")
        else:
            raise Exception("核心交易执行手工正常回款任务失败")
        print("================查询还款状态====================")
        repayStatus = "0"
        for i in range(10):
            time.sleep(15)
            url4 = self.coreurlbase + "/rest/settle/queryDebtRepayPage"
            header1 = {"Content-Type": "application/json"}
            data4 = {'callback': 'jQuery17206316655256710433_1562162797078\n', '_': '1562162810402',
                     't': '1562162810402\n',
                     'jsonParams': '{"method":"queryDebtRepayPage","params":{"page":{"conditions":"{\\"debtCode\\":\\"%s\\"}","pageNum":1,"pageSize":10}}}\n' % debtCode}
            rels = self.core.get(url4, params=data4, headers=header1)
            # print(rels.text)
            rStatus = self.regular('periodSeq":%s,"planRepayDate(.+?)}' % term_num, rels.text)
            repayStatus = self.regular('repayStatus":"(.+?)"', rStatus)
            print(repayStatus)
            if repayStatus == "10":
                print("回款成功")
                break
        if repayStatus != "10":
            raise Exception("回款失败")

    def financialsave_zx(self, money):
        '''
        :return: 智享服务发标
        '''
        print("第一步：创建智享标")
        url4 = self.coreurlbase + "/rest/financial/save"
        header1 = {"Content-Type": "application/json"}
        data4 = {
            'jsonParams': '{"method":"saveFinancial","params":{"param":"{\\"categoryId\\":\\"1000000001\\",\\"expectTol\\":\\"%s\\",\\"startTime\\":\\"2018-11-24 20:02:58\\",\\"endTime\\":\\"2020-11-24 20:03:13\\"}","type":"submit"}}\n' % money,
            't': '1543061018937\n', 'callback': 'jQuery17208713135843824564_1543056651820\n', '_': '1543061018937'}
        res2 = self.core.get(url4, params=data4, headers=header1)
        print(res2.text)
        if "SUCCESS" in res2.text:
            print("核心智享服务标创建成功")
        else:
            raise Exception("核心智享服务标创建失败")

        print("第二步：智享服务标审核通过，发标")
        db = MysqlDB()
        ts = time.strftime("%Y-%m-%d", time.localtime())
        script = "SELECT id,productNo FROM qtw_core_db.core_product_b WHERE insertTime LIKE '%s" % ts + "%' ORDER BY productNo DESC LIMIT 1;"
        result = db.select_return_A_data(script)
        bidcore_zx = str(result[0])  # 智享标的主键
        bidNocore_zx = str(result[1])  # 智享标的编号

        print("智享标的主键%s" % bidcore_zx)
        print("智享标的编号%s" % bidNocore_zx)

        self.rwf.update_resourse("resourse", "${bidcore_zx}", bidcore_zx)
        self.rwf.update_resourse("resourse", "${bidNocore_zx}", bidNocore_zx)

        url5 = self.coreurlbase + "/rest/financial/audit"
        header1 = {"Content-Type": "application/json"}
        data5 = {'_': '1543061778984', 'callback': 'jQuery17208713135843824564_1543056651873\n',
                 'jsonParams': '{"method":"auditFinancial","params":{"param":"{\\"id\\":\\"%s\\",\\"bidStatus\\":\\"1\\"}"}}\n' % bidcore_zx,
                 't': '1543061778983\n'}
        res2 = self.core.get(url5, params=data5, headers=header1)
        print(res2.text)
        if "SUCCESS" in res2.text:
            print("核心智享服务标发标成功")
        else:
            raise Exception("核心智享服务标发标失败")

    def cuohejiesuan_zx(self, debtCode, bidNocore):
        '''
        :param debtCode: 债权编号
        :param bidNocore: 标的编号
        :return: 撮合结算
        '''
        db = MysqlDB()
        script = 'SELECT debtId FROM qtw_core_db.core_loan_debt_info WHERE debtCode = "%s"' % debtCode
        result = db.select_return_A_data(script)
        debtId = str(result[0])
        script = 'SELECT id FROM qtw_core_db.core_loan_unmatch_debt WHERE debtId = "%s"' % debtId
        result = db.select_return_A_data(script)
        undebtId = str(result[0])  # 未匹配所有债权的主键
        print("未匹配所有债权的主键%s" % undebtId)
        # 查询订单的主键
        url3 = self.coreurlbase + "/rest/invest/query"
        header1 = {"Content-Type": "application/json"}
        data3 = {'_': '1543066226060', 'callback': 'jQuery17208713135843824564_1543056652065\n', 't': '1543066226060\n',
                 'jsonParams': '{"method":"queryOrderList","params":{"page":{"conditions":"{\\"bidNo\\":\\"%s\\"}","pageNum":1,"pageSize":10}}}\n' % bidNocore}
        res2 = self.core.get(url3, params=data3, headers=header1)
        print(res2.text)
        orderNo = self.regular('"orderNo":"(.+?)"', res2.text, 1)
        script = 'SELECT id FROM qtw_core_db.core_biz_invest_order WHERE orderNo = "%s"' % orderNo
        result = db.select_return_A_data(script)
        orderNo = str(result[0])  # 订单的主键
        print("订单的主键%s" % orderNo)

        print("============撮合，一条债权撮合一条订单")
        url4 = self.coreurlbase + "/rest/unMatchDebt/handMatch"
        header1 = {"Content-Type": "application/json"}
        data4 = {
            'jsonParams': '{"method":"handMatch","params":{"id":%s,"orders":[{"orderId":"%s","matchAmt":1000000}]}}\n' % (
            undebtId, orderNo), 't': '1543064261829\n', '_': '1543064261829',
            'callback': 'jQuery17208713135843824564_1543056651993\n'}
        res2 = self.core.get(url4, params=data4, headers=header1)
        print(res2.text)
        if "SUCCESS" in res2.text:
            print("核心系统撮合成功")
        else:
            raise Exception("核心系统撮合失败")

        print("============结算管理，系统结算=======")
        url4 = self.coreurlbase + "/rest/unMatchDebt/autoSettle"
        header1 = {"Content-Type": "application/json"}
        data4 = {'_': '1543067738322', 'callback': 'jQuery17208713135843824564_1543056652137\n',
                 'jsonParams': '{"method":"autoSettle"}\n', 't': '1543067738322\n'}
        res2 = self.core.get(url4, params=data4, headers=header1)
        print(res2.text)
        if "SUCCESS" in res2.text:
            print("核心系统结算成功")
        else:
            raise Exception("核心系统结算失败")

    def regular(self, regex, content, index=1):
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


if __name__ == "__main__":
    c = CoreSystem()
    c.coresyslogin()
    # c.querydebtId("jj2019070300006")
    c.cuohejiesuan_zx("jj2019070500005", "zxfw0120190705003")