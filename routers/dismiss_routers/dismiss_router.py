from aiogram import Router, F
from aiogram.types import CallbackQuery

from api.bot.access import KickUser
from api.payments.wayforpay_api import remove_regular_invoice
from db.sql.model import User
from db.sql.service import DetachWfpDataFromUser, run_sql
from middlewares.middleware import AuthMiddlewareCallback

router = Router()
router.callback_query.middleware(AuthMiddlewareCallback())


@router.callback_query(F.data == 'dismiss')
async def dismiss_callback(query: CallbackQuery, user: User):
    if user.wfp_data:
        order = user.wfp_data.order
        await remove_regular_invoice(order)
        await run_sql(DetachWfpDataFromUser(user.tg_id))
        await query.message.answer("Авто списывание через wayforpay было удаленно😌")
    await query.answer("Мы будем скучать!")
    await KickUser(query.bot, user.tg_id, left=True).task()
