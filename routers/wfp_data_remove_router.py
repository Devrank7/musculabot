from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery

from api.payments.wayforpay_api import remove_regular_invoice
from db.sql.model import User
from db.sql.service import run_sql, DetachWfpDataFromUser
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())
pay_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Пополнить через TON 💳")],
    [KeyboardButton(text="Пополнить через WayForPay 💎")],
    [KeyboardButton(text="Пополнить через Coinpayment 💵")],
    # [KeyboardButton(text="Пополнить через Liqpay")],
], resize_keyboard=True, one_time_keyboard=True)


@router.callback_query(F.data == 'Удалить текущий регулярный платеж')
async def remove_order(query: CallbackQuery, user: User):
    await query.answer()
    if user.wfp_data:
        order = user.wfp_data.order
        await remove_regular_invoice(order)
        await run_sql(DetachWfpDataFromUser(user.tg_id))
        await query.message.answer("💯 Мы удалили ваш регулярные платеж."
                                   "👊Подписка у вас, так и осталась, но теперь регулярно обновляться она не будет."
                                   "🤝После того как подписка закончится ми уведомим вас и вы новый способ оплати",
                                   reply_markup=ReplyKeyboardRemove())
    else:
        await query.message.answer("У вас нет регулярного платежа!", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == 'Удалить текущий регулярный платеж и продлить подписку')
async def remove_order(message: Message, user: User):
    if user.wfp_data:
        order = user.wfp_data.order
        await remove_regular_invoice(order)
        await run_sql(DetachWfpDataFromUser(user.tg_id))
        await message.answer("💯 Мы удалили ваш регулярные платеж.", reply_markup=ReplyKeyboardRemove())
        await message.answer("👊Подписка у вас, так и осталась, но теперь регулярно обновляться она не будет"
                             "👋Теперь, вы можете выбрать новую систему, для продления подписки,"
                             " или опять использовать wayforpay для авто снимания денег!", reply_markup=pay_button)
    else:
        await message.answer("У вас нет регулярного платежа!", reply_markup=ReplyKeyboardRemove())
