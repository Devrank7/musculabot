from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton

from db.sql.enums.enums import Lang
from db.sql.model import User
from db.sql.service import run_sql, UpdateUserLang
from lang.language import translate
from middlewares.middleware import AuthMiddlewareCallbackWithoutLang, AuthMiddlewareWithoutLang

router = Router()
router.callback_query.middleware(AuthMiddlewareCallbackWithoutLang())
router.message.middleware(AuthMiddlewareWithoutLang())

lang_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ru 🇷🇺', callback_data="lang_ru"),
     InlineKeyboardButton(text="ua 🇺🇦", callback_data="lang_ua")]
])


@router.message(Command("lang"))
async def set_lang(message: Message, user: User):
    if user.lang:
        await message.answer(translate("27", user.lang), reply_markup=lang_buttons)
    else:
        await message.answer("Пожалуйста выберете язык🌎")


@router.callback_query(F.data.startswith('lang_'))
async def lang_callback(query: CallbackQuery, user: User):
    lang = query.data.split("_")[1]
    if lang == "ua":
        await run_sql(UpdateUserLang(user.tg_id, Lang.UA))
        await query.message.edit_text("Ваша мова змінилася на українську 🇺🇦. Щоб взаємодіяти з ботом, натисніть /start")
    elif "ru":
        await run_sql(UpdateUserLang(user.tg_id, Lang.RU))
        await query.message.edit_text("Ваш язык изменился на русский 🇷🇺. Для взаимодействия с ботом нажмите /start")
