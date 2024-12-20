from aiogram import Router, F
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from routers.pay_routers import ton_router, way_for_pay_router, coinpayment_router

router = Router()
router.include_router(ton_router.router)
router.include_router(way_for_pay_router.router)
router.include_router(coinpayment_router.router)
pay_button = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Пополнить через TON")],
    [KeyboardButton(text="Пополнить через WayForPay")],
    [KeyboardButton(text="Пополнить через Coinpayment")],
], resize_keyboard=True, one_time_keyboard=True)


@router.callback_query(F.data == "unity")
async def callback_query_unity(query: CallbackQuery):
    await query.answer(text="Теперь осталось выбрать способ оплати")
    await query.message.answer("Выберите способ оплаты", reply_markup=pay_button)
