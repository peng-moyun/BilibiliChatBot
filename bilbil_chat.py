import openai
import requests
from bilibili_api import Credential, sync
from bilibili_api.session import Session, Event, EventType
from bilibili_api.utils.picture import Picture
from bilibili_api import settings
import os

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
credential = Credential(
    sessdata="86cdce96,1731481810,c9ce7*52CjDi53A-Dj_YJL1GoB6_ow6YlpoRT2EJsoHnB8lj7_ySTOfbb2al7iEzFFS3inysK3wSVnY1eTR0NVl4OEdNTXRGNGlaV3FHc20wSmNSLVVyck9UOFVtRnhRVXJqT2dZSUdtZElkVWxfYXYzeWVnSlh2SjRDaTRfcmlhUDNBVDRRY2w4RmJteXN3IIEC",
    bili_jct="32474b142f3d5022127ce88dbaedf23f",
    buvid3="0F584BD5-3446-06DC-4E58-488185FA23D601373infoc",
    dedeuserid="525446160"
)
session = Session(credential)

# 设置OpenAI API密钥
openai.api_key = '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'


def get_gpt_reply(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
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
            answer = get_gpt_reply(str(event.content))
            print(answer)
            await session.reply(event, answer)
        except Exception as e:
            print(f"Error in getting GPT reply: {e}")
            await session.reply(event, "获取回复时出错，请稍后再试。")


sync(session.start())
