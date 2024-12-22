from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

support_text = '''
Если у вас возникли проблемы,
или вы хотите узнать более подробную информацию о проекте,
нажмите на кнопку ниже👇
'''
support_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Связаться со мной", url="https://t.me/boreyko_mike")]
])


@router.message(Command("support"))
async def support(message: Message):
    await message.answer(support_text, reply_markup=support_button)
