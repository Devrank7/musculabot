import logging
import os
from abc import abstractmethod, ABC
from datetime import timedelta, datetime

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

from db.sql.service import run_sql, UpdateUserDate, UpdateUserDateOnNone

load_dotenv()
CHAT_ID = int(os.getenv("CHAT_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
buttons_subscribe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Купить подписку на месяц🦾", callback_data="unity")],
])
DEBUG = True


class BotTask(ABC):
    @abstractmethod
    async def task(self):
        raise NotImplementedError


class KickUser(BotTask):
    CRY_MESSAGE = '''
    Жаль, что ты нас покидаешь😢
    Но мы всегда будем ждать тебя снова, успехов в тренировках🫡
    '''

    def __init__(self, bot: Bot, tg_id: int, left: bool = False):
        self.bot = bot
        self.tg_id = tg_id
        self.left = left

    async def task(self):
        try:
            member = await self.bot.get_chat_member(chat_id=CHAT_ID, user_id=self.tg_id)
            if member and member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED]:
                await self.bot.ban_chat_member(chat_id=CHAT_ID, user_id=self.tg_id)
                await self.bot.send_message(self.tg_id, self.CRY_MESSAGE, reply_markup=buttons_subscribe)
                await run_sql(UpdateUserDateOnNone(self.tg_id))
            else:
                logger.info("User not found")
                if self.left:
                    await self.bot.send_message(self.tg_id, self.CRY_MESSAGE, reply_markup=buttons_subscribe)
                    await run_sql(UpdateUserDateOnNone(self.tg_id))
        except Exception as e:
            logger.error(f"Ошибка в методе task класс KickUser {e}")


class JoinUser(BotTask):
    def __init__(self, bot: Bot, tg_id: int):
        self.bot = bot
        self.tg_id = tg_id

    JOIN_TEXT = '''
    🔥Поздравляю, ты оформил подписку в Muscle Lab!
     Добро пожаловать в лучшее комьюнити натурального бодибилдинга🦍
    '''
    BOOST_TEXT = '''
    🔥Поздравляю, ты продлил подписку теперь тебе начислено еще месяц нахождения
     в лучшем канале для бодибилдинга💪 
    '''

    async def task(self):
        try:
            member = await self.bot.get_chat_member(chat_id=CHAT_ID, user_id=self.tg_id)
            if (member is None) or (member.status in [ChatMemberStatus.KICKED, ChatMemberStatus.LEFT]):
                await self.bot.unban_chat_member(chat_id=CHAT_ID, user_id=self.tg_id)
                invite_link = await self.bot.create_chat_invite_link(chat_id=CHAT_ID, creates_join_request=True,
                                                                     expire_date=datetime.now() + timedelta(hours=1))
                await self.bot.send_message(self.tg_id,
                                            f"{self.JOIN_TEXT} . Вот ваша ссылка на вступление👋"
                                            f" {invite_link.invite_link} ."
                                            f" Обратите внимание, что ссылка будет действительна"
                                            f" в течении часа, после чего она станет недоступной, и вы"
                                            f" не сможете вступить в канала. Не тяните время!👌")
                await run_sql(UpdateUserDate(self.tg_id, date_time=datetime.now() + (
                    timedelta(minutes=5) if DEBUG else timedelta(days=30)), debug=DEBUG))
            else:
                if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.RESTRICTED]:
                    await run_sql(UpdateUserDate(self.tg_id, date_time=datetime.now() + (
                        timedelta(minutes=5) if DEBUG else timedelta(days=30)), debug=DEBUG))
                    await self.bot.send_message(self.tg_id, self.BOOST_TEXT)
                elif member.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
                    await self.bot.send_message(self.tg_id, "Вы админ этой группы!💪")
        except Exception as e:
            logger.error(f"err tasks.py class JoinUser: {e}")
