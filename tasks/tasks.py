import logging
from abc import abstractmethod, ABC
from datetime import datetime

from aiogram import Bot

from api.bot.access import KickUser, JoinUser
from api.payments.wayforpay_api import check_ok_regular_invoice, remove_regular_invoice
from buttons.inline import get_dismiss, get_subscribe
from db.sql.model import User
from db.sql.service import run_sql, AllUsers, UpdateUserDateBeforeWeekOnNone, \
    UpdateUserDateThreeOnNone, UpdateUserDateOneOnNone, DetachWfpDataFromUser
from lang.language import translate
from utility.utils import check_access_for_chanel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
                await self.bot.send_message(user.tg_id, translate("1", user.lang))
            else:
                await remove_regular_invoice(order)
                await run_sql(DetachWfpDataFromUser(user.tg_id))
                await KickUser(self.bot, user.tg_id).task()
                logger.warning("Пользователь с WFP был кикнут")
                await self.bot.send_message(user.tg_id,
                                            translate("2", user.lang),
                                            reply_markup=get_subscribe(user))
        else:
            await KickUser(self.bot, user.tg_id).task()
            logger.info("Пользователь был кикнут")

    async def distributed(self, user: User):
        try:
            if user.date_week_before_kill and datetime.now() > user.date_week_before_kill:
                await self.bot.send_message(user.tg_id, translate("3", user.lang),
                                            reply_markup=get_dismiss(user))
                await run_sql(UpdateUserDateBeforeWeekOnNone(user.tg_id))
                return
            if user.date_three_before_kill and datetime.now() > user.date_three_before_kill:
                await self.bot.send_message(user.tg_id, translate("4", user.lang),
                                            reply_markup=get_dismiss(user))
                await run_sql(UpdateUserDateThreeOnNone(user.tg_id))
                return
            if user.date_one_before_kill and datetime.now() > user.date_one_before_kill:
                await self.bot.send_message(user.tg_id, translate("1", user.lang),
                                            reply_markup=get_dismiss(user))
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
