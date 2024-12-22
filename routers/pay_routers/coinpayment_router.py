from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from api.bot.access import JoinUser
from api.payments.coinpayments import create_transaction, check_payment_status
from buttons.inline import get_cp_button
from db.sql.model import User
from filter.reply import ReplyFilter
from lang.language import translate
from middlewares.middleware import AuthMiddleware, AuthMiddlewareCallback

router = Router()
router.message.middleware(AuthMiddleware())
router.message.middleware(AuthMiddlewareCallback())


@router.message(ReplyFilter('3'))
async def pay_router(message: Message, user: User) -> None:
    tx_id, url = create_transaction(4, "Лучший канал Muscle Lab", "week2735@gmail.com")
    cp_button = get_cp_button(user, url, tx_id)
    await message.answer(translate("19", user.lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(translate("24", user.lang),
                         reply_markup=cp_button)


@router.callback_query(F.data.startswith('cp_'))
async def coinpayment_callback(query: CallbackQuery, user: User):
    tx_id = query.data.split('_')[1]
    status, ok = check_payment_status(tx_id)
    if ok:
        await query.answer(translate("25", user.lang), show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        await query.answer(translate("26", user.lang),
                           show_alert=True)
