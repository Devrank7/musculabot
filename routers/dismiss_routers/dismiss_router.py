from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from api.bot.access import KickUser
from api.payments.wayforpay_api import remove_regular_invoice
from buttons.inline import get_dis
from db.sql.model import User
from db.sql.service import DetachWfpDataFromUser, run_sql
from lang.language import translate
from middlewares.middleware import AuthMiddlewareCallback

router = Router()
router.callback_query.middleware(AuthMiddlewareCallback())


@router.callback_query(F.data == 'dismiss')
async def dis_callback(query: CallbackQuery, state: FSMContext, user: User):
    await query.answer()
    await state.update_data(dis_previous_text=query.message.text)
    await state.update_data(dis_previous_reply=query.message.reply_markup)
    await query.message.edit_text(translate("28", user.lang), reply_markup=get_dis(user))


@router.callback_query(F.data.startswith('dis_'))
async def dismiss_callback(query: CallbackQuery, user: User, state: FSMContext):
    status = query.data.split("_")[1]
    if status == 'yes':
        await query.message.edit_text(translate("29", user.lang))
        if user.wfp_data:
            order = user.wfp_data.order
            await remove_regular_invoice(order)
            await run_sql(DetachWfpDataFromUser(user.tg_id))
            await query.message.answer(translate("30", user.lang))
        await query.answer("Good Buy!")
        await KickUser(query.bot, user.tg_id, left=True).task()
    else:
        data = await state.get_data()
        text = data['dis_previous_text']
        reply_buttons = data['dis_previous_reply']
        await query.answer("<<>>")
        await query.message.edit_text(text, reply_markup=reply_buttons)
    await state.clear()
