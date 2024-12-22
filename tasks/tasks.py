import logging
from abc import abstractmethod, ABC
from datetime import datetime

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from api.bot.access import KickUser, JoinUser
from api.payments.wayforpay_api import check_ok_regular_invoice, remove_regular_invoice
from db.sql.model import User
from db.sql.service import run_sql, AllUsers, UpdateUserDateBeforeWeekOnNone, \
    UpdateUserDateThreeOnNone, UpdateUserDateOneOnNone, DetachWfpDataFromUser
from utility.utils import check_access_for_chanel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dismiss_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить подписку сейчас🙄", callback_data="dismiss")],
    [InlineKeyboardButton(text="Купить подписку на месяц сейчас🦾", callback_data="unity")]
])
buttons_subscribe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить доступ в комьюнити🦾", callback_data="unity")],
])


class Task(ABC):
    @abstractmethod
    async def task(self):
        raise NotImplementedError


class DistributedTask(Task):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def change_access_for_chanel(self, user: User):
        logger.info(f"WFP is {user.wfp_data}")
        if user.wfp_data:
            order = user.wfp_data.order
            logger.warning(f"ORDER: {order}")
            status = await check_ok_regular_invoice(order)
            print(f"STATUS: {status}")
            if status:
                await JoinUser(self.bot, user.tg_id).task()
                await self.bot.send_message(user.tg_id, 'Успешно продлено с автоматическим списанием!')
            else:
                await remove_regular_invoice(order)
                await run_sql(DetachWfpDataFromUser(user.tg_id))
                await KickUser(self.bot, user.tg_id).task()
                logger.warning("Пользователь с WFP был кикнут")
                await self.bot.send_message(user.tg_id,
                                            "Не удалось продлить подписку🙁."
                                            " Регулярная подписка окончена, или отключена."
                                            "Для покупки месячной подписки выберите оплату🤞",
                                            reply_markup=buttons_subscribe)
        else:
            await KickUser(self.bot, user.tg_id).task()
            logger.info("Пользователь был кикнут")

    async def distributed(self, user: User):
        try:
            if user.date_week_before_kill and datetime.now() > user.date_week_before_kill:
                await self.bot.send_message(user.tg_id, "💥Подписка заканчивается через 7 дней!",
                                            reply_markup=dismiss_button)
                await run_sql(UpdateUserDateBeforeWeekOnNone(user.tg_id))
                return
            if user.date_three_before_kill and datetime.now() > user.date_three_before_kill:
                await self.bot.send_message(user.tg_id, "💥Подписка заканчивается через 3 дней",
                                            reply_markup=dismiss_button)
                await run_sql(UpdateUserDateThreeOnNone(user.tg_id))
                return
            if user.date_one_before_kill and datetime.now() > user.date_one_before_kill:
                await self.bot.send_message(user.tg_id, "💥Подписка заканчивается через 1 дней",
                                            reply_markup=dismiss_button)
                await run_sql(UpdateUserDateOneOnNone(user.tg_id))
                return
            logger.info("Пользователь был уведомлен!")
        except Exception as e:
            logger.error(f"method distribute tasks.py: {e}")

    async def task(self):
        try:
            users = await run_sql(AllUsers())
            for user in users:
                await self.distributed(user) if check_access_for_chanel(
                    user) else await self.change_access_for_chanel(
                    user)
        except Exception as e:
            logger.error(f"task in tasks.py: {e}")
