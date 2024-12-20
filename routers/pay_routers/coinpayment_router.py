from aiogram import Router, F
from aiogram.types import Message

from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == "Пополнить через Coinpayment")
async def pay_router(message: Message) -> None:
    pass
