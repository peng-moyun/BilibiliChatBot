import asyncio
from bilibili_api import Credential, session
from bilibili_api.session import EventType

class Message:
    def __init__(self, credential: Credential):
        self.my_credential = credential

    async def method_send_msg(self, uid: int, msg: str, msg_type: EventType = EventType.TEXT):
        try:
            await session.send_msg(
                credential=self.my_credential,
                receiver_id=uid,
                msg_type=msg_type,
                content=msg,
            )
            print(f'发送成功~{msg}')
        except Exception as e:
            print(f'send error: {e}')

async def func_main():
    credential = Credential(
        sessdata="86cdce96,1731481810,c9ce7*52CjDi53A-Dj_YJL1GoB6_ow6YlpoRT2EJsoHnB8lj7_ySTOfbb2al7iEzFFS3inysK3wSVnY1eTR0NVl4OEdNTXRGNGlaV3FHc20wSmNSLVVyck9UOFVtRnhRVXJqT2dZSUdtZElkVWxfYXYzeWVnSlh2SjRDaTRfcmlhUDNBVDRRY2w4RmJteXN3IIEC",
        bili_jct="32474b142f3d5022127ce88dbaedf23f",
        buvid3="0F584BD5-3446-06DC-4E58-488185FA23D601373infoc",
        dedeuserid="525446160"
    )

    lv_send_msg = Message(credential=credential)
    await lv_send_msg.method_send_msg(
        uid=482217361,
        msg='hello',
        msg_type=EventType.TEXT,
    )

if __name__ == "__main__":
    asyncio.run(func_main())
