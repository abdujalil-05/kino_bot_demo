from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from filters.private_chat_filter import IsPrivateChat

import random

router = Router()

@router.message(IsPrivateChat(), Command("start"))
async def start_handler(message: Message):

    welcome_text = (
            "🎬 **Kino Botimizga xush kelibsiz!** 🎬\n\n"
            "Bu yerda siz eng so‘nggi filmlarni topishingiz va yuklab olishingiz mumkin.\n\n"
            "🔹 Filmlarni qidirish uchun, kino kodini yuboring.\n"
           "🔹 Yoki quyidagi tugmalardan foydalaning:\n"
            "   • /new - Yangi filmlar\n"
            "   • /top - Top reytingdagi filmlar\n\n"
            "Yoqimli tomosha! 🍿\n\n"
            "🔎 Kino kodini yuboring\n"
            f"🟢 Misol uchun: {random.randint(1, 99)}\n"
            )

    await message.answer(welcome_text)