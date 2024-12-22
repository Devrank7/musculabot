from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery

from api.payments.wayforpay_api import remove_regular_invoice
from buttons.reply import pay_buttons
from db.sql.model import User
from db.sql.service import run_sql, DetachWfpDataFromUser
from filter.reply import ReplyFilter
from lang.language import translate
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.callback_query(F.data == 'Удалить текущий регулярный платеж')
async def remove_order(query: CallbackQuery, user: User):
    await query.answer()
    if user.wfp_data:
        order = user.wfp_data.order
        await remove_regular_invoice(order)
        await run_sql(DetachWfpDataFromUser(user.tg_id))
        await query.message.answer(translate("6", user.lang),
                                   reply_markup=ReplyKeyboardRemove())
    else:
        await query.message.answer(translate("7", user.lang), reply_markup=ReplyKeyboardRemove())


@router.message(ReplyFilter('5'))
async def remove_order(message: Message, user: User):
    if user.wfp_data:
        order = user.wfp_data.order
        await remove_regular_invoice(order)
        await run_sql(DetachWfpDataFromUser(user.tg_id))
        await message.answer(translate("40", user.lang), reply_markup=ReplyKeyboardRemove())
        await message.answer(translate("8", user.lang), reply_markup=pay_buttons(user))
    else:
        await message.answer(translate("7", user.lang), reply_markup=ReplyKeyboardRemove())
