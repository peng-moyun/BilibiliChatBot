import configparser

import openai
import requests
from bilibili_api import Credential, sync
from bilibili_api.session import Session, Event, EventType
from bilibili_api.user import User
from bilibili_api.utils.picture import Picture
from bilibili_api import settings
from bilibili_api import user
import os
import re

config = configparser.ConfigParser()
config_path = 'config.txt'
config.read(config_path, encoding='utf-8')
g_set = config.get('DEFAULT', 'set')
# 打印set的类型
print(g_set)
# Set the proxy URL with scheme
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
settings.timeout = 99.0

proxies = {
    'http': 'http://127.0.0.1:your_proxy_port',
    'https': 'http://127.0.0.1:your_proxy_port'
}

# 创建一个请求会话并设置代理
session = requests.Session()
session.proxies.update(proxies)

# 使用 aiohttp.ClientSession()
settings.http_client = settings.HTTPClient.AIOHTTP  # default
# 使用 httpx.AsyncClient()
settings.http_client = settings.HTTPClient.HTTPX

settings.request_log = True


# B站认证


def extract_credential(cookie_str):
    def get_value(key):
        match = re.search(rf"{key}=([^;]+)", cookie_str)
        return match.group(1) if match else None

    sessdata = get_value("SESSDATA")
    bili_jct = get_value("bili_jct")
    buvid3 = get_value("buvid3")
    dedeuserid = get_value("DedeUserID")

    return Credential(sessdata, bili_jct, buvid3, dedeuserid)

# 输入的cookie字符串
cookie_str = ("i-wanna-go-back=-1; b_ut=7; header_theme_version=CLOSE; CURRENT_FNVAL=4048; PVID=1; buvid_fp_plain=undefined; buvid3=0F584BD5-3446-06DC-4E58-488185FA23D601373infoc; b_nut=1703577601; _uuid=6232C7D7-DCEB-C8C10-F4B4-23BBF263354A01695infoc; buvid4=304CD76F-0F21-4156-3FA3-43A0FD67373902292-023122608-5V%2BS1%2B6ZgMsXijxDBM5%2BBg%3D%3D; rpdid=|(uYmmkuuRml0J'u~|Jl~~Y|k; enable_web_push=DISABLE; LIVE_BUVID=AUTO9417091739995791; hit-dyn-v2=1; DedeUserID=525446160; DedeUserID__ckMd5=43b2f4e8e9abbcfd; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_BLACKGAP=0; bp_video_offset_525446160=923859611551793160; SESSDATA=86cdce96%2C1731481810%2Cc9ce7%2A52CjDi53A-Dj_YJL1GoB6_ow6YlpoRT2EJsoHnB8lj7_ySTOfbb2al7iEzFFS3inysK3wSVnY1eTR0NVl4OEdNTXRGNGlaV3FHc20wSmNSLVVyck9UOFVtRnhRVXJqT2dZSUdtZElkVWxfYXYzeWVnSlh2SjRDaTRfcmlhUDNBVDRRY2w4RmJteXN3IIEC; bili_jct=32474b142f3d5022127ce88dbaedf23f; sid=5qkpwqm6; fingerprint=367bded1043e9edd3ed6128297e8a666; bsource=search_bing; buvid_fp=367bded1043e9edd3ed6128297e8a666; home_feed_column=4; bp_t_offset_525446160=934624401658216464; b_lsid=D211010A10E_18FA53FBA94; browser_resolution=484-2672")

# 提取Credential对象
credential = extract_credential(cookie_str)
print(credential)

session = Session(credential)

# 设置OpenAI API密钥
openai.api_key = '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'


def get_gpt_reply(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": g_set},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"An error occurred: {e}"


# answer = get_gpt_reply("测试")
# print(answer)
@session.on(EventType.PICTURE)
async def pic(event: Event):
    img: Picture = event.content
    img.download("./")


@session.on(EventType.TEXT)
async def reply(event: Event):
    if event.content == "/close":
        session.close()
    elif event.content == "来张涩图":
        img = await Picture.from_file("test.png").upload_file(session.credential)
        await session.reply(event, img)
    else:
        try:
            print(event.sender_uid)
            uid_num = int(event.sender_uid)
            s_user = user.User(uid=uid_num, credential=credential)
            # answer = get_gpt_reply(str(event.content))
            fenshi = await s_user.get_user_medal()
            print(fenshi)
            answer = "测试"
            print(answer)
            await session.reply(event, answer)
        except Exception as e:
            print(f"Error in getting GPT reply: {e}")
            await session.reply(event, "获取回复时出错，请稍后再试。")


sync(session.start())
