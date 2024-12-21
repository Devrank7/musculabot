import uuid

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

from api.bot.access import JoinUser
from api.payments.liqpay_api import generate_url, get_order_status_from_liqpay
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == "Пополнить через Liqpay")
async def pay_router(message: Message) -> None:
    order_id = f"o_{uuid.uuid4().hex}"
    print(order_id)
    url = generate_url(order_id, 10)
    buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 💳", url=url)],
        [InlineKeyboardButton(text="Проверить оплату ⚡", callback_data=order_id)]
    ])
    await message.answer("Теперь нужно оплатить подписку", reply_markup=ReplyKeyboardRemove())
    await message.answer("Проверьте оплату: ", reply_markup=buttons)


@router.callback_query(F.data.startswith("o_"))
async def order_callback(query: CallbackQuery):
    print(query.data)
    status = get_order_status_from_liqpay(query.data)
    if status:
        await query.answer("Вы успешно оплатили заказ!🥳", show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        await query.answer("Вы еще не оплатили заказ!☹️", show_alert=True)
