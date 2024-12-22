from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from db.sql.model import User
from middlewares.middleware import AuthMiddleware
from utility.utils import check_access_for_chanel

router = Router()
router.message.middleware(AuthMiddleware())
start_message_text = """
Привет🫡

Здесь можно получить доступ в закрытый канал, где ты будешь получать эксклюзивные материалы, а именно:
🔸ежемесячные планы тренировок;
🔸статьи на темы разборов тренировок и питания с исследованиями, мыслями и цитатами из научных статей;
🔸стримы с ответами на вопросы участников канала;
🔸эксклюзивный контент от меня;

💵Цена подписки \\- _*всего 4$ в месяц\\!*_

🔥Минимум стоимости за максимум контента и пользы\\.
Жду тебя в комьюнити🦍
🤝Связь с поддержкой /support
"""
buttons_subscribe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Получить доступ в комьюнити🦾", callback_data="unity")],
])
dismiss_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить подписку", callback_data="dismiss")]
])
dismiss_wtf_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Отменить подписку", callback_data="dismiss")],
    [InlineKeyboardButton(text="Отменить авто списание через WFP")]
])


@router.message(CommandStart())
async def start_router(message: Message, user: User):
    end = ''
    buttons = buttons_subscribe
    if check_access_for_chanel(user):
        if user.wfp_data:
            buttons = dismiss_button
            end = ('🔊У вас установлено авто списание через wayforpay. Вы можете его отключить.'
                   'Если отключить. Подписку вы не потеряете🤟, но через месяц автоматически она не продлится💫 \n'
                   'и прийдется выбирать платежную систему для оплаты подписки на канал.')
        else:
            buttons = dismiss_button
        end += "*У Вас есть подписка до " + user.date_of_kill.strftime('%d.%m.%Y').replace('.', '\\.') + '*'
    await message.answer(f"{start_message_text}. {end}", reply_markup=buttons, parse_mode=ParseMode.MARKDOWN)
