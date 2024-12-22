from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from buttons.inline import get_subscribe, get_dismiss1, get_dismiss_wtf_button
from db.sql.model import User
from lang.language import translate
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


@router.message(CommandStart())
async def start_router(message: Message, user: User):
    print(f"LANG: {user.lang}")
    end = ''
    end1 = ''
    buttons = get_subscribe(user)
    if check_access_for_chanel(user):
        if user.wfp_data:
            buttons = get_dismiss_wtf_button(user)
            end = ('🔊У вас установлено авто списание через wayforpay. Вы можете его отключить.'
                   'Если отключить. Подписку вы не потеряете🤟, но через месяц автоматически она не продлится💫 \n'
                   'и прийдется выбирать платежную систему для оплаты подписки на канал.')
        else:
            buttons = get_dismiss1(user)
        end1 = "*У Вас есть подписка до " + user.date_of_kill.strftime('%d.%m.%Y').replace('.', '\\.') + '*'
    end_text = translate("14", user.lang) if end else ''
    end_text1 = translate("36", user.lang) if end1 else ''
    await message.answer(f"{translate("13", user.lang)}. {end_text} {end_text1}", reply_markup=buttons,
                         parse_mode=ParseMode.MARKDOWN)
