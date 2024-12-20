from aiogram import Router, F
from aiogram.types import CallbackQuery

from api.bot.access import KickUser
from db.sql.model import User
from middlewares.middleware import AuthMiddlewareCallback

router = Router()
router.callback_query.middleware(AuthMiddlewareCallback())


@router.callback_query(F.data == 'dismiss')
async def dismiss_callback(query: CallbackQuery, user: User):
    await query.answer("Мы будем скучать!")
    await KickUser(query.bot, user.tg_id, left=True).task()
