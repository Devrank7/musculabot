import uuid
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from db.sql.model import User
from db.sql.service import AttachWfpDataToUser, run_sql, DetachWfpDataFromUser, CreateAndUpdateFullUser
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


identifiers = [
    409531826, 396149097, 454127114, 1764041558, 828007952, 6335709216,
    5943479419, 459279094, 384757544, 546234588, 499851529, 864984382,
    764973948, 411083054, 1785335155, 463009456, 292305006, 910249809,
    784029450, 888366238, 64283271, 632897321, 477173763, 521550301,
    394342394, 541428214, 396388921, 383213637, 428117994, 305282412,
    229228208, 604582372, 1145072941, 502737145, 606871360, 420280851,
    474042280, 1108033553, 456473894, 58972608, 1067987375, 372187807,
    5795545411, 1950446826, 769548253, 5173665198, 335256472, 736477022,
    828894537, 5378839624, 568922881, 485097043, 932127144, 505618514,
    501212479, 242026062, 1099055586, 576603550, 1033991580, 365243495,
    1676408227, 117434666, 189274144, 860538473, 554583076, 397819684,
    376480803, 5991835904, 575436160
]


@router.message(Command("add_us_mike_boreyko"))
async def create_and_update(message: Message):
    for user in identifiers:
        await run_sql(CreateAndUpdateFullUser(user, datetime(2025, 1, 15, 9, 30)))
    await message.answer("Все пользователи были добавлены!")
