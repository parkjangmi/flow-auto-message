import requests
import json
import os
from datetime import datetime

EMAIL = os.environ["FLOW_EMAIL"]
PASSWORD = os.environ["FLOW_PASSWORD"]
MESSAGE = os.environ["FLOW_MESSAGE"]
ROOM_SRNO = os.environ["FLOW_ROOM_SRNO"]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://flow.team/",
    "Origin": "https://flow.team",
})

print("로그인 중...")
login_payload = {
    "_JSON_": json.dumps({
        "USER_ID": EMAIL,
        "USER_PW": PASSWORD,
        "AUTO_LOGIN_YN": "N",
        "LOGIN_GB": "01"
    })
}
res = session.post("https://flow.team/member/MEMBER_LOGIN_P001.jct", data=login_payload)
result = res.json()
print(f"로그인 결과: {result.get('COMMON_HEAD', {}).get('MESSAGE', '')}")

if result.get('COMMON_HEAD', {}).get('ERROR'):
    raise Exception("로그인 실패!")

rgsn_dttm = result.get('RGSN_DTTM', '')
rgsr_nm = result.get('USER_NM', '')

print(f"메시지 전송 중: {MESSAGE}")
now = datetime.now()
hour = now.hour
minute = now.minute
ampm = "오전" if hour < 12 else "오후"
hour12 = hour if hour <= 12 else hour - 12
convt_dttm = f"{ampm} {hour12}:{minute:02d}"

msg_payload = {
    "_JSON_": json.dumps({
        "USER_ID": EMAIL,
        "RGSN_DTTM": rgsn_dttm,
        "ROOM_SRNO": ROOM_SRNO,
        "RGSR_ID": EMAIL,
        "RGSR_NM": rgsr_nm,
        "RGSR_JBCL_NM": "",
        "CNTN": MESSAGE,
        "BOMB_YN": "N",
        "REPLY_YN": "N",
        "BOMB_TIMER": "",
        "CHAT_SRCH_GB": "E",
        "MSG_GB": "",
        "ROOM_KIND": "",
        "CONVT_DTTM": convt_dttm,
        "ROOM_CHAT_SRNO": "NEW",
        "TEMP_CHAT_SRNO": "NEW",
        "NOT_READ_CNT": 1,
        "REPLY_CHAT_SRNO": "",
        "REPLY_MSG_GB": "",
        "REPLY_IMG_COUNT": "",
        "ROOM_GB": "1",
        "RGSN_DTTM_YYYYMMDDHHmm": now.strftime("%Y%m%d%H%M%S"),
        "FILE_CLOUD_REC": []
    }, ensure_ascii=False)
}
res = session.post("https://flow.team/colabo2/COLABO2_CHAT_MSG_C001.jct", data=msg_payload)
result = res.json()
print(f"전송 결과: {result}")

if not result.get('COMMON_HEAD', {}).get('ERROR'):
    print("메시지 전송 성공!")
else:
    raise Exception(f"전송 실패: {result}")
