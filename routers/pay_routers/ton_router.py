import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from dotenv import load_dotenv

from api.bot.access import JoinUser
from api.payments.ton import check_payment
from middlewares.middleware import AuthMiddleware
from utility.utils import generate_random_code

router = Router()
router.message.middleware(AuthMiddleware())
load_dotenv()
wallet_address_base64 = os.getenv("WALLET_ADRESS_BASE64")
wallet_address_hex16 = os.getenv("WALLET_ADRESS_HEX")


def get_ton_text(wallet_address, memo):
    return f'''
Для оформления подписки переведи *TON* на указанный адрес и ОБЯЗАТЕЛЬНО укажи комментарий (*memo*).
 Ты можешь оплатить подписку только на месяц вперёд.

👉 *Адрес:* `{wallet_address}`
`- - - - - - - - - - - - - - - - -` 
👉 *Memo:* `{memo}`

Стоимость подписки на *1 месяц = 0.7 TON*.
 
P.s: чтобы скопировать *адрес и MEMO*, просто нажми на них. 
'''


@router.message(F.text == "Пополнить через TON 💳")
async def pay_router(message: Message) -> None:
    memo_code = generate_random_code()
    ton_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить оплату⚡", callback_data=f"ton_{memo_code}")]
    ])
    await message.answer("Теперь нужно оплатить подписку", reply_markup=ReplyKeyboardRemove())
    await message.answer(get_ton_text(wallet_address_base64, memo_code), reply_markup=ton_button,
                         parse_mode=ParseMode.MARKDOWN)


@router.callback_query(F.data.startswith("ton_"))
async def ton_reader(query: CallbackQuery):
    memo = query.data.split('_')[1]
    status, error = await check_payment(wallet_address_hex16, memo, 0.7)
    if status:
        await query.answer("Вы успешно оплатили!🥳", show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        if error:
            await query.answer("Случилась ошибка, проверьте логи!☹️")
        else:
            await query.answer("Вы еще не продлили!☹️", show_alert=True)
