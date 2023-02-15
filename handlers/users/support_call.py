from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.inline.support import support_keyboard, support_callback, check_support_available, get_support_manager, \
    cancel_support, cancel_support_callback
from loader import dp, bot


@dp.message_handler(Command("support_call"))
async def ask_support_call(message: types.Message):
    text = "Operator bilan bog'lanish"
    keyboard = await support_keyboard(messages="many")
    if not keyboard:
        await message.answer("Hozir operatorlar yo'q keyinroq urinib ko'ring")
        return
    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="yes"))
async def send_to_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text("Siz operatorga murojaat qildingiz operator javobini kuting")

    user_id = int(callback_data.get("user_id"))
    if not await check_support_available(user_id):
        support_id = await get_support_manager()
    else:
        support_id = user_id

    if not support_id:
        await call.message.edit_text("Hozir operatorlar yo'q keyinroq urinib ko'ring")
        await state.reset_state()
        return

    await state.set_state("wait_in_support")
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(messages="many", user_id=call.from_user.id)

    await bot.send_message(support_id,
                           f"Foydalanuvchi siz bilan bog'lanmoqchi {call.from_user.full_name}",
                           reply_markup=keyboard
                           )


@dp.callback_query_handler(support_callback.filter(messages="many", as_user="no"))
async def answer_support_call(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get("user_id"))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != "operatorni kuting":
        await call.message.edit_text("Murojatingiz jonatilgan o'zgartira olmaysiz")
        return

    await state.set_state("in_support")
    await user_state.set_state("in_support")

    await state.update_data(second_id=second_id)

    keyboard = cancel_support(second_id)
    keyboard_second_user = cancel_support(call.from_user.id)

    await call.message.edit_text("Siz foydalanuvchiga ulagansiz\n"
                                 "suxbatni tugatish tugmasini bosing",
                                 reply_markup=keyboard
                                 )
    await bot.send_message(second_id,
                           "operator online \n"
                           "Murojatingizni qoldirishingiz mumkun",
                           reply_markup=keyboard_second_user
                           )


@dp.message_handler(state="wait_in_support", content_types=types.ContentTypes.ANY)
async def not_supported(message: types.Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get("second_id")

    keyboard = cancel_support(second_id)
    await message.answer("operator javobini kuting yoki seansi bekor qiling", reply_markup=keyboard)


@dp.callback_query_handler(cancel_support_callback.filter(), state=["in_support", "wait_in_support", None])
async def exit_support(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get("second_id")
        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await bot.send_message(user_id, "foydalanuvchi seansni tugatdi")

    await call.message.edit_text("siz sesiyani yakunladingiz")
    await state.reset_state()

