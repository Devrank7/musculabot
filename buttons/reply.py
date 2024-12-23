from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from db.sql.model import User
from lang.language import reply_translate


def pay_buttons(user: User):
    return ReplyKeyboardMarkup(keyboard=[
        # [KeyboardButton(text=reply_translate("1", user.lang))],
        [KeyboardButton(text=reply_translate("2", user.lang))],
        [KeyboardButton(text=reply_translate("3", user.lang))],
        # [KeyboardButton(text="Пополнить через Liqpay")],
    ], resize_keyboard=True, one_time_keyboard=True)


def regular_but(user: User):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=reply_translate("5", user.lang))]
    ])


def regular_but1(user: User):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=reply_translate("4", user.lang))]
    ])
