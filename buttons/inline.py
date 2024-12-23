from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.sql.model import User
from lang.language import inline_translate


def get_dismiss(user: User):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("1", user.lang), callback_data="dismiss")],
        [InlineKeyboardButton(text=inline_translate("2", user.lang), callback_data="unity")]
    ])


def get_dismiss1(user: User):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("5", user.lang), callback_data="dismiss")]
    ])


def get_dismiss_wtf_button(user: User):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("5", user.lang), callback_data="dismiss")],
        [InlineKeyboardButton(text=inline_translate("6", user.lang), callback_data="Удалить текущий регулярный платеж")]
    ])


def get_subscribe(user: User):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("3", user.lang), callback_data="unity")],
    ])


def get_support(user: User):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("4", user.lang), url="https://t.me/boreyko_mike")]
    ])


def get_wtf_buttons(user: User, url, order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("7", user.lang), url=url[0])],
        [InlineKeyboardButton(text=inline_translate("8", user.lang), callback_data=f"wfp_{order_id}")]
    ])


def get_ton_buttons(user: User, memo, require: float):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("8", user.lang), callback_data=f"ton_{memo}_{require}")]
    ])


def get_cp_button(user: User, url, tx_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("7", user.lang), url=url)],
        [InlineKeyboardButton(text=inline_translate("8", user.lang), callback_data=f"cp_{tx_id}")]
    ])


def get_dis(user: User):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=inline_translate("9", user.lang), callback_data="dis_yes"),
         InlineKeyboardButton(text=inline_translate("10", user.lang), callback_data="dis_not")]
    ])
