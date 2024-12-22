import random

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from api.bot.access import JoinUser
from api.payments.wayforpay_api import create_regular_invoice, check_ok_regular_invoice
from db.sql.model import User
from db.sql.service import run_sql, AttachWfpDataToUser
from middlewares.middleware import AuthMiddleware, AuthMiddlewareCallback

router = Router()
router.message.middleware(AuthMiddleware())
router.callback_query.middleware(AuthMiddlewareCallback())

text_wtf = '''
❗️Платеж был создан: После того как оплатите подписку. Нажмите на 'Проверить оплату'
и вам предоставится доступ к каналу
'''


@router.message(F.text == "Пополнить через WayForPay 💎")
async def pay_router(message: Message, user: User) -> None:
    order_id = f"HD{user.tg_id}PD{random.randint(1, 1000)}"
    url = create_regular_invoice(order_id)
    wtf_buttons = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 💳", url=url[0])],
        [InlineKeyboardButton(text="Проверить оплату ⚡", callback_data=f"wfp_{order_id}")]
    ])
    await message.answer("Теперь нужно оплатить подписку", reply_markup=ReplyKeyboardRemove())
    await message.answer(text_wtf, reply_markup=wtf_buttons)


@router.callback_query(F.data.startswith("wfp_"))
async def order_callback(query: CallbackQuery):
    order_id = query.data.split("_")[1]
    status = await check_ok_regular_invoice(order_id)
    if status:
        await run_sql(AttachWfpDataToUser(query.from_user.id, order_id))
        await query.answer("Вы успешно оплатили доступ🥳 Используя wayforpay, с регулярной подпиской!🙌", show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        await query.answer("Вы еще не оплатили регулярный платеж!", show_alert=True)
