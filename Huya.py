import os.path
import time
import json
import datetime

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import Driver

class HuyaCheck:
    def __init__(self, gen_page, sr_page, vision=False):
        pass
        self.vision = vision
        self.driver = self.init_chrome()
        self.gen_page = gen_page
        self.sr_page = sr_page




    def init_chrome(self):
        driver = Driver.init_chrome(user_dir_name='Default', vision=self.vision, keep_alive=False)

        # 访问 Huya 主播页面
        page = "https://www.huya.com/28908254"
        driver.get(page)

        # 这里可以执行其他 Selenium 操作，例如查找元素、模拟点击等
        # input()
        # time.sleep(50)

        if not os.path.exists("huya.cookie"):
            input("press to continue")
            with open("huya.cookie", 'w') as f:
                # 将cookies保存为json格式
                f.write(json.dumps(driver.get_cookies()))
        else:
            with open('huya.cookie', 'r') as f:
                # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
                cookies_list = json.load(f)

                # 将expiry类型变为int
                for cookie in cookies_list:
                    # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
                    if isinstance(cookie.get('expiry'), float):
                        cookie['expiry'] = int(cookie['expiry'])
                        driver.add_cookie(cookie)

        driver.refresh()

        return driver

    def set_time(self, hour, min, sec):
        self.hour, self.min, self.sec = hour, min, sec


    def check_time(self, ignore_time=False):
        if ignore_time:
            return True
        start_time = datetime.datetime.combine(datetime.datetime.now().date(),
                                               datetime.time(hour=self.hour, minute=self.min, second=self.sec))
        sec5 = datetime.timedelta(seconds=5)
        min3 = datetime.timedelta(seconds=180)
        return start_time - sec5 < datetime.datetime.now() < start_time + min3



    def check_sr(self, loop=False, ignore_time=False):
        # input()
        self.driver.get(self.sr_page)
        time.sleep(5)
        # 寻找按钮
        elements = self.driver.find_elements(By.CLASS_NAME, "item.J_item")
        self.driver.execute_script("arguments[0].click();", elements[1])
        time.sleep(1)
        elements = self.driver.find_elements(By.CLASS_NAME, "tab-item.J_connShow")
        self.driver.execute_script("arguments[0].click();", elements[1])
        time.sleep(1)
        # 创建一个新的div元素，并将元素m移动到这个div中
        self.driver.execute_script('''
            var newDiv = document.createElement('div');
            var BPS = document.querySelectorAll('.diy-comp[data-flag^="BP"]');
            for (var i = 0; i < BPS.length; i++) { 
                if (BPS[i].children.length > 0) {
                    newDiv.appendChild(BPS[i]);
                }
            }
            document.getElementById('main_col').innerHTML='';
            document.getElementById('main_col').appendChild(newDiv);
        ''')
        element = self.driver.find_element(By.XPATH, "//div[@class='task-name' and text()='+10经验值']")
        li_element = element.find_element(By.XPATH, "./ancestor::li")
        button = li_element.find_element(By.XPATH, "./button")
        self.driver.execute_script("arguments[0].click();", button)
        button_text = button.text
        # print("子节点 <button> 的文本:", button_text)
        if loop:
            self.loop(exp_button=button, ignore_time=ignore_time)
        # input("press any key to continue")
        return "All pass" if button_text == "已领取" else "虎 铁 unfinish！！！"

    def check_gen(self, loop=False, ignore_time=False):
        self.driver.get(self.gen_page)
        time.sleep(5)
        # 寻找按钮
        elements = self.driver.find_elements(By.CLASS_NAME, "item.J_item")
        elements[2].click()
        self.driver.execute_script('''
            var newDiv = document.createElement('div');
            var BPS = document.querySelectorAll('.diy-comp[data-flag^="BP"]');
            for (var i = 0; i < BPS.length; i++) { 
                if (BPS[i].children.length > 0) {
                    newDiv.appendChild(BPS[i]);
                }
            }
            document.getElementById('main_col').innerHTML='';
            document.getElementById('main_col').appendChild(newDiv);
        ''')
        time.sleep(5)
        button = self.driver.find_element(By.XPATH,
                                          "//div[@class='task-name' and text()='+10经验值']/ancestor::li/button")
        self.driver.execute_script("arguments[0].click();", button)
        button_text = button.text


        if loop:
            self.loop(exp_button=button, ignore_time=ignore_time)

        return "All pass" if button_text == "已领取" else "虎 原 unfinish！！！"

    def loop(self, exp_button, ignore_time=False):
        def clear():
            waste_dialog = self.driver.find_elements(By.CLASS_NAME, "diy-com-pop-cover") + \
                           self.driver.find_elements(By.CLASS_NAME, "diy-com-pop")
            for c in waste_dialog:
                self.driver.execute_script("arguments[0].remove();", c)
        clear()

        while True:
            if self.check_time(ignore_time):
                try:
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", exp_button)
                    text = self.driver.find_elements(By.CLASS_NAME, 'dcpc-text')[0]
                    clear()
                except selenium.common.exceptions.StaleElementReferenceException:

                    break
                except IndexError as e:
                    if exp_button.text != "未完成":
                        break
            else:
                print(".", end="")
                time.sleep(10)

        on_received_li = self.driver.find_elements(By.CLASS_NAME, "on.received")[0]
        on_received_button = on_received_li.find_element(By.TAG_NAME, "button")
        # try:
        #     next_li = on_received_li.find_element(By.XPATH, './following-sibling::li')
        #     next_button = next_li.find_element(By.TAG_NAME, "button")
        # except selenium.common.exceptions.NoSuchElementException:
        #     next_button = on_received_button
        next_button = on_received_button
        for b in [on_received_button, next_button]:
            self.driver.execute_script(f"arguments[0].setAttribute('class', 'do-task-btn J_getLevelAward')", b)

        while self.check_time():
            for b in [on_received_button, next_button]:
                try:
                    self.driver.execute_script("arguments[0].click();", b)
                except selenium.common.exceptions.StaleElementReferenceException:
                    on_received_li = self.driver.find_elements(By.CLASS_NAME, "on.received")[0]
                    on_received_button = on_received_li.find_element(By.TAG_NAME, "button")

                    next_li = on_received_li.find_element(By.XPATH, './following-sibling::li')
                    next_button = next_li.find_element(By.TAG_NAME, "button")
                    print("chong xin ding wei an niu")
                    continue
                try:
                    time.sleep(0.5)
                    t = self.driver.find_elements(By.CLASS_NAME, 'dcpc-text')[0]
                    print(t.text)
                    clear()
                except IndexError:
                    print("xun zhao text chu cuo")
                    continue

if __name__ == "__main__":
    Checker = HuyaCheck(gen_page="https://www.huya.com/189385",
                        sr_page="https://www.huya.com/126423",
                        vision=False)
    Checker.set_time(hour=1, min=0, sec=0)

    g_status = Checker.check_gen(loop=True, ignore_time=1)# 原
    # s_status = Checker.check_sr(loop=True, ignore_time=False) # 崩
    # print(g_status, s_status)
