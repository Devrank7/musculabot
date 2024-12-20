from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "chat_id")
async def forward(message: Message):
    chat_id = message.forward_from_chat.id
    await message.answer(f"Chat id: {chat_id}")
