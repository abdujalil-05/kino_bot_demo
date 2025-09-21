from aiogram import Bot
from data.db.config.config import ADMINS

async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(admin, "✅ Bot ishga tushdi")
        except Exception as err:
            print(f"Admin {admin} ga xabar yuborilmadi: {err}")
