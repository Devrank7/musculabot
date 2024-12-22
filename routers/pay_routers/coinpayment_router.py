from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove

from api.bot.access import JoinUser
from api.payments.coinpayments import create_transaction, check_payment_status
from middlewares.middleware import AuthMiddleware

router = Router()
router.message.middleware(AuthMiddleware())


@router.message(F.text == "Пополнить через Coinpayment 💵")
async def pay_router(message: Message) -> None:
    tx_id, url = create_transaction(4, "Лучший канал Muscle Lab", "week2735@gmail.com")
    cp_button = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 💳", url=url)],
        [InlineKeyboardButton(text='Проверить оплату ⚡', callback_data=f"cp_{tx_id}")]
    ])
    await message.answer("Теперь нужно оплатить подписку", reply_markup=ReplyKeyboardRemove())
    await message.answer("Вы используете Coinpayment для оплаты в лучший канал бодибилдеров 🦍."
                         "Для этого оплатите нажав на кнопку 'Оплатить' , после оплати нажмите 'Проверить оплату'👌",
                         reply_markup=cp_button)


@router.callback_query(F.data.startswith('cp_'))
async def coinpayment_callback(query: CallbackQuery):
    tx_id = query.data.split('_')[1]
    status, ok = check_payment_status(tx_id)
    if ok:
        await query.answer("Вы успешно оплатили через Coinpayment!🥳", show_alert=True)
        await query.message.delete()
        await JoinUser(query.bot, query.from_user.id).task()
    else:
        await query.answer("Coinpayment еще не подтвердил транзакцию или вы не оплатили!☹️ Если вы все же оплатили,"
                           "то подождите немного от 10 до 35 минут, к тому времени все должно пройти успешно!",
                           show_alert=True)
