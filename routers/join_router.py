import os
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import ChatJoinRequest
from dotenv import load_dotenv

from db.sql.model import User
from db.sql.service import ReadUser, run_sql
from lang.language import translate

router = Router()
load_dotenv()
CHAT_ID = int(os.environ.get("CHAT_ID"))


def fit_user(user: User) -> bool:
    if user.date_of_kill is None:
        return False
    return user.date_of_kill > (datetime.now() + timedelta(minutes=1))


@router.chat_join_request(F.chat.id == CHAT_ID)
async def join_chat_request(join_request: ChatJoinRequest):
    print("Join chat request: {}".format(join_request))
    user: User = await run_sql(ReadUser(tg_id=join_request.from_user.id))
    if user:
        if fit_user(user):
            await join_request.approve()
            await join_request.bot.send_message(user.tg_id, translate("16", user.lang))
            return
    await join_request.bot.send_message(user.tg_id, translate("17", user.lang))
    await join_request.decline()
