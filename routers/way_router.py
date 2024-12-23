from aiogram import Router, F
from aiogram.types import CallbackQuery

from buttons.reply import pay_buttons, regular_but
from db.sql.model import User
from lang.language import translate
from middlewares.middleware import AuthMiddlewareCallback
from routers.pay_routers import ton_router, way_for_pay_router, coinpayment_router, liqpay_router

router = Router()
router.callback_query.middleware(AuthMiddlewareCallback())
router.include_router(ton_router.router)
router.include_router(way_for_pay_router.router)
router.include_router(coinpayment_router.router)
router.include_router(liqpay_router.router)


@router.callback_query(F.data == "unity")
async def callback_query_unity(query: CallbackQuery, user: User):
    if user.wfp_data:
        await query.answer()
        await query.message.answer(translate("9", user.lang), reply_markup=regular_but(user))
        return
    await query.answer(text=translate("10", user.lang))
    await query.message.answer(translate("11", user.lang), reply_markup=pay_buttons(user))
