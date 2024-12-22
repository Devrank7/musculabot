from aiogram.filters import Filter
from aiogram.types import Message

from lang.language import dic_reply


class ReplyFilter(Filter):
    def __init__(self, index: str):
        self.index = index

    async def __call__(self, message: Message) -> bool:
        print("FILTER")
        lan = dic_reply.get(self.index)
        for k, v in lan.items():
            if message.text == v:
                return True
        return False
