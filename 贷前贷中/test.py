import time
from selenium import webdriver


class A():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.baidu.com/")
        # 输入Selenium并点击'百度一下'按钮
        # self.driver.maximize_window()
        time.sleep(2)
    def aa(self):
        self.driver.find_element_by_id("kw").send_keys("selenium")
        self.driver.find_element_by_id("su").click()
        self.driver.find_element_by_xpath('//*[@id="s_tab"]/div/a[7]').click()
        self.driver.find_element_by_xpath('//*[@id="sole-input"]').clear()
        self.driver.find_element_by_xpath('//*[@id="sole-input"]').send_keys("经海路")
        self.driver.find_element_by_xpath('//*[@id="search-button"]').click()
        time.sleep(3)
    def ab(self):
        self.driver.find_element_by_xpath('//*[@id="card-2"]/div/ul/li[1]/div[1]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="route-from"]/span[2]').click()
        self.driver.find_element_by_xpath('//*[@id="route-searchbox-content"]/div[2]/div/div[2]/div[2]/input').send_keys(
            "九棵树地铁站")
        self.driver.find_element_by_xpath('//*[@id="search-button"]').click()

class B():
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://www.baidu.com/")
        # 输入Selenium并点击'百度一下'按钮
        # self.driver.maximize_window()
        time.sleep(2)
    def aa(self):
        self.driver.find_element_by_id("kw").send_keys("selenium")
        self.driver.find_element_by_id("su").click()
        self.driver.find_element_by_xpath('//*[@id="s_tab"]/div/a[7]').click()
        self.driver.find_element_by_xpath('//*[@id="sole-input"]').clear()
        self.driver.find_element_by_xpath('//*[@id="sole-input"]').send_keys("经海路")
        self.driver.find_element_by_xpath('//*[@id="search-button"]').click()
        time.sleep(3)
    def ab(self):
        self.driver.find_element_by_xpath('//*[@id="card-2"]/div/ul/li[1]/div[1]').click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="route-from"]/span[2]').click()
        self.driver.find_element_by_xpath('//*[@id="route-searchbox-content"]/div[2]/div/div[2]/div[2]/input').send_keys(
            "小红门")
        self.driver.find_element_by_xpath('//*[@id="search-button"]').click()


# driver.close()
# driver.quit()
if __name__=="__main__":
    a = A()
    b = B()
    a.aa()
    b.aa()
    a.ab()
    b.ab()