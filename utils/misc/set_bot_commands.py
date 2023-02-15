from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Botni qayta ishga tushuirsh"),
        types.BotCommand("admin", "Admin bilan boglanish"),
        types.BotCommand("support_call", "Admin start"),
        types.BotCommand("help", "Yordam"),
    ])
