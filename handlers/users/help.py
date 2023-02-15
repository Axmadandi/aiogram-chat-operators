from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar ro\'yxati: ",
            "/start - Botni ishga tushurish",
            "/help - Yordam")
    
    await message.answer("\n".join(text))
