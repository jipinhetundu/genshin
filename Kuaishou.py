
import requests
import pickle
import json
import time
import random
import multiprocessing
import datetime

class KuaishouReward:
    # 用来领取一个task_id对应的奖励
    def __init__(self):
        self.data = {
            # "client_key": "e0428a3f",
            # "kuaishou.live.mate_st": "ChVrdWFpc2hvdS5saXZlLm1hdGUuc3QSkAHX_Z1Umo2Iss-TZeUhd07SN52k0YtvTidykx_5mksTydfHq2XsDa2B-QVeOmTiE2AYFm3oDYVGiuCyMCkKBKx0Ui7aWJmklGM31CvaMBUoP2y4_d_CeN6q6yrAw5UHjSbY8aZFFSHb_p3tRFZsd5DDuCfnUflmJIXnO0BgqGM8Sx2vafel8YUmS_dnfoaWG8gaEkbIApOsckhmmh2wzxmhVom5ZyIgDtV4wxL27Tvm2cBetCp9yP_75PZLMs2MBFgvk2pYKBkoBTAB",
            "token": "38e7f911d633415c8d4e125e7b7b4214-3766912550",
            # "os": "android",
            # "sig": "df28126598633f005ca51404da88e125"
        }

    def check(self, care_task=None, ind=0, log=False):
        check_url = 'https://mate.gifshow.com/rest/n/live/mate/authortask/v2/my-tasks'
        session = requests.Session()
        response = session.post(check_url, data=self.data)
        task_info = json.loads(response.content)["tasks"]
        task = task_info[ind]
        if care_task:
            find= False
            for task in task_info:
                if task["taskId"] == int(care_task):
                    find = True
                    break
            if not find:
                print("未找到care_task !! 默认寻找最后一个")
        else:
            pass
            for t in task_info:
                print(t["taskId"], t["title"])
        # rewardStatus 0未完成 3已领取 5已抢光
        for sub_t in task["subTask"]:
            status = sub_t["rewardStatus"]
            # print(sub_t)
            if log: print(sub_t["title"], sub_t["completeRatio"], status, "剩余:", sub_t["remainNum"])
            # print(type(sub_t["recordId"]))
            # if sub_t["recordId"] == 0:
            #     for i in range(567873, 575621):
            #         time.sleep(1)
            #         pass
            #         self.reward(i + 4003000000)
            if status not in [0, 3, 5]:
                self.reward(sub_t["recordId"])
                print("可以抢")
        return task


    def reward(self, recordId):
        reward_url = f'https://mate.gifshow.com/rest/n/live/mate/authortask/drawReward?recordId={recordId}'
        session = requests.Session()
        response = session.post(reward_url, data=self.data)
        print(response.text)

    def regular_check(self, care_task, start_time):
        while True:
            start_dtime = datetime.datetime.combine(datetime.date.today(), start_time)
            if start_dtime < datetime.datetime.now() < start_dtime + datetime.timedelta(seconds=600):
                self.check(care_task=care_task, log=False)
                print("-", end="")
                time.sleep(1)
            else:
                time.sleep(30)
                print(".", end="")




if __name__ == "__main__":
    KS = KuaishouReward()
    KS.check(ind=3)
    KS.check(care_task=2657, log=True)
    KS.check(care_task=2717, log=True)
    KS.regular_check(care_task=2717, start_time=datetime.time(hour=0, minute=28, second=0))