from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from db.sql.model import User
from middlewares.middleware import AuthMiddlewareCallback
from routers.pay_routers import ton_router, way_for_pay_router, coinpayment_router, liqpay_router

router = Router()
router.callback_query.middleware(AuthMiddlewareCallback())
router.include_router(ton_router.router)
router.include_router(way_for_pay_router.router)
router.include_router(coinpayment_router.router)
router.include_router(liqpay_router.router)
pay_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Пополнить через TON 💳")],
    [KeyboardButton(text="Пополнить через WayForPay 💎")],
    [KeyboardButton(text="Пополнить через Coinpayment 💵")],
    [KeyboardButton(text="Пополнить через Liqpay")],
], resize_keyboard=True, one_time_keyboard=True)
remove_wfp_data = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Удалить текущий регулярный платеж и продлить подписку")]
])


@router.callback_query(F.data == "unity")
async def callback_query_unity(query: CallbackQuery, user: User):
    if user.wfp_data:
        await query.answer()
        await query.message.answer("🤙На данный момент ви имеете подписку через wayforpay,"
                                   "где используются регулярные платежи каждый месяц!"
                                   "Если вы хотите оплатить новую регулярную подписку,"
                                   "или оплатить месяц подписки другим способом,"
                                   "то удалите текущий регулярный платеж👌", reply_markup=remove_wfp_data)
        return
    await query.answer(text="Теперь осталось выбрать способ оплати")
    await query.message.answer("Выберите способ оплаты♠️", reply_markup=pay_button)
