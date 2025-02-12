from bilibili_api import Credential, session


class Message:
    def __init__(self, credential: Credential):
        self.my_credential = credential

    def method_send_msg(self, uid, msg, msg_type):
        pass


async def method_send_msg(self, uid: int, msg: str, msg_type: session.EventType = session.EventType.TEXT):
    try:
        await session.send_msg(
            credential=self.my_credential,
            receiver_id=uid,
            msg_type=msg_type,
            content=msg,
        )
        print(f'发送成功~{msg}')
    except:
        print('send error')
