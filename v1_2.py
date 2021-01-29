from selenium import webdriver
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymysql
def job():
    db=pymysql.connect(host="localhost",user="",password="",db="")
    cursor=db.cursor()
    cursor.execute("select * from clockin_personinfo")
    data = cursor.fetchall()
    for id,name,email,password in data:
        try:
            jobs(name,password,email)
        except:
            pass
    cursor.close()
    db.close()

def send_email(email_address):
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="171932086@qq.com"    #用户名
    mail_pass=""   #口令
    sender = '171932086@qq.com'
    receivers = [email_address]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText('打卡成功', 'plain', 'utf-8')
    message['From'] = Header("hwh", 'utf-8')
    message['To'] =  Header("厦大人", 'utf-8')
		 
    subject = '打卡成功'
    message['Subject'] = Header(subject, 'utf-8')	 
		 
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
    except smtplib.SMTPException:
       print ("Error: 无法发送邮件")



def jobs(username,password,email):

    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    #driver = webdriver.Chrome(chrome_options=chrome_options)#可替换为后台运行
    chromeoptions = webdriver.ChromeOptions()

    chromeoptions.add_argument('--headless')  #浏览器无窗口加载
    chromeoptions.add_argument('--disable-gpu')  #不开启gpu加速
    
    """
    解决报错:
    selenium.common.exceptions.webdriverexception: message: unknown error: chrome failed to start: exited abnormally
    (unknown error: devtoolsactiveport file doesn't exist)
    """
    chromeoptions.add_argument('--disable-dev-shm-usage')  #禁止
    chromeoptions.add_argument('--no-sandbox')#以根用户打身份运行chrome，使用-no-sandbox标记重新运行chrome

    #其它设置(可选):
    #chromeoptions.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
    #chromeoptions.add_argument('blink-settings=imagesenabled=false') #不加载图片, 提升速度
    #chromeoptions.add_argument("user-agent=mozilla/5.0 (windows nt 10.0; wow64) applewebkit/537.36 (khtml, like gecko) chrome/71.0.3578.98 safari/537.36")  #伪装其它版本浏览器,有时可以解决代码在不同环境上的兼容问题,或者爬虫cookie有效性保持一致需要设置此参数

    #创建driver对象
    #chrome_options=chromeoptions加载设置
    #executable_path="/usr/bin/chromedriver"指定webdriver路径(可选)
    driver = webdriver.Chrome(chrome_options=chromeoptions,executable_path="/usr/local/bin/chromedriver")
    driver.get("https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu")
    wait = WebDriverWait(driver,10)
    driver.find_element('id','username').send_keys(username)
    driver.find_element('id','password').send_keys(password)
    #driver.find_element_by_xpath("//*[@id='casLoginForm']/p[5]/button").click()#登录
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]')))
    button.click()#登录
    driver.find_element_by_xpath("//*[@id='mainPage-page']/div[1]/div[3]/div[2]/div[2]/div[3]/div/div[1]/div[2]").click()#进入防疫登记表单
    sleep(3)
    driver.switch_to_window(driver.window_handles[-1])

    driver.find_element_by_xpath('//*[@id="mainM"]/div/div/div/div[1]/div[2]/div/div[3]/div[2]').click()#点击我的表单

    sleep(3)
    driver.find_element_by_xpath('//*[@id="select_1582538939790"]/div/div').click()#更改表单内容
    driver.find_element_by_xpath('/html/body/div[8]/ul/div/div[3]/li').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[2]/div[1]/div/div/span/span').click()#点击确定

    confirm = driver.switch_to.alert#处理confirm弹出框
    confirm.accept() #点击confirm的确定按钮

    sleep(3)
    driver.quit()
    send_email(email)

if __name__=='__main__':
    scheduler = BlockingScheduler()
    intervalTrigger=CronTrigger(hour=7,minute=10)
    scheduler.add_job(job,intervalTrigger,id='my_job_id')
    try:
        scheduler.start()
    except:
        with open('日志.txt','w',encoding='utf8')as file:
            file.write('%s 发生错误' %datetime.now())

