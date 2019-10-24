#coding=utf-8
import os
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from common.ReadAndWriteFiles import ReadAndWriteFiles
from common.ReadXML import ReadXML


def send_mail(subject):
    rwf = ReadAndWriteFiles()
    rx = ReadXML()
    result = rx.readx(rwf.pathreportxml)


    to_addrs = str(rwf.ini_read(rwf.pathemailini,"email_to_addrs")).strip(',').split(',')  # 收件人地址
    from_addr = str(rwf.ini_read(rwf.pathemailini,"email_from_addr"))  # 发件人人地址
    smtp_addr = str(rwf.ini_read(rwf.pathemailini,"email_smtp_addr"))  # 邮件服务器
    password = str(rwf.ini_read(rwf.pathemailini,"email_password"))  # 发件人密码
    mail_msg = MIMEMultipart()  # 初始化邮件内容

    str5 = ""
    str0 = '<div class="heading"><h1>去投网2.0接口测试报告</h1><p class="attribute"><strong>Start Time:</strong> %s</p><p class="attribute"><strong>Duration:</strong> ———</p><p class="attribute"><strong>Status:</strong> Pass %s Fail %s</p><p class="description">去投网2.0接口测试</p></div>'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),result["pass"],result["fail"])
    str1 = '<table border="1" cellspacing="0" style="width: 80%;border-collapse: collapse;border: 1px solid #777;"><tbody>'
    str2 = '<tr style="font-weight: bold;color: white;background-color: #777;"><td>去投网2.0api接口测试</td><td>Count</td><td>Pass</td><td>Fail</td></tr>'
    if int(result["fail"]) > 0:
        str3 = '<tr style="background-color: #c60;"><td>test_result</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(result["pass"]+result["fail"],result["pass"],result["fail"])
    else:
        str3 = '<tr style="background-color: #6c6;"><td>test_result</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (result["pass"]+result["fail"],result["pass"],result["fail"])
    i = 1
    for key in result["base"].keys():
        if int(result["base"][key][1]) > 0:
            str5 = str5 + '<tr style="background-color: #c60;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%(i,key,result["base"][key][0],result["base"][key][1])
        else:
            str5 = str5 + '<tr style="background-color: #6c6;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (i,key,result["base"][key][0],result["base"][key][1])
        i = i +1

    #=============================主要流程=============================
    str50 = ""
    str20 = '<tr style="font-weight: bold;color: white;background-color: #777;"><td>去投网2.0主要流程测试</td><td>Count</td><td>Pass</td><td>Fail</td></tr>'
    i = 1
    for key in result["func"].keys():
        if int(result["func"][key][1]) > 0:
            str50 = str50 + '<tr style="background-color: #c60;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (i,key,result["func"][key][0],result["func"][key][1])
        else:
            str50 = str50 + '<tr style="background-color: #6c6;"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (i,key,result["func"][key][0],result["func"][key][1])
        i = i + 1

    str6 = '</tbody></table>'
    str7 = "<a href ='http://192.168.1.31:8090/jenkins/job/qtw_interfacetest_autoenv_SendEmail/'><button type='button'>" \
           "<h4>点击查看详细报告</h4></button></a>"
    str1 = str0+str1+str2+str3+str5+str20+str50+str6+str7


    test = str1.encode('utf-8')
    mail_body =test

    MIMEText(mail_body, 'plain', 'utf-8')

    html_report = MIMEText(mail_body, _subtype='html', _charset='utf-8')
    mail_msg.attach(html_report)  # 读取的报告写在邮件内容中
    mail_msg['Subject'] = subject
    mail_msg['From'] = from_addr
    mail_msg['To'] = ','.join(to_addrs)
    s = smtplib.SMTP()
    s.connect(smtp_addr)
    s.login(from_addr, password)
    s.sendmail(from_addr, to_addrs, mail_msg.as_string())
    s.quit()




if __name__ == '__main__':
    send_mail("去投网2.0接口测试")
