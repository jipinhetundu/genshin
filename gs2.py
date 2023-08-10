import requests
import pickle
import json
import time
import random
import multiprocessing

# cookie_path = r'D:\Users\11201\Downloads\biliupR-v0.1.19-x86_64-windows\cookies.json'
cookie_path = r'cookies.json'
taskid = '6407fa34'
single_task_url = f'https://api.bilibili.com/x/activity/mission/single_task?csrf=696a628ebb741bcc4e5743615aa88d5f&id={taskid}'
class Config():
    def __init__(self):
        self.data = {}
    def load_cookies(self):
        self.data["user"] = {"cookies": {}}
        with open(cookie_path, encoding='utf-8') as stream:
            s = json.load(stream)
            for i in s["cookie_info"]["cookies"]:
                name = i["name"]
                self.data["user"]["cookies"][name] = i["value"]
            self.data["user"]["access_token"] = s["token_info"]["access_token"]
s = Config()
s.load_cookies()
# print(s.data['user'].keys())
print(s.data['user']['cookies'])

# 目标URL
url = "https://api.bilibili.com/x/activity/mission/task/reward/receive?access_key="+s.data['user']['access_token']
# print(url)

# 请求体数据
data = {
    # 将POST请求体的数据添加在这里，以表单参数形式提供
    # 示例：如果有参数名为 "param1" 和 "param2"，并且值分别为 "value1" 和 "value2"，可以这样添加：
    # "param1": "value1",
    # "param2": "value2",
    'csrf': '6261da124b0840a9f45802f6f2141031',
    'act_id': '769',
    'task_id': '3115',
    'group_id': '0',
    'receive_id': '1150986', # 2052147 # 1139956 1141252 1144439
    'receive_from': 'missionPage',
    'act_name': '星穹铁道1.2版本任务【直播】',
    'task_name': '累计20天完成全部“每日直播任务”',
    'reward_name': '星琼*1000',
    'gaia_vtoken': '',
}


# 请求头信息
headers = {
    "Authority": "api.bilibili.com",
    "Method": "POST",
    "Path": "/x/activity/mission/task/reward/receive",
    "Scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Length": "428",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.bilibili.com",
    "Referer": "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id="+taskid,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def loop():
    session = requests.Session()
    i = 0
    if True:
        i += 1
        response = session.post(url, data=data, headers=headers, cookies=s.data['user']['cookies'])
        if json.loads(response.content)['code']>0:
            print(response.text, i)
            i = 0
        # time.sleep(1)

if __name__ == '__main__':
    multiprocessing.freeze_support()  # Initialize multiprocessing
    time1 = time.perf_counter()
    #线程数
    pool = multiprocessing.Pool(50)
    #一共跑几次
    task_number = 10000
    for i in range(task_number):
        pool.apply_async(func=loop, args=())
    pool.close()
    pool.join()
    time2 = time.perf_counter()
    times = time2 - time1
    print(times / task_number)  # 每次请求用时