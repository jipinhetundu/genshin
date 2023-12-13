def parse_cookie(cookie_str):
    cookie_dict = {}
    items = cookie_str.split('; ')

    for item in items:
        key, value = item.split('=', 1)
        cookie_dict[key] = value

    return cookie_dict

Bili = dict()

Bili['26326848'] = {
    'room_id': '26326848',
    'name': '赶快改名保命',
    # 'Cookie': "LIVE_BUVID=AUTO4715860026148713; buvid4=0E36E6C0-EEF7-A6B8-6E5D-E565D4E7979296292-022012521-bLBnUTnxriDSYoWSQjmLMg%3D%3D; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; buvid_fp_plain=undefined; rpdid=|(k|))~uu)Jl0J'uYY)l)kRkR; CURRENT_FNVAL=16; b_ut=5; header_theme_version=CLOSE; nostalgia_conf=-1; CURRENT_PID=da823200-cd40-11ed-8ff9-ed7db7cab5f8; buvid3=783459E4-24FD-DB81-44CC-6C5C6DDBEAC361086infoc; b_nut=1680625861; _uuid=F91104F66-661F-8F1A-F2610-BBAFE10EB831902537infoc; hit-new-style-dyn=1; FEED_LIVE_VERSION=V8; go_old_video=-1; hit-dyn-v2=1; CURRENT_QUALITY=80; DedeUserID=484436716; DedeUserID__ckMd5=a9b6c1e772d4c34c; home_feed_column=5; enable_web_push=DISABLE; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1701169555,1701264613,1701436317,1701772727; fingerprint=81c65a80e4168f917cf348465bc99636; browser_resolution=1536-715; SESSDATA=5d94d51e%2C1717743482%2C05c2c%2Ac1CjAsG-Yl-LrRo0SA9C5cDoeecLjGfbF496YWfIH3BlG-E_q71yXh9bjBY8pHS7-cktESVklMTFQtTmZGYmtfUXhpVXdQV2hxN1dvWHJxaWJCSDZCamN1QWRJNzlFVnNyblhPcG5vU21GVlBYenBETnBTbVVzVEZoUUhHaWxtOUdlbExGcFFGQ1BBIIEC; bili_jct=6b2aaba9145a282406cfd01f0f8807e8; bp_video_offset_484436716=873464599906615313; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI0ODU3ODEsImlhdCI6MTcwMjIyNjUyMSwicGx0IjotMX0.BYZm7vn8zcUpijKsx3zp_D-9X9rlxbT1xLSfqQDgDsY; bili_ticket_expires=1702485721; buvid_fp=81c65a80e4168f917cf348465bc99636; innersign=0; sid=h2kdj417; PVID=1; b_lsid=4BE42942_18C5EC2670B"
    'Cookie': "LIVE_BUVID=AUTO4715860026148713; buvid4=0E36E6C0-EEF7-A6B8-6E5D-E565D4E7979296292-022012521-bLBnUTnxriDSYoWSQjmLMg%3D%3D; CURRENT_BLACKGAP=0; i-wanna-go-back=-1; buvid_fp_plain=undefined; rpdid=|(k|))~uu)Jl0J'uYY)l)kRkR; CURRENT_FNVAL=16; b_ut=5; header_theme_version=CLOSE; nostalgia_conf=-1; CURRENT_PID=da823200-cd40-11ed-8ff9-ed7db7cab5f8; buvid3=783459E4-24FD-DB81-44CC-6C5C6DDBEAC361086infoc; b_nut=1680625861; _uuid=F91104F66-661F-8F1A-F2610-BBAFE10EB831902537infoc; hit-new-style-dyn=1; FEED_LIVE_VERSION=V8; go_old_video=-1; hit-dyn-v2=1; CURRENT_QUALITY=80; DedeUserID=484436716; DedeUserID__ckMd5=a9b6c1e772d4c34c; home_feed_column=5; enable_web_push=DISABLE; fingerprint=81c65a80e4168f917cf348465bc99636; browser_resolution=1536-715; SESSDATA=5d94d51e%2C1717743482%2C05c2c%2Ac1CjAsG-Yl-LrRo0SA9C5cDoeecLjGfbF496YWfIH3BlG-E_q71yXh9bjBY8pHS7-cktESVklMTFQtTmZGYmtfUXhpVXdQV2hxN1dvWHJxaWJCSDZCamN1QWRJNzlFVnNyblhPcG5vU21GVlBYenBETnBTbVVzVEZoUUhHaWxtOUdlbExGcFFGQ1BBIIEC; bili_jct=6b2aaba9145a282406cfd01f0f8807e8; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI0ODU3ODEsImlhdCI6MTcwMjIyNjUyMSwicGx0IjotMX0.BYZm7vn8zcUpijKsx3zp_D-9X9rlxbT1xLSfqQDgDsY; bili_ticket_expires=1702485721; innersign=0; PVID=2; sid=8cnckk0i; bp_video_offset_484436716=874296517875204113; buvid_fp=2a6d69ab418362d1b7f5b6ff9f248fed; b_lsid=B738A92A_18C5F69071A; x-bili-gaia-vtoken=16209de9e5c94157a869660ad4c2e7cb"
}

Bili["31513203"] = {
    'room_id': "31513203",
    'name': '另一个蒙昧的春天',
    'Cookie': "innersign=0; buvid3=6C504CE9-876B-9B5D-AE22-3AF53D16CCC229026infoc; b_nut=1702395329; i-wanna-go-back=-1; b_ut=7; _uuid=869481FE-149D-10247-4A79-2BC1A110EF22E28581infoc; enable_web_push=DISABLE; header_theme_version=undefined; home_feed_column=5; browser_resolution=1536-715; buvid4=084633FE-35AC-E39A-4837-3BB22E19A1C530498-023121215-; SESSDATA=795bcff7%2C1717947341%2Cf642f%2Ac2CjAN-kOMbOjQ8JqtQtQj_aT94VaFgMDXvaZuapig3sLXfZv_OFrdKWOwVRX06kW_glcSVks3VzlHemhGTlRTNWdiQzE0YVFWTXA5Qjh0UkVQa2FhYjJSeHJHNVRkVWpWZ1pDcVY4MzItR1Z2TVVJMV9SZnBlLTZNV3NRaFZDUkFRcWRCSkcyQm9nIIEC; bili_jct=0135d438a937ad0823d28afe1542477d; DedeUserID=3546375247629156; DedeUserID__ckMd5=b91cfd36461d1a26; fingerprint=81c65a80e4168f917cf348465bc99636; buvid_fp_plain=undefined; buvid_fp=81c65a80e4168f917cf348465bc99636; CURRENT_FNVAL=4048; sid=6q0tl5eo; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2NTQ2MDgsImlhdCI6MTcwMjM5NTM0OCwicGx0IjotMX0.5RMHzEfBhKdbevTKmY2aP2j1dy0dM2NJQRgeAQo6YmA; bili_ticket_expires=1702654548; PVID=1; LIVE_BUVID=AUTO6917023954132301; b_lsid=B106D726E_18C5EC26718"
}

Bili["31393092"] = {
    'room_id': "31393092",
    'name': 'xflmnm',
    # 'Cookie': "buvid3=A0DBBBB7-AFC0-317E-2D9B-A26E67CB0A8523840infoc; b_nut=1702399823; i-wanna-go-back=-1; b_ut=7; b_lsid=A1FEC57E_18C5EEFCE53; _uuid=57C5E292-9BB10-5CC7-2822-1B4FCFC7645523488infoc; CURRENT_FNVAL=4048; buvid4=F71822CB-3C82-50AE-898D-C32AA47D669F25306-023121216-; rpdid=|(k|~u~YuJl)0J'u~|kJmm)kY; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2NTk1MDksImlhdCI6MTcwMjQwMDI0OSwicGx0IjotMX0.TnxjtYLOBozgepkUQ3y88ZFxRsAapXw-UXnDPFAxy20; bili_ticket_expires=1702659449; SESSDATA=10932e94%2C1717952484%2Cfd631%2Ac1CjCJuewuVURm_DULyR6CJer5vIoMCa_brvFj4sI49FzQp-hU6Gm7JmHDk05YKoMcDVwSVlhaN2MxcjhVMGdXUS15czlhY2M1OFNqSS14UUJ6UFlHWVZJMkdsT3JvcnE0cWFvaElkSGVPS2VIeVhHZHFSVkFNLVFuLVhWbnNUaFZBZlUxRHdfYmxnIIEC; bili_jct=4c778cbf63c4af1772417171e64c9133; DedeUserID=416926781; DedeUserID__ckMd5=076139969a7a5b15; sid=ej0zprd7; fingerprint=81c65a80e4168f917cf348465bc99636; buvid_fp=783459E4-24FD-DB81-44CC-6C5C6DDBEAC361086infoc; buvid_fp_plain=undefined"
    'Cookie': "innersign=0; buvid3=F025A220-AF82-B1E4-DE9E-D5FD5461F75C29875infoc; b_nut=1702406629; i-wanna-go-back=-1; b_ut=7; b_lsid=56DF5E61_18C5F57A7BC; _uuid=EDB3C7108-5CD5-CC36-9110E-FDFE98C610C81029331infoc; enable_web_push=DISABLE; header_theme_version=undefined; buvid4=E033B21A-185A-A2E1-0EC0-5AFCDA30E67E30430-023121218-; home_feed_column=5; browser_resolution=1536-715; SESSDATA=03d0ada6%2C1717958713%2C7911d%2Ac1CjDZaYHm51XnEZQ3nmDbT5airZ8T9PgBOkR-R_aPfHT8D2woZm-ZhbQyOlScCdM-EJMSVjNUUklCdnByM0YzLXZzU0JSeXo2MGVPRW1tS0g2YXh6WnFsQlBFODV6dDE1cUk3b0pmNTBtamdfeExtY2g2M1IwLUo1OUZkY19YUExNek14SkpfbEV3IIEC; bili_jct=db8cf78a960a9036f518e6a8b9373442; DedeUserID=416926781; DedeUserID__ckMd5=076139969a7a5b15; fingerprint=81c65a80e4168f917cf348465bc99636; buvid_fp_plain=undefined; buvid_fp=81c65a80e4168f917cf348465bc99636; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2NjU5MjUsImlhdCI6MTcwMjQwNjY2NSwicGx0IjotMX0.JzJpbSAjUTIOt9VGI1M6rxn7Hgk1kVlJwIwy-L73zmk; bili_ticket_expires=1702665865; sid=5z4ramku"
}

Bili["smile-67709"] = {
    'room_id': "",
    'name': 'smile-67709',
    # 'Cookie': "buvid3=A0DBBBB7-AFC0-317E-2D9B-A26E67CB0A8523840infoc; b_nut=1702399823; i-wanna-go-back=-1; b_ut=7; b_lsid=A1FEC57E_18C5EEFCE53; _uuid=57C5E292-9BB10-5CC7-2822-1B4FCFC7645523488infoc; CURRENT_FNVAL=4048; buvid4=F71822CB-3C82-50AE-898D-C32AA47D669F25306-023121216-; rpdid=|(k|~u~YuJl)0J'u~|kJmm)kY; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI2NTk1MDksImlhdCI6MTcwMjQwMDI0OSwicGx0IjotMX0.TnxjtYLOBozgepkUQ3y88ZFxRsAapXw-UXnDPFAxy20; bili_ticket_expires=1702659449; SESSDATA=10932e94%2C1717952484%2Cfd631%2Ac1CjCJuewuVURm_DULyR6CJer5vIoMCa_brvFj4sI49FzQp-hU6Gm7JmHDk05YKoMcDVwSVlhaN2MxcjhVMGdXUS15czlhY2M1OFNqSS14UUJ6UFlHWVZJMkdsT3JvcnE0cWFvaElkSGVPS2VIeVhHZHFSVkFNLVFuLVhWbnNUaFZBZlUxRHdfYmxnIIEC; bili_jct=4c778cbf63c4af1772417171e64c9133; DedeUserID=416926781; DedeUserID__ckMd5=076139969a7a5b15; sid=ej0zprd7; fingerprint=81c65a80e4168f917cf348465bc99636; buvid_fp=783459E4-24FD-DB81-44CC-6C5C6DDBEAC361086infoc; buvid_fp_plain=undefined"
    'Cookie': "b_lsid=1B6106CAF_18C62AF8C07; _uuid=928A9D6A-6CD6-81110-85A9-FE48D52C13DC21039infoc; buvid_fp=98e79958c6450c50658886f55cbdac09; buvid3=AC3C7D91-FD24-9439-9F88-DD413D16DD9E20713infoc; b_nut=1702462721; buvid4=B7CD0DF6-F112-DD30-B4D2-BC10E134BEAF20713-023121310-; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDI3MjE5MjEsImlhdCI6MTcwMjQ2MjY2MSwicGx0IjotMX0.n4v_jdxmVsr7TuHrpqGpVQCryZYWpSArR4LgqxCex40; bili_ticket_expires=1702721861; SESSDATA=59841983%2C1718014733%2C5ee9a%2Ac2CjDYPMIcb2C2Q6X7sCnTp9uz2_2B63sEYuaFLBfA8k_b9uoRsyxUh-qOXLcaVoG5o7wSVk5WLUgwOGJfQ3RXUWROdm5zMnBLdFVTaEx0TmcwNVdSV3hwYmd3SGJBRldKT1ZwZU50dVZldnVTNldjWDh0bFByaFR4T2VHVUprM0dVZ0VhSHBOSktBIIEC; bili_jct=a3daa1accf55f832a2a0e08de05ec6b0; DedeUserID=3461576287849005; DedeUserID__ckMd5=1ef2f5c8b95afa36; sid=okiuesr5"
}