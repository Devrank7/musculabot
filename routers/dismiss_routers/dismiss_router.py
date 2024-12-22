from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from api.bot.access import KickUser
from api.payments.wayforpay_api import remove_regular_invoice
from db.sql.model import User
from db.sql.service import DetachWfpDataFromUser, run_sql
from middlewares.middleware import AuthMiddlewareCallback

router = Router()
router.callback_query.middleware(AuthMiddlewareCallback())

dismiss_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data="dis_yes"),
     InlineKeyboardButton(text="Нет", callback_data="dis_not")]
])


@router.callback_query(F.data == 'dismiss')
async def dis_callback(query: CallbackQuery, state: FSMContext):
    await query.answer()
    await state.update_data(dis_previous_text=query.message.text)
    await state.update_data(dis_previous_reply=query.message.reply_markup)
    await query.message.edit_text("Вы точно в этом уверены!?", reply_markup=dismiss_button)


@router.callback_query(F.data.startswith('dis_'))
async def dismiss_callback(query: CallbackQuery, user: User, state: FSMContext):
    status = query.data.split("_")[1]
    if status == 'yes':
        await query.message.edit_text('Мы будем скучать! Удачи в тренировках🔩')
        if user.wfp_data:
            order = user.wfp_data.order
            await remove_regular_invoice(order)
            await run_sql(DetachWfpDataFromUser(user.tg_id))
            await query.message.answer("Авто списывание через wayforpay было удаленно😌")
        await query.answer("Мы будем скучать!")
        await KickUser(query.bot, user.tg_id, left=True).task()
    else:
        data = await state.get_data()
        text = data['dis_previous_text']
        reply_buttons = data['dis_previous_reply']
        await query.answer("Назад")
        await query.message.edit_text(text, reply_markup=reply_buttons)
    await state.clear()
