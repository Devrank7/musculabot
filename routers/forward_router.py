import uuid

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from db.sql.model import User
from db.sql.service import AttachWfpDataToUser, run_sql, DetachWfpDataFromUser
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == "chat_id")
async def forward(message: Message):
    chat_id = message.forward_from_chat.id
    await message.answer(f"Chat id: {chat_id}")


@router.message(Command("attach"))
async def attach_test(message: Message, user: User):
    if user.wfp_data is None:
        random_order = uuid.uuid4().hex
        await run_sql(AttachWfpDataToUser(user.tg_id, random_order))
        await message.answer("Attach")
    else:
        await message.answer("Already attach")


@router.message(Command("detach"))
async def detach_test(message: Message, user: User):
    if user.wfp_data:
        await run_sql(DetachWfpDataFromUser(user.tg_id))
        await message.answer("Detach")
    else:
        await message.answer("Already detach")
