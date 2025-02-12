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
import DFAFilter

config = configparser.ConfigParser()
config_path = 'config.txt'
config.read(config_path, encoding='utf-8')
g_set = config.get('DEFAULT', 'set')
openaikey = config.get('DEFAULT', 'openai.api_key0')
target_id = config.get('DEFAULT', 'target_id')
help_message = config.get('DEFAULT', 'help_message')
# 打印set的类型
print(g_set)
print(openaikey)
print(target_id)
print(help_message)


# Set the proxy URL with scheme
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
settings.timeout = 99.0

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 创建一个请求会话并设置代理
session = requests.Session()
session.proxies.update(proxies)

# 使用 aiohttp.ClientSession()
settings.http_client = settings.HTTPClient.AIOHTTP  # default
# 使用 httpx.AsyncClient()
settings.http_client = settings.HTTPClient.HTTPX

settings.request_log = True

import sqlite3
from datetime import datetime
import user_data_manager

user_data_manager.init_db()


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
cookie_str = (
    "i-wanna-go-back=-1; b_ut=7; header_theme_version=CLOSE; CURRENT_FNVAL=4048; PVID=1; buvid_fp_plain=undefined; buvid3=0F584BD5-3446-06DC-4E58-488185FA23D601373infoc; b_nut=1703577601; _uuid=6232C7D7-DCEB-C8C10-F4B4-23BBF263354A01695infoc; buvid4=304CD76F-0F21-4156-3FA3-43A0FD67373902292-023122608-5V%2BS1%2B6ZgMsXijxDBM5%2BBg%3D%3D; rpdid=|(uYmmkuuRml0J'u~|Jl~~Y|k; enable_web_push=DISABLE; LIVE_BUVID=AUTO9417091739995791; hit-dyn-v2=1; DedeUserID=525446160; DedeUserID__ckMd5=43b2f4e8e9abbcfd; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; CURRENT_BLACKGAP=0; fingerprint=367bded1043e9edd3ed6128297e8a666; bp_t_offset_525446160=934709527908974601; buvid_fp=4d3fa4bee33ee583bc0f29df7d81c6b1; b_lsid=1C3101251_18FB7C65149; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTcwMzQzNzksImlhdCI6MTcxNjc3NTExOSwicGx0IjotMX0.qjvSNG0pIGraXKqo-FVoc-sn9DdFiP8orIQL_tjBsCw; bili_ticket_expires=1717034319; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; SESSDATA=dd33daa7%2C1732332414%2C25bf0%2A52CjAad3ZE_GAa35ZIiFR1xUDvB84Zo4npm_tzchKnR9BdFlKvQC1cOgIfznqwwTtL9pESVnpZVEp6U3hjR2J5YXN6cnZqeHBkSF8tSHc1ZHpuR0VXb2RpMi1Pa3BUX1BLZmlha0RNaFBEY01OVmVRWTRfd0VCNFNWeXI3SGFCYm5iUU42RWNXQkF3IIEC; bili_jct=f5ff777cebe4812de1466166434e2357; sid=6qgfrr1x; home_feed_column=4; browser_resolution=1068-1466")

# 提取Credential对象
credential = extract_credential(cookie_str)
print(credential)

session = Session(credential)

# 设置OpenAI API密钥
# openai.api_key = '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'
openai.api_key = openaikey


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
        print(f"An error occurred: {e}")
        return f"获取回复时出错，请稍后再试。"


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
    elif event.content == "#help":
        await session.reply(event, help_message)
    elif event.content.startswith("#"):
        try:
            uid_num = int(event.sender_uid)
            conn = sqlite3.connect('user_data.db')
            cursor = conn.cursor()

            # 获取用户数据
            cursor.execute('SELECT message_count, last_updated FROM user_messages WHERE uid = ?', (uid_num,))
            row = cursor.fetchone()

            today_date = datetime.now().date()
            if row:
                message_count, last_updated = row
                last_updated_date = datetime.strptime(last_updated, "%Y-%m-%d").date()

                # 如果日期已更改，则重置计数
                if last_updated_date < today_date:
                    message_count = 0
            else:
                message_count = 0
                cursor.execute('INSERT INTO user_messages (uid, message_count, last_updated) VALUES (?, ?, ?)',
                               (uid_num, message_count, today_date))

            if message_count >= 50:
                await session.reply(event, "米卡今天很累了，明天再来聊天吧！")
            elif event.content == "#查询额度":
                remaining_quota = 50 - message_count
                await session.reply(event, f"剩余 {remaining_quota} 条信息额度。")
            elif event.content == "#查询性格":
                await session.reply(event, g_set)
            else:
                content = event.content[1:].strip()
                # 处理你的逻辑
                message_count += 1
                remaining_quota = 50 - message_count
                cursor.execute('UPDATE user_messages SET message_count = ?, last_updated = ? WHERE uid = ?',
                               (message_count, today_date, uid_num))
                conn.commit()

                # 粉丝检查逻辑
                s_user = user.User(uid=uid_num, credential=credential)
                data = await s_user.get_user_medal()
                is_fan = False
                medal_level = None
                for item in data["list"]:
                    if item["medal_info"]["target_id"] == int(target_id):
                        is_fan = True
                        medal_level = item["medal_info"]["level"]
                        break
                if is_fan:
                    answer = get_gpt_reply(str(content))
                    answer = "「AI回复」"+answer
                    print(answer)
                    # dfa = DFAFilter.DFAFilter()
                    # if dfa.filterSensitiveWords(answer):
                    #     answer = "这个话题太敏感请换个话题"
                    print(f"剩余 {remaining_quota} 条信息额度，粉丝牌等级：{medal_level}。")
                else:
                    answer = f"你还不是粉丝或你没公开粉丝牌哦"

                await session.reply(event, answer)
        except Exception as e:
            print(f"Error in getting GPT reply: {e}")
            await session.reply(event, "获取回复时出错，请稍后再试。")
        finally:
            conn.close()


sync(session.start())
