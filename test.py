from bilibili_api import Credential, sync
from bilibili_api.session import Session, Event, EventType
from bilibili_api.utils.picture import Picture
from bilibili_api import settings
import os

# Set the proxy URL with scheme
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
settings.timeout = 99.0

# 使用 aiohttp.ClientSession()
settings.http_client = settings.HTTPClient.AIOHTTP  # default
# 使用 httpx.AsyncClient()
settings.http_client = settings.HTTPClient.HTTPX

settings.request_log = True

from bilibili_api import Credential

credential = Credential(
    sessdata="86cdce96,1731481810,"
             "c9ce7*52CjDi53A-Dj_YJL1GoB6_ow6YlpoRT2EJsoHnB8lj7_ySTOfbb2al7iEzFFS3inysK3wSVnY1eTR0NVl4OEdNTXRGNGlaV3FHc20wSmNSLVVyck9UOFVtRnhRVXJqT2dZSUdtZElkVWxfYXYzeWVnSlh2SjRDaTRfcmlhUDNBVDRRY2w4RmJteXN3IIEC",
    bili_jct="32474b142f3d5022127ce88dbaedf23f",
    buvid3="0F584BD5-3446-06DC-4E58-488185FA23D601373infoc",
    dedeuserid="525446160"
)
session = Session(credential)


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
        await session.reply(event, "你好李鑫")


sync(session.start())
