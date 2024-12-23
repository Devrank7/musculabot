import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from api.bot.access import JoinUser
from api.currency.curency import get_require
from api.payments.wayforpay_api import create_regular_invoice, check_ok_regular_invoice
from buttons.inline import get_wtf_buttons
from db.sql.model import User
from db.sql.service import run_sql, AttachWfpDataToUser
from filter.reply import ReplyFilter
from lang.language import translate
from middlewares.middleware import AuthMiddleware, AuthMiddlewareCallback

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddlewareCallback())


@router.message(ReplyFilter('2'))
async def pay_router(message: Message, user: User) -> None:
    order_id = f"HD{user.tg_id}PD{random.randint(1, 1000)}"
    req = get_require()
    url = create_regular_invoice(order_id, req)
    wtf_buttons = get_wtf_buttons(user, url, order_id)
    await message.answer(translate("19", user.lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(translate("18", user.lang), reply_markup=wtf_buttons)


@router.callback_query(F.data.startswith("wfp_"))
async def order_callback(query: CallbackQuery, user: User):
    order_id = query.data.split("_")[1]
    status = await check_ok_regular_invoice(order_id)
    if status:
        await run_sql(AttachWfpDataToUser(query.from_user.id, order_id))
        await query.answer(translate("20", user.lang), show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        await query.answer(translate("21", user.lang),
                           show_alert=True)
