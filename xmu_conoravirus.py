from selenium import webdriver
from time import sleep
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
def job():
    username = 'yourusername'#请更改
    password = 'yourpassword'

    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    #driver = webdriver.Chrome(chrome_options=chrome_options)#可替换为后台运行
    driver = webdriver.Chrome()
    driver.get("https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu")

    driver.find_element('id','username').send_keys(username)
    driver.find_element('id','password').send_keys(password)
    driver.find_element_by_xpath("//*[@id='casLoginForm']/p[5]/button").click()#登录

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


if __name__=='__main__':
    scheduler = BlockingScheduler()
    intervalTrigger=CronTrigger(hour=9,minute=15)
    scheduler.add_job(job,intervalTrigger,id='my_job_id')
    try:
        scheduler.start()
        print('启动成功')
    except:
        with open('日志.txt','w',encoding='utf8')as file:
            file.write('%s 发生错误' %datetime.now())

