import os

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from dotenv import load_dotenv

from api.bot.access import JoinUser
from api.payments.ton import check_payment
from buttons.inline import get_ton_buttons
from db.sql.model import User
from filter.reply import ReplyFilter
from lang.language import translate
from middlewares.middleware import AuthMiddleware, AuthMiddlewareCallback
from utility.utils import generate_random_code

router = Router()
router.message.middleware(AuthMiddleware())
router.message.middleware(AuthMiddlewareCallback())
load_dotenv()
wallet_address_base64 = os.getenv("WALLET_ADRESS_BASE64")
wallet_address_hex16 = os.getenv("WALLET_ADRESS_HEX")


def get_ton_text(wallet_address, memo, user: User):
    return f'''
{translate("37", user.lang)}

👉 *Адрес:* `{wallet_address}`
`- - - - - - - - - - - - - - - - -` 
👉 *Memo:* `{memo}`

{translate("38", user.lang)}
'''


@router.message(ReplyFilter('1'))
async def pay_router(message: Message, user: User) -> None:
    memo_code = generate_random_code()
    ton_button = get_ton_buttons(user, memo_code)
    await message.answer(translate("19", user.lang), reply_markup=ReplyKeyboardRemove())
    await message.answer(get_ton_text(wallet_address_base64, memo_code, user), reply_markup=ton_button,
                         parse_mode=ParseMode.MARKDOWN)


@router.callback_query(F.data.startswith("ton_"))
async def ton_reader(query: CallbackQuery, user: User):
    memo = query.data.split('_')[1]
    status, error = await check_payment(wallet_address_hex16, memo, 0.6)
    if status:
        await query.answer(translate("22", user.lang), show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        if error:
            await query.answer("Случилась ошибка, проверьте логи!☹️")
        else:
            await query.answer(translate("23", user.lang),
                               show_alert=True)
