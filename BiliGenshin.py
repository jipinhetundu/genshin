import requests
import pickle
import json
import time
import random
import multiprocessing
import datetime
import CookieText

class DelaySession:
    def __init__(self, session):
        self.session = session

    def get(self, delay=1, *args, **kwargs):
        time.sleep(delay)
        # print(*args)
        # self.session.headers['Method'] = 'GET'
        # self.
        return self.session.get(*args, **kwargs)




class SingleReward:
    # 用来领取一个task_id对应的奖励
    def __init__(self, task_id, cookie_id):
        self.cookie_id = cookie_id
        self.cookie_str = CookieText.Bili[cookie_id]['Cookie']
        self.task_id = task_id
        self.csrf = self.cookie_str.split("bili_jct=")[1].split(";")[0]
        self.single_task_url = f'https://api.bilibili.com/x/activity/mission/single_task?csrf={self.csrf}&id={task_id}'
        self.cookie = CookieText.parse_cookie(self.cookie_str)
        self.may_start_time = None

        self.receive_url = f"https://api.bilibili.com/x/activity/mission/task/reward/receive?" \
                           f"access_key={self.csrf}" \
                           f"&access_token={self.csrf}"
        self.data = {
            'csrf': self.csrf,
            'receive_from': 'missionPage',
        }
        self.headers = {
            "Authority": "api.bilibili.com",
            "Method": "POST",
            "Path": "/x/activity/mission/task/reward/receive",
            "Scheme": "https",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            # "Content-Length": "428",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.bilibili.com",
            "Referer": "https://www.bilibili.com/blackboard/activity-award-exchange.html?task_id="+self.task_id,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        self.start_time = None
        self.headers['Cookie'] = self.cookie_str
        self.session = requests.Session()
        self.session.headers = self.headers
        self.session = DelaySession(self.session)




    def test_day_ok_gen(self, ver="4.2", task_ids=["a3521d29", "e8dedd3d", "13c1f49a", "67240ae2"]):
        res = ""
        for task_id in task_ids:
            single_task_url = f'https://api.bilibili.com/x/activity/mission/single_task?csrf={self.csrf}&id={task_id}'
            # print(self.cookie['user']['cookies'])
            response = self.session.get(url=single_task_url)
            content = json.loads(response.content)
            code = content['code']
            rec = 0
            if code == 0:
                rec = content["data"]["task_info"]["receive_id"]
            if rec != 0:
                continue
            else:
                print("g", code, rec)
                res+=f'{ver}, {code}, {response.text}'
        return "All pass" if not res else str(code)

    def test_day_ok_sr(self, ver="1.5", task_ids=["6ERA1wloghvfce00"]):
        res = ""
        for task_id in task_ids:
            single_task_url = f'https://api.bilibili.com/x/activity_components/mission/info?csrf={self.csrf}&task_id={task_id}'
            # print(single_task_url)
            response = self.session.get(url=single_task_url)
            content = json.loads(response.content)
            code = content['code']
            rec = 0
            if code == 0:
                rec = content["data"]["task_finished"]
            if rec:
                continue
            else:
                print("sr", task_id, code, rec, response.text)
                res+=f'{ver}, {code}, {response.text}'
        return "All pass" if not res else str(code)

    def get_self_data(self):
        single_task_url = f'https://api.bilibili.com/x/activity_components/mission/info?csrf={self.csrf}&task_id={self.task_id}'
        response = self.session.get(url=single_task_url, data=self.data)
        content = json.loads(response.content)
        # print(content)
        '''
        gaia_vtoken: 16209de9e5c94157a869660ad4c2e7cb
        '''
        try:
            # sr
            self.data['activity_name'] = content["data"]["act_name"]
            self.data['activity_id'] = content["data"]["act_id"]
            self.data['task_id'] = content["data"]["task_id"]
            self.data['task_name'] = content["data"]["task_name"]
            self.data['reward_name'] = content["data"]['reward_info']["award_name"]
            self.data['gaia_vtoken'] = '16209de9e5c94157a869660ad4c2e7cb'
        # except :
        except KeyError:
            # gen
            self.data['act_name'] = content["data"]["act_info"]["act_name"]
            self.data['act_id'] = content["data"]["act_info"]["id"]
            self.data['task_id'] = content["data"]["task_info"]["id"]
            self.data['task_name'] = content["data"]["task_info"]["task_name"]
            self.data['reward_name'] = content["data"]["task_info"]['reward_info']["reward_name"]
            rec = content["data"]["task_info"]["receive_id"]
            if rec != 0:
                self.data['receive_id'] = str(rec)
        except TypeError:
            print("其它错误。返回值为None，可能是taskid不对")
            return



    def get_start_time(self):
        times = 0
        while True:
            try:
                times += 1
                response = self.session.get(url=self.single_task_url, data=self.data)
                content = json.loads(response.content)
                if content['code'] == 75950:
                    single_task_url = f'https://api.bilibili.com/x/activity_components/mission/info?csrf={self.csrf}&task_id={self.task_id}'
                    response = self.session.get(url=single_task_url, data=self.data)
                    content = json.loads(response.content)
                if content['code'] == -702:
                    time.sleep(1)
                    continue
                try:
                    try:
                        self.data['task_name'] = content["data"]["task_info"]["task_name"]
                    except KeyError:
                        # 星铁现在1.5抓不到start_time
                        self.data['task_name'] = content["data"]["task_name"]
                        return
                    rep_str = self.data['task_name'].replace("累计投稿","累积").replace("累计", "累积").replace("完成", "累积")
                    # print(self.data['task_name'], rep_str)
                    days = int(rep_str.split("累积")[1].split("天")[0])
                    # try:
                    #     days = self.data['task_name'].split("完成")[1].split("天每日所有任务")[0]
                    #     days = int(days)
                    # except:
                    #     days = self.data['task_name'].replace("累计", "累积").split("累积")[1].split("天")[0]
                    #     days = int(days)
                    cycle_start_time = [i["cycle_start_time"] for i in content["data"]["task_info"]["reward_stock_configs"]]
                    self.may_start_time = max(cycle_start_time)
                    cycle_start_time = min(cycle_start_time)
                    start_time = cycle_start_time + (days - 1) * 86400 - 3600 * 11 + 3599
                    # print(int(content["data"]["task_info"]["task_name"].split("完成")[1].split("天每日所有任务")[0]))
                    return start_time
                except ImportError:
                    if "data" in content.keys():
                        return content["data"]["task_info"]["reward_stock_configs"][0]["cycle_start_time"] + 3599
            except ImportError:
                time.sleep(1)
                if times > 10000:
                    print("获取截止日期出错！")
                    return


    def try_get_receive_id(self):
        self.start_time = self.get_start_time()
        while True:
            now_get = self.get_start_time()
            self.start_time = now_get
            if now_get > time.time():
                print(f'{self.task_id}:{self.data["task_name"]}的时间未到！ 预期开始时间:{self.start_time},当前时间:{time.time()},'
                      f'post将于{(self.start_time - time.time()) / 2}秒后再次发送。')
                time.sleep((now_get - time.time()) / 2)
            response = self.session.get(url=self.single_task_url)
            content = json.loads(response.content)
            code = content['code']
            if code == 0:
                rec = content["data"]["task_info"]["receive_id"]
                self.data['act_name'] = content["data"]["act_info"]["act_name"]
                self.data['act_id'] = content["data"]["act_info"]["id"]
                self.data['task_id'] = content["data"]["task_info"]["id"]
                self.data['task_name'] = content["data"]["task_info"]["task_name"]
                self.data['reward_name'] = content["data"]["task_info"]['reward_info']["reward_name"]
                print(f"{self.data['task_name']}recid:", rec if rec else "-")
            else:
                print("." + str(code) + "/", end="")
                continue
            if rec != 0:
                self.data['receive_id'] = str(rec)
                print(self.data)
                break
            else:
                time.sleep(0 if datetime.datetime.now().hour < 4 else 10)

        return self.start_time

    def get_cookie(self):
        # 读取biliup工程中获得的cookie
        # 弃用
        data = dict()
        data["user"] = {"cookies": {}}
        cookie_str = "?access_key="
        with open(self.cookie_path, encoding='utf-8') as stream:
            s = json.load(stream)
            # print(s)
            cookie_str += s['token_info']['access_token'] + "&"
            for i in s["cookie_info"]["cookies"]:
                name = i["name"]
                data["user"]["cookies"][name] = i["value"]
                cookie_str += f"{name}={i['value']}&"
            data["user"]["access_token"] = s["token_info"]["access_token"]

            # data['user']['cookies'] =
            # print('https://api.bilibili.com/x/activity/mission/task/reward/receive' + cookie_str[:-1])
        # print(1 / 0)
        return data

    def loop(self, sleep=1):

        # ----弃用，start_time从1.5版本开始抓不到了，还是手动输入比较好-----
        # if not self.start_time:
        #     self.start_time = self.try_get_receive_id()
        # while True:
        #     if time.time() > self.start_time:
        #         break
        #     else:
        #         print(f'{self.task_id}:{self.data["task_name"]}的时间未到！ 预期开始时间:{self.start_time},当前时间:{time.time()},'
        #               f'post将于{(self.start_time - time.time()) / 2}秒后再次发送。')
        #         time.sleep((self.start_time - time.time()) / 2)
        # --------------------------------------------------------
        self.get_self_data()
        print(self.data)
        i = 0
        conut_101 = 0
        while True:
            i += 1




            response = self.session.session.get(url='https://data.bilibili.com/log/web?0000171702409792330https%3A%2F%2Fwww.bilibili.com%2Fblackboard%2Fnew-award-exchange.html%3Ftask_id%3D6ERA1wloghvhw100|888.81821.selfDef.dt_task-award_0_award_click||1702409792000|0|0|594x715|1|{%22event%22:%22dt_task-award_0_award_click%22,%22value%22:{%22task_id%22:%226ERA1wloghvhw100%22,%22award_id%22:%225ERA1wloghvgey00%22,%22award_receive_status%22:2,%22award_receive_text%22:%22%E6%AF%8F%E6%97%A5%E5%BA%93%E5%AD%98%E5%B7%B2%E8%BE%BE%E4%B8%8A%E9%99%90%22,%22local_time%22:%22Wed%20Dec%2013%202023%2003:36:32%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)%22,%22online_time%22:%22Wed%20Dec%2013%202023%2003:33:26%20GMT+0800%20(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)%22},%22bsource%22:%22%22,%22appBuvid%22:%22%22,%22b_nut_h%22:1680710400,%22lsid%22:%22B738A92A_18C5F69071A%22,%22buvid_fp%22:%222a6d69ab418362d1b7f5b6ff9f248fed%22,%22buvid4%22:%220E36E6C0-EEF7-A6B8-6E5D-E565D4E7979296292-022012521-bLBnUTnxriDSYoWSQjmLMg%3D%3D%22,%22bsource_origin%22:%22empty%22,%22share_source_origin%22:%22empty%22}|{}|https%3A%2F%2Fwww.bilibili.com%2Fblackboard%2Fera%2FdtQaF6aJp3nMxO8K.html|F91104F66-661F-8F1A-F2610-BBAFE10EB831902537infoc|zh-CN|null|1')
            print(response.text)

            response = self.session.session.post(url=self.receive_url, data=self.data)

            content = json.loads(response.content)
            code = content['code']
            print(response.text, self.data)
            input()
            if code >= 1:
                i = 0

            if code == -101:
                # 用户未登录(需要验证码)
                print(".", end="")
                conut_101 += 1
                if conut_101 > 10:
                    print(response.text, self.data['receive_id'], i, "需要验证码！")
                    break
                time.sleep(0.3)
                continue
            else:
                conut_101 = 0
            if code == -400:
                # 领取信息不存在，recid错了
                self.start_time = self.try_get_receive_id()
                continue
            elif code == -702:
                # 自身访问次数过多
                print("x", end="")
            elif code == -705:
                # 全局访问次数过多
                print("-", end="")
                continue
            elif code == 75086:
                print(response.text, self.data['receive_id'], i)
                print(f'{self.task_id}:{self.data["task_name"]}奖励已领取.')
                break
            elif code == 75153:
                if self.may_start_time:
                    current_datetime = time.time()
                    seconds = self.may_start_time - current_datetime
                    if seconds < 0:
                        self.start_time = self.get_start_time()
                        continue
                    print(f'{self.task_id}:{self.data["task_name"]}奖励未开始领取,等待{current_datetime}|{self.may_start_time}再次发送，还有{seconds}秒')
                    time.sleep(max(1., (seconds - 1) / 2))
                else:
                    self.start_time = self.get_start_time()
            elif code == 75154:
                print(response.text, self.data['receive_id'], i)
                current_datetime = datetime.datetime.now()
                today_date = current_datetime.date()
                tomorrow_date = today_date + datetime.timedelta(days=1)
                target_time = datetime.datetime(tomorrow_date.year, tomorrow_date.month, tomorrow_date.day, 0, 0, 0)
                time_difference = target_time - current_datetime
                seconds = time_difference.total_seconds()
                print(f'{self.task_id}:{self.data["task_name"]}奖励今日已领完,等待第二天再次发送，还有{seconds}秒')
                time.sleep(3600 - int(time.time()) % 3600)
            elif code == 0:
                print(response.text, self.data['receive_id'], i)
                print(f'{self.task_id}:{self.data["task_name"]}奖励已领取.')
                break
            elif code == 75255:
                print(response.text, self.data['receive_id'], i)
                print(f'{self.task_id}:{self.data["task_name"]}奖励无了.')
                break
            time.sleep(sleep)

    def info(self):
        print(self.data)

    def loop_in_web(self):
        import Driver
        url = f'https://www.bilibili.com/blackboard/new-award-exchange.html?task_id={self.task_id}'
        driver = Driver.init_chrome(user_dir_name=self.cookie_id, vision=True, keep_alive=True)
        # driver.get('https://www.bilibili.com/')
        # driver.get('https://www.bilibili.com/blackboard/era/8WDv3ZkrY311kYPm.html?spm_id_from=333.337.0.0')
        # driver.get('https://www.bilibili.com/blackboard/era/dtQaF6aJp3nMxO8K.html')
        driver.get(url)
        script = '''
        function getByClass(parent, cls){
        if(parent.getElementsByClassName){
            return parent.getElementsByClassName(cls);
        }else{
            var res = [];
            var reg = new RegExp(' ' + cls + ' ', 'i')
            var ele = parent.getElementsByTagName('*');
            for(var i = 0; i < ele.length; i++){
                if(reg.test(' ' + ele[i].className + ' ')){
                    res.push(ele[i]);
                }
            }
            return res;
        }
    }
    var wrap = getByClass(document.body, "tool-wrap")[0];
    var btn = getByClass(wrap, "button")[0];
    btn.className = "button exchange-button";

    function getTime(){var m = new Date().getMinutes(); var s = new Date().getSeconds(); var h = new Date().getHours(); return {h,m,s}}

    function createButton() {
        console.log("创建111")
        var button = getByClass(document.body, "left-icon f-c-c")[0];
        button.innerHTML = '领';
        button.addEventListener('click', startInterval);
    }
    var int=null;
    btn.click();

    function startInterval(){
        if (int){
            console.log("清除现有");
            clearInterval(int);
        }
        int = setInterval(
        function(){
            var gt = getTime();
            var m = gt.m;
            var s = gt.s;
            var h = gt.h;
            console.log(m, s);
            if ((m == 59 && s > 55) || m < 10){
                btn.click();
                console.log("submit");
            }
        }, 500);
    }
        '''
        time.sleep(5)
        driver.execute_script(script)



# SingleReward(task_id='6ERA1wloghvhw10', cookie_id='26326848')


if __name__ == "__main__":
    pool = []
    task_ids=["6ERA1wloghvhw100"]
    cookie_ids = CookieText.Bili.keys()
    for task_id in (task_ids):
        for cookie_id in cookie_ids:
            if not CookieText.Bili[cookie_id]['room_id']:
                continue
            s = SingleReward(task_id=task_id, cookie_id=cookie_id)
            # break
            pool.append(multiprocessing.Process(target=s.loop_in_web, args=()))
            # s.loop_in_web()
            # break

    for i in pool:
        time.sleep(2)
        i.start()
    for i in pool:
        i.join()

