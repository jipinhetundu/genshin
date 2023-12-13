import requests
import pickle
import json
import time
import random
import multiprocessing
import datetime


class DouyuReward:
    # 用来领取一个task_id对应的奖励
    def __init__(self, task_ids):
        self.single_task_url = "https://www.douyu.com/japi/carnival/nc/web/roomTask/getPrize"
        cookie_str = \
           'dy_did=e1256365eb7c00518f01e91a00021601; acf_did=e1256365eb7c00518f01e91a00021601; acf_isNewUser=1; dy_teen_mode=%7B%22uid%22%3A%22491004513%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; dy_did=e1256365eb7c00518f01e91a00021601; PHPSESSID=ncn7h47bb5dfhjhr8o0smme7n4; acf_auth=ac87YrsovMpq6VrAVFr%2F9efXhOsCJj0IkO4r1Kpjo4bhMSnmO2liA7BoeRMs3L9tn9Ek58XylBkHNj0tPd%2Bfbm7dQMVT1ZVDuAGkMwZWMSaRKMPHDyECVbk; dy_auth=eafcqdCvo%2FQ07Y3KZlCvI8KH%2BCoYaPw%2BY75EW8%2FdMQtJGxf4q%2FXNdLzLTZ30pLixyQE%2Frpq%2BvuxlvF8pprwWEVXxM79FEVuSz8cCwveiYXIzD8G1QztNfIM; wan_auth37wan=adbf94c1cf00zLW66autcXuGMGPEZ4ummPLGyDzjLcG1qOGK2SQZoeWQCo7VcohAy6noklMdlKwoWvO9DosQTOSFOvUXmkJbz9JEX1KZkg7KFriiLtg; acf_uid=491004513; acf_username=491004513; acf_nickname=%E8%9D%97%E7%81%BE%E5%A4%AA%E8%BD%BB%E6%9D%BE%E4%BA%86; acf_own_room=1; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2Fdefault%2F21_; acf_ct=0; acf_ltkid=22214451; acf_biz=1; acf_stk=a763c5e02e80446c; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1701621349,1701872889,1701878234,1702107712; acf_ccn=2e847f613951e3065d90f57525cb9a04; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1702107734; cvl_csrf_token=64d25e888f504a40bb776ff5c1b13164'
        self.headers = {
            "Cookie": cookie_str}
        # self.headers = {
        #     "Cookie": "dy_did=5e185db95f9c14746543639200021701;"
        #               " acf_auth=17081KTXkIP7WbqEjYvjKYTBMSzLNe1A53MHuaUrsP7epe%2FLG0U6zb%2F9rCS1FmJh5Pg94J%2BmBtvC3gsbziXBbmmVuD4ey7xHACKPFY71CWsgpoWgjgR3HNU;"
        #               " acf_uid=491004513;"
        #               " acf_ltkid=22214458;"
        #               " acf_stk=d8dbbf7ac9badd70;"
        # }
        self.task_ids = task_ids

    def test_day_ok_last(self, last_task_id="241272", start_days=datetime.date(year=2023, month=11, day=8)):
        now_days = datetime.datetime.now().date() - start_days
        now_days = now_days.days + 1
        session = requests.Session()
        response = session.post(self.single_task_url, data={"taskId": last_task_id},
                                headers=self.headers)
        # print(json.loads(response.content))
        try:
            cur = json.loads(response.content)["data"]["taskStatus"]["condCompleteList"][0]["num"]
        except KeyError:
            return json.loads(response.content)["msg"]
        return "All pass" if cur == now_days else "斗 原 未完成！\n"

    def test_day_ok_sing(self, task_ids):
        session = requests.Session()
        res = ""
        for task_id in task_ids:
            response = session.post(self.single_task_url, data={"taskId": task_id},
                                    headers=self.headers)
            e = json.loads(response.content)["error"]
            if e != 0 and e != 1004 and e != 2002:
                res += f'{e}, {json.loads(response.content)["msg"]}\n'
                # print(res)
        return "All pass" if not res else "斗 铁 未完成！\n"

    def check(self, g=True, s=True,
              last_task_id="241272", start_days=datetime.date(year=2023, month=11, day=8),
              task_ids=["242519", "242521", "242522", "242524"]):
        post_text = ""
        # 原
        g_status = self.test_day_ok_last(last_task_id=last_task_id, start_days=start_days)
        # 铁
        s_status = self.test_day_ok_sing(task_ids=task_ids)
        if g_status != "All pass" and g:
            post_text += g_status
        if s_status != "All pass" and s:
            post_text += s_status
        return post_text

    def getPrize(self, taskid, hour=6, min=0, sec=0):
        session = requests.Session()
        start_time = datetime.datetime.combine(datetime.datetime.now().date(), datetime.time(hour=hour, minute=min, second=sec))
        sec20 = datetime.timedelta(seconds=20)
        min2 = datetime.timedelta(seconds=120)
        # print(start_time, sec5, start_time - sec5, start_time + min2)

        while True:
            now_time = datetime.datetime.now()

            if (start_time - sec20 < now_time < start_time + min2):
                response = session.post(self.single_task_url, data={"taskId": taskid},
                                        headers=self.headers)
                print(response.text)
                time.sleep(0.5)
            else:
                time.sleep(20)
                start_time = datetime.datetime.combine(datetime.datetime.now().date(),
                                                       datetime.time(hour=hour, minute=min, second=sec))

                print(".", end="")


if __name__ == "__main__":
    c = DouyuReward("")
    c.check()
    # c.getPrize(taskid="241388", hour=0, min=29, sec=55)
    c.getPrize(taskid="241270", hour=0, min=59, sec=55)



