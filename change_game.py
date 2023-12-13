import os

import requests
import json
import time
from kill_liveroom import terminate_process
import subprocess
import traceback
import CookieText





def change_json(changes, path=r'C:\Users\11201\AppData\Roaming\obs-studio\basic\profiles\未命名\obs-multi-rtmp.json'):
    with open(path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
        rtmp_data = json.loads(content)
    for name, new_server, new_key in changes:
        find = False
        for t in rtmp_data['targets']:
            if t['name'] == name:
                find = True
                break
        if not find:
            print("ERROR FIND ", name)
            return
        print(name, new_server, new_key)
        t['service-param']['key'] = new_key
        t['service-param']['server'] = new_server

    with open(path, 'w', encoding='utf-8-sig') as f:
        json.dump(rtmp_data, f, indent=2, ensure_ascii=False)




class HuyaLive:

    def __init__(self):
        self.headers = {
            'Authority': 'i.huya.com',
            'Method': 'GET',
            'Path': '/index.php?m=ProfileSetting&do=ajaxChangeLiveInfo&game_id=7349&live_desc=%E4%BC%9A%E6%96%9C%E7%9C%BC%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4',
            'Scheme': 'https',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://i.huya.com/index.php?m=ProfileSetting',
            'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        self.headers['Cookie'] = "SoundValue=0.50; alphaValue=0.80; game_did=NG5KDBMICCF-zyPmQt4guWk2v2KSdKieT52; isInLiveRoom=true; udb_guiddata=49f42fc980ef4c4c8a3defeea2847bec; guid=0adb8b9d917f78654c0163526452b199; udb_deviceid=w_787102223240482816; udb_anobiztoken=AQBGAia1fdN2Ieiw9Nd2T1SrFUx6yXxDkcYZ6EtpDPKhoxdYA7pW4t867zEDXRL7zv98LvyxXXM1q-lfP9WkkKpXDiCeck_83hOgGZK1hFKJJHpDLBORUzkK2nMUG1_fpJK8v_OQUYcx4D2jxnF3_opXvVwxU3atkhxtIze5u9mFhHF-bJ1YTzty0BUmhHWYrtFwFKQEtQMJJSzoDPudXhufdwK8rbRxDYOu27tbn4OGWEOiJ8Wv3UGnc761IOQFo3nHFadSX0nRcImfUVTqXenoHkzLeZwcmgUhFY6uTVuq0VKtPJ0pGYbJ3X6-HjlBv3x7wlHdCfJz8Sd1XVFxwRa-; udb_anouid=1466842898034; udb_passdata=3; __yasmid=0.16184999940654587; __yamid_tt1=0.16184999940654587; __yamid_new=CA8C7653CFC000019E1E3CDE1C901E14; sdidshorttest=test; sdid=0UnHUgv0_qmfD4KAKlwzhqbV7C5n2cUq8RqHhqosi08ngz3Pr3pWy5g6WBp1MB8sTwdvJioUkyl27CF_AlMMiD90mXCS3eJvSaPC1wWJOEtHWVkn9LtfFJw_Qo4kgKr8OZHDqNnuwg612sGyflFn1djYK8RQdh_qaRiK0cGNnqYSwHixp6BsckgkZDiOUDYyA; sdidtest=0UnHUgv0_qmfD4KAKlwzhqbV7C5n2cUq8RqHhqosi08ngz3Pr3pWy5g6WBp1MB8sTwdvJioUkyl27CF_AlMMiD90mXCS3eJvSaPC1wWJOEtHWVkn9LtfFJw_Qo4kgKr8OZHDqNnuwg612sGyflFn1djYK8RQdh_qaRiK0cGNnqYSwHixp6BsckgkZDiOUDYyA; Hm_lvt_51700b6c722f5bb4cf39906a596ea41f=1702395797; _rep_cnt=2; udb_biztoken=AQA7_oLXe0aGnjhXJ1tuzVqR2RqVEPvlgCZARhv01WlOyjJEL8pzA58fQ-59be6by-hxyP70Gm8UcV4BLmEWNb4dO2kxbB-Ev4bkSIceY0Pd9Cg3hcd1cPYqygJidWLLZ822xvG-Lqsi0ovnX6ACcOAkAX-xE5ukJN0ARQ8UynoNG7IiIEsJTT6fedWls10kgMrX3qiH07WGJNReLFJjMYqewXeiWp5uoFOzet7tQXz8DcxizuengqlC3DLuwA2BQsippi1Q3ySjWM3EWRFZccsQNNmZYmMD1geobYdO02o5mJnGXJCL1VxWJ57gYddsT8uBsToDbTb7HJSNDEehXDgW; udb_cred=CjBMbaS83luaAqd7z01fBgFIf5RzAJEBE4yYJwZUstXl-DmI6LC-nyrwFPf7o5aO1jRZ6d1svRNf8LEc-il6vxOTDUUCXrH0Hc9ep9fAYwuGW07XWPUkRmrRpHUkU1sm0YZzU0QQ1NfFl2rOgumvNhN3; udb_origin=0; udb_passport=hy_236945444; udb_status=1; udb_uid=1199624303734; udb_version=1.0; username=hy_236945444; yyuid=1199624303734; udb_accdata=undefined; h_unt=1702395810; __yaoldyyuid=1199624303734; _yasids=__rootsid%3DCA8C7657DB60000146D54CA4C8A01D89; rep_cnt=17; PHPSESSID=4hrk63c34sn59aeqna750occt2; guid=0adb8b9d917f78654c0163526452b199; undefined=undefined; first_username_flag=hy_236945444_first_1; Hm_lpvt_51700b6c722f5bb4cf39906a596ea41f=1702395836; huya_ua=webh5&0.0.1&activity; huya_flash_rep_cnt=35; huya_hd_rep_cnt=11; huya_web_rep_cnt=100"

    def change_game(self, game_id=7349):
        change_url = f"https://i.huya.com/index.php?"\
                     f"m=ProfileSetting&do=ajaxChangeLiveInfo&game_id={game_id}&"\
                     f"live_desc=%E4%BC%9A%E6%96%9C%E7%9C%BC%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4"
        response = self.session.get(change_url)
        cnt = json.loads(response.content)
        if cnt['status'] == 500:
            print('虎', change_url, ['msg'], "原" if game_id == 5489 else "崩")
        else:
            print('虎成功', "原" if game_id == 5489 else "崩")

    def start_live(self, game="原"):
        if game == "gen":
            game_id = 5489
        elif game == "sr":
            game_id = 7349
        else:
            print("ERROR IN GAME ID !")
            return
        self.change_game(game_id)
        start_url = f'https://i.huya.com/index.php?m=ProfileSetting&do=ajaxGetOpenRtmpAddr&game_id={game_id}&live_desc=%E4%BC%9A%E6%96%9C%E7%9C%BC%E7%9A%84%E7%9B%B4%E6%92%AD%E9%97%B4&game_name=%E5%8E%9F%E7%A5%9E&live_flag=0&read_only=0'
        response = self.session.get(start_url)
        print(json.loads(response.content))
        data = json.loads(response.content)['data']
        print('虎牙，', game, data['rtmpKey'])
        return "虎牙", data['rtmpAddr'], data['rtmpKey']

    def kill_live(self):
        kill_url = 'https://i.huya.com/index.php?m=ProfileSetting&do=ajaxOpenRtmpEndLive'
        response = self.session.get(kill_url)
        print(json.loads(response.content))

bili_headers = {
    # 'Host': 'api.live.bilibili.com',
    'method': 'GET',
    'path': '/xlive/web-ucenter/user/live_info',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en',
    'Cache-Control': 'max-age=0',
    'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
}

class BiliOther:

    def __init__(self, cookie, room_id):
        self.session = requests.Session()
        self.session.headers = bili_headers.copy()
        self.session.headers['Cookie'] = cookie
        self.csrf = self.session.headers['Cookie'].split("bili_jct=")[1].split(";")[0]
        room = self.session.get('https://api.live.bilibili.com/xlive/web-ucenter/user/live_info')
        # print(json.loads(room.content))
        time.sleep(1)
        if json.loads(room.content)['code'] != 0:
            print("申请房间信息出错，使用默认!!--Others")
            self.room_id = room_id
        else:
            self.room_id = json.loads(room.content)['data']['room_id']
    def change_game(self, game_id):
        # url = f'https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch?platform=pc&area_parent_id=3&area_id={game_id}'
        response = self.session.get(f'https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch?platform=pc&area_parent_id=3&area_id={game_id}')
        print(json.loads(response.content))

    def start_live(self, game):
        if game == "gen":
            game_id = 321
        elif game == 'sr':
            game_id = 549
        else:
            print("ERROR IN GAME")
            return
        self.change_game(game_id)
        start_url = 'https://api.live.bilibili.com/room/v1/Room/startLive'

        post_data = {
            'room_id': self.room_id,
            'area_v2': game_id,
            'csrf': self.csrf,
            'csrf_token': self.csrf,
            'backup_stream': 0,
            'platform': 'pc'
        }


        response = self.session.post(start_url, data=post_data)
        data = json.loads(response.content)['data']
        print(data['rtmp'])
        return 'bili', data['rtmp']['addr'], data['rtmp']['code']

        # room_id: 26326848
        # platform: pc
        # area_v2: 549
        # backup_stream: 0

    def kill_live(self):
        post_data = {
            'room_id': self.room_id,
            'csrf': self.csrf,
            'csrf_token': self.csrf,
            'platform': 'pc'
        }
        # print(post_data)
        response = self.session.post('https://api.live.bilibili.com/room/v1/Room/stopLive', data=post_data)
        print(json.loads(response.content))
class BiliLive:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = bili_headers.copy()
        self.session.headers['Cookie'] = CookieText.Bili['26326848']
        self.csrf = self.session.headers['Cookie'].split("bili_jct=")[1].split(";")[0]
        time.sleep(1)
        room = self.session.get('https://api.live.bilibili.com/xlive/web-ucenter/user/live_info')
        # print(json.loads(room.content), 11111111)
        if json.loads(room.content)['code'] != 0:
            print("申请房间信息出错，使用默认")
            self.room_id = '26326848'
        else:
            self.room_id = json.loads(room.content)['data']['room_id']



    def change_game(self, game_id):
        # url = f'https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch?platform=pc&area_parent_id=3&area_id={game_id}'
        response = self.session.get(f'https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch?platform=pc&area_parent_id=3&area_id={game_id}')
        print(json.loads(response.content))

    def start_live(self, game):
        if game == "gen":
            game_id = 321
        elif game == 'sr':
            game_id = 549
        else:
            print("ERROR IN GAME")
            return
        self.change_game(game_id)
        start_url = 'https://api.live.bilibili.com/room/v1/Room/startLive'

        post_data = {
            'room_id': self.room_id,
            'area_v2': game_id,
            'csrf': self.csrf,
            'csrf_token': self.csrf,
            'backup_stream': 0,
            'platform': 'pc'
        }

        response = self.session.post(start_url, data=post_data)
        data = json.loads(response.content)['data']
        print(data['rtmp'])
        return 'bili', data['rtmp']['addr'], data['rtmp']['code']

        # room_id: 26326848
        # platform: pc
        # area_v2: 549
        # backup_stream: 0

    def kill_live(self):
        post_data = {
            'room_id': self.room_id,
            'csrf': self.csrf,
            'csrf_token': self.csrf,
            'platform': 'pc'
        }
        response = self.session.post('https://api.live.bilibili.com/room/v1/Room/stopLive', data=post_data)
        print(json.loads(response.content))


class DouyuLive:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'Authority': 'www.douyu.com',
            'Method': 'POST',
            'Path': '/japi/creator/w/apinc/live/pushflow/openShow',
            'Scheme': 'https',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en',
            'Baggage': 'sentry-environment=master,sentry-public_key=aa6a729218ad4f47ba54c250d5d6a871,sentry-trace_id=7dc907eb80bc4908af037d4a7c7ce5e8',
            # 'Content-Length': '86',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'dy_did=fcb8b348b5661e3f118dcb6800071701; acf_did=fcb8b348b5661e3f118dcb6800071701; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1701775860; PHPSESSID=nrqfvg24mpsj34v35nucq4ah73; acf_auth=39a9kJXVKXle3P7p3%2FmT%2B17PURndgEI%2B7E5%2B%2BC4PGYfR%2FS%2BdtayMVDtGxA60%2FR3xiUl3Ej1J6V3nGzRJe%2BYgGWntN8CXjzTVKKKzYa56mzicvPhkVp920SM; dy_auth=6c4a8AnZt4IU8O5LXMOk4%2BmDrH8tXa1uaD81MOZeRo3zAWcseI2%2BH3qBofjDG37Pm5z8STowKxQN7Dg5fMCK44iKyHEJuqYKtkoIG9Hxmd723DAbPX1DD64; wan_auth37wan=efe965d87102gOZ3%2B5J4YaYiugEn6rGrljVGprb0cFU7g4GG0rsgj0ExDuOnUWtmC3pwMpJIFUxRmFnUm1aA38PI6IJ4h%2BA0o7DhSGPnrY%2BP3EvlyuM; acf_uid=491004513; acf_username=491004513; acf_nickname=%E8%9D%97%E7%81%BE%E5%A4%AA%E8%BD%BB%E6%9D%BE%E4%BA%86; acf_own_room=1; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2Fdefault%2F21_; acf_ct=0; acf_ltkid=22214460; acf_biz=1; acf_stk=459a6dff90a76ed5; acf_isNewUser=1; dy_teen_mode=%7B%22uid%22%3A%22491004513%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; acf_ccn=b9e60b0a6533a9ce4f895749ab5a1876; dy_did=fcb8b348b5661e3f118dcb6800071701; acf_ctn=4a5a879372f8d8d280ef088f97d00762; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1701775973',
            'Origin': 'https://www.douyu.com',
            'Referer': 'https://www.douyu.com/creator/main/live',
            'Sec-Ch-Ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sentry-Trace': '7dc907eb80bc4908af037d4a7c7ce5e8-a6bdf7682ce2e18e-0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }

        self.session.headers['Cookie'] = 'Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1702396282; dy_did=f03342b1e57240cda4dcbc4d00031701; acf_did=f03342b1e57240cda4dcbc4d00031701; dy_did=f03342b1e57240cda4dcbc4d00031701; PHPSESSID=80c6tq9pddkt0c3ctn8rch60g1; acf_auth=5e84EZ5wX0PFJ6CQqxjrMkbApZSDt%2FyTneGPQJQlVCNs4kPGeJbQFWZFbnCYhYYh%2FoRYJRLBmhnbn078f0QlgiBZM4QQVmCpPGFuxFRSssPGV9vMb0H%2FFEw; dy_auth=6149CF3jxfSdqR8Z1UYPu3TiVtlUouV0%2FZKMVArHmcSZ1AtKz3mNOAssgMhLaCuyacTQNW83XsAAmmgCwbTimVqDO3rfZ3YdmnOF9KUhCOL3YY7xJsDgP9Y; wan_auth37wan=9def132f1d82RY3PV497o6xqvnxfTOG2A4JKp5B4rphA0SRL3ajfkapYOIuXP0Ndrr2WS82i2U3tXJSo%2BYpUwC%2B5zZAyPqtpHnKPgCUWcpeAtiP7rb4; acf_uid=491004513; acf_username=491004513; acf_nickname=%E8%9D%97%E7%81%BE%E5%A4%AA%E8%BD%BB%E6%9D%BE%E4%BA%86; acf_own_room=1; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favatar%2Fdefault%2F21_; acf_ct=0; acf_ltkid=22214463; acf_biz=1; acf_stk=bd0afd791a5c8b61; acf_isNewUser=1; dy_teen_mode=%7B%22uid%22%3A%22491004513%22%2C%22status%22%3A0%2C%22birthday%22%3A%22%22%2C%22password%22%3A%22%22%7D; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1702396316; acf_ctn=cc5bb6d8931f07c1bc5b8e8ccb96959c; acf_ccn=3543a3a401d778e2929f30fd30fd5f3f'
        # 没问题，官方就是ccn和ctn反着传的，不是我写错了。
        self.ctn = self.session.headers['Cookie'].split('acf_ccn=')[1].split(';')[0]
        self.ccn = self.session.headers['Cookie'].split('acf_ctn=')[1].split(';')[0]



    def change_game(self, game_name='星穹铁道'):
        try:
            c2_url = f'https://www.douyu.com/japi/creator/w/apinc/live/cate/fuzzyC2Info?c2name={game_name}'
            game_id = json.loads(self.session.get(c2_url).content)['data']['cate1List'][0]['cate2Id']
            c3_url = f'https://www.douyu.com/japi/creator/w/apinc/live/cate/getC3List?cid2={game_id}'
            cid3 = json.loads(self.session.get(c3_url).content)['data'][0]['id']
        except Exception:
            traceback.print_exc()
        # url = f'https://api.live.bilibili.com/xlive/app-blink/v1/index/getNewRoomSwitch?platform=pc&area_parent_id=3&area_id={game_id}'
        data ={
            'cid2': game_id,
            'cid3': cid3,
            'ctn': self.ctn,
            'ccn': self.ccn
        }
        response = self.session.post(f'https://www.douyu.com/japi/creator/w/apinc/live/category/editCategoryByRid', data=data)
        # print(json.loads(response.content))

    def start_live(self, game):
        if game == "gen":
            game_name = '原神'
        elif game == 'sr':
            game_name = '星穹铁道'
        else:
            print("ERROR IN GAME")
            return
        self.change_game(game_name)
        start_url = 'https://www.douyu.com/japi/creator/w/apinc/live/pushflow/openShow'

        post_data = {
            'notshowtip': 0,
            'ctn': self.ctn,
            'ccn': self.ccn
        }

        response = self.session.post(start_url, data=post_data)
        time.sleep(1)
        response = self.session.get('https://www.douyu.com/japi/creator/w/apinc/live/pushflow/getRtmp')
        data = json.loads(response.content)['data']
        print('斗鱼，', game, data['rtmpVal'])
        return 'douyu', data['rtmpUrl'], data['rtmpVal']

        # room_id: 26326848
        # platform: pc
        # area_v2: 549
        # backup_stream: 0

    def kill_live(self):
        post_data = {
            'ctn': self.ctn,
            'ccn': self.ccn
        }
        response = self.session.post('https://www.douyu.com/japi/creator/w/apinc/live/pushflow/closeShow', data=post_data)
        print(json.loads(response.content))




obs_json_path = r'C:\Users\11201\AppData\Roaming\obs-studio\basic\profiles\未命名\obs-multi-rtmp.json'

# cookies = {
#     "31513203":'innersign=0; buvid3=6C504CE9-876B-9B5D-AE22-3AF53D16CCC229026infoc; b_nut=1702395329; i-wanna-go-back=-1; b_ut=7; _uuid=869481FE-149D-10247-4A79-2BC1A110EF22E28581infoc; enable_web_push=DISABLE; header_theme_version=undefined; home_feed_column=5; browser_resolution=1536-715; buvid4=084633FE-35AC-E39A-4837-3BB22E19A1C530498-023121215-; SESSDATA=795bcff7%2C1717947341%2Cf642f%2Ac2CjAN-kOMbOjQ8JqtQtQj_aT94VaFgMDXvaZuapig3sLXfZv_OFrdKWOwVRX06kW_glcSVks3VzlHemhGTlRTNWdiQzE0YVFWTXA5Qjh0UkVQa2FhYjJSeHJHNVRkVWpWZ1pDcVY4MzItR1Z2TVVJMV9SZnBlLTZNV3NRaFZDUkFRcWRCSkcyQm9nIIEC; bili_jct=0135d438a937ad0823d28afe1542477d; DedeUserID=3546375247629156; DedeUserID__ckMd5=b91cfd36461d1a26; fingerprint=81c65a80e4168f917cf348465bc99636; buvid_fp_plain=undefined; buvid_fp=81c65a80e4168f917cf348465bc99636; CURRENT_FNVAL=4048; sid=6q0tl5eo; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2NTQ2MDgsImlhdCI6MTcwMjM5NTM0OCwicGx0IjotMX0.5RMHzEfBhKdbevTKmY2aP2j1dy0dM2NJQRgeAQo6YmA; bili_ticket_expires=1702654548; PVID=1; LIVE_BUVID=AUTO6917023954132301; b_lsid=B106D726E_18C5EC26718',
#     "31393092":"buvid3=A0DBBBB7-AFC0-317E-2D9B-A26E67CB0A8523840infoc; b_nut=1702399823; i-wanna-go-back=-1; b_ut=7; b_lsid=A1FEC57E_18C5EEFCE53; _uuid=57C5E292-9BB10-5CC7-2822-1B4FCFC7645523488infoc; CURRENT_FNVAL=4048; buvid4=F71822CB-3C82-50AE-898D-C32AA47D669F25306-023121216-; rpdid=|(k|~u~YuJl)0J'u~|kJmm)kY; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2NTk1MDksImlhdCI6MTcwMjQwMDI0OSwicGx0IjotMX0.TnxjtYLOBozgepkUQ3y88ZFxRsAapXw-UXnDPFAxy20; bili_ticket_expires=1702659449; SESSDATA=10932e94%2C1717952484%2Cfd631%2Ac1CjCJuewuVURm_DULyR6CJer5vIoMCa_brvFj4sI49FzQp-hU6Gm7JmHDk05YKoMcDVwSVlhaN2MxcjhVMGdXUS15czlhY2M1OFNqSS14UUJ6UFlHWVZJMkdsT3JvcnE0cWFvaElkSGVPS2VIeVhHZHFSVkFNLVFuLVhWbnNUaFZBZlUxRHdfYmxnIIEC; bili_jct=4c778cbf63c4af1772417171e64c9133; DedeUserID=416926781; DedeUserID__ckMd5=076139969a7a5b15; sid=ej0zprd7; fingerprint=81c65a80e4168f917cf348465bc99636; buvid_fp=783459E4-24FD-DB81-44CC-6C5C6DDBEAC361086infoc; buvid_fp_plain=undefined"
# }

enable = {
   # 'bili': (BiliLive(), 'sr'),
   # 'huya': (HuyaLive(), 'sr'),
   #  'douyu': (DouyuLive(),'sr'),
#     'bili': (BiliLive(), 'gen'),
    'huya': (HuyaLive(), 'gen'),
    'douyu': (DouyuLive(),'gen'),
}

enable['bili2'] = (BiliOther(cookie=CookieText.Bili["31513203"]['Cookie'], room_id="31513203"), 'sr')
enable['bili3'] = (BiliOther(cookie=CookieText.Bili["31393092"]['Cookie'], room_id="31393092"), 'sr')
new_data = []
print("-----")
plats = enable.keys()

def start(shut_obs=True):
    if shut_obs:
        stop()
        terminate_process('OBS')
    # 开播
    for l in plats:
        try:
            new_data.append(enable[l][0].start_live(enable[l][1]))
            print(f'!!!!!!!!{enable[l][0]} 开始 {enable[l][1]}!!!!!!!!!')
        except Exception as e:
            print(e)
            traceback.print_exc()
    if shut_obs:
        change_json(new_data)
        # 启动目标EXE文件
        os.chdir(r'D:\Program Files\obs-studio\bin\64bit')
        subprocess.Popen(r'obs64.exe')

def stop():
    # 关播
    for l in plats:
        try:
            enable[l][0].kill_live()
        except Exception as e:
            print(e)
            traceback.print_exc()


if __name__ == "__main__":
    start(shut_obs=True)
    # pass
    # stop()
    # r = BiliLive().start_live('sr')
    # print(r)
    # BiliLive().change_game()
    # HuyaLive().kill_live()
    # print(1)