from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from buttons.inline import get_support
from db.sql.model import User
from lang.language import translate
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(Command("support"))
async def support(message: Message, user: User):
    await message.answer(translate("12", user.lang), reply_markup=get_support(user))
