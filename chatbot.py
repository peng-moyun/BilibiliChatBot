import requests
import logging
import time
from deepdiff import DeepDiff

# B站会话接口
SESSION_API = "https://api.vc.bilibili.com/session_svr/v1/session_svr/get_sessions?session_type=1&group_fold=1&unfollow_fold=1&sort_rule=2&build=0&mobi_app=web"
# B站发送消息接口
SEND_MESSAGE_API = "https://api.vc.bilibili.com/web_im/v1/web_im/send_msg"

# 替换为你的Cookies字符串，推荐从环境变量或安全配置中读取
COOKIES = "i-wanna-go-back=-1; b_ut=7; header_theme_version=CLOSE; CURRENT_FNVAL=4048; PVID=1; buvid_fp_plain=undefined; buvid3=0F584BD5-3446-06DC-4E58-488185FA23D601373infoc; b_nut=1703577601; _uuid=6232C7D7-DCEB-C8C10-F4B4-23BBF263354A01695infoc; buvid4=304CD76F-0F21-4156-3FA3-43A0FD67373902292-023122608-5V%2BS1%2B6ZgMsXijxDBM5%2BBg%3D%3D; rpdid=|(uYmmkuuRml0J'u~|Jl~~Y|k; enable_web_push=DISABLE; LIVE_BUVID=AUTO9417091739995791; hit-dyn-v2=1; DedeUserID=525446160; DedeUserID__ckMd5=43b2f4e8e9abbcfd; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_BLACKGAP=0; bp_video_offset_525446160=923859611551793160; SESSDATA=86cdce96%2C1731481810%2Cc9ce7%2A52CjDi53A-Dj_YJL1GoB6_ow6YlpoRT2EJsoHnB8lj7_ySTOfbb2al7iEzFFS3inysK3wSVnY1eTR0NVl4OEdNTXRGNGlaV3FHc20wSmNSLVVyck9UOFVtRnhRVXJqT2dZSUdtZElkVWxfYXYzeWVnSlh2SjRDaTRfcmlhUDNBVDRRY2w4RmJteXN3IIEC; bili_jct=32474b142f3d5022127ce88dbaedf23f; sid=5qkpwqm6; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTY0NTY3NDgsImlhdCI6MTcxNjE5NzQ4OCwicGx0IjotMX0.Lh0EHstLRhuiXzpvNCQtF9oK93ESQXDnCZHFwIeBNYk; bili_ticket_expires=1716456688; fingerprint=367bded1043e9edd3ed6128297e8a666; bsource=search_bing; buvid_fp=367bded1043e9edd3ed6128297e8a666; bp_t_offset_525446160=934330810556743702; home_feed_column=4; browser_resolution=1227-692; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; b_lsid=108D934610_18FA3F18B47"
# 将Cookies转换为字典
cookies = {item.split("=")[0]: item.split("=")[1] for item in COOKIES.split("; ")}

# 添加必要的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://message.bilibili.com/',
    'Origin': 'https://www.bilibili.com'
}

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 用于保存上一次的会话信息
previous_sessions = None


def get_sessions():
    try:
        response = requests.get(SESSION_API, headers=headers, cookies=cookies)
        response.raise_for_status()  # 如果发生HTTP错误，则抛出异常
        data = response.json()
        logger.info("Response Data: %s", data)
        if data['code'] == 0:
            session_list = data['data'].get('session_list', [])
            if not session_list:
                logger.info("No unread private messages.")
            return session_list
        else:
            logger.error("Error in API response: %s", data['message'])
    except requests.exceptions.RequestException as e:
        logger.error("Failed to connect to the API: %s", e)
    return []


def send_message(talker_id, content="你好"):
    payload = {
        "msg[sender_uid]": "525446160?",  # 替换为你的用户ID
        "msg[receiver_id]": talker_id,
        "msg[receiver_type]": 1,
        "msg[msg_type]": 1,
        "msg[msg_status]": 0,
        "msg[content]": f'{{"content":"{content}"}}',
        "msg[timestamp]": int(time.time()),
        "csrf_token": cookies['bili_jct']
    }
    try:
        response = requests.post(SEND_MESSAGE_API, headers=headers, cookies=cookies, data=payload)
        response.raise_for_status()  # 如果发生HTTP错误，则抛出异常
        data = response.json()
        if data['code'] == 0:
            logger.info("Message sent to %s: %s", talker_id, content)
        else:
            logger.error("Error in sending message: %s", data['message'])
    except requests.exceptions.RequestException as e:
        logger.error("Failed to send message: %s", e)


def compare_sessions(previous, current):
    prev_dict = {session['talker_id']: session for session in previous}
    curr_dict = {session['talker_id']: session for session in current}

    all_talker_ids = set(prev_dict.keys()).union(curr_dict.keys())

    for talker_id in all_talker_ids:
        prev_session = prev_dict.get(talker_id, {})
        curr_session = curr_dict.get(talker_id, {})

        diff = DeepDiff(prev_session, curr_session, ignore_order=True)
        if diff:
            logger.info("Differences found for talker_id %s: %s", talker_id, diff)
            send_message(talker_id)


def main():
    global previous_sessions
    while True:
        current_sessions = get_sessions()
        if previous_sessions is not None:
            compare_sessions(previous_sessions, current_sessions)
        previous_sessions = current_sessions
        time.sleep(3)  # 每60秒执行一次


if __name__ == "__main__":
    main()
