from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from typing import Callable, Awaitable, Any

from data.db.users import users_db
from data.db.channels import channels_db
from keyboards.inline.subscribe import generate_channels_keyboard

import json
import ast
import asyncio
import time


# String -> List aylantirish uchun universal parser
def parse_channels(data: str):
    if not data:
        return []
    try:
        return json.loads(data)  # JSON format bo'lsa
    except json.JSONDecodeError:
        try:
            return ast.literal_eval(data)  # Python list string bo'lsa
        except Exception:
            return []


# 🛡 Flood control uchun cache
user_last_message_time = {}
FLOOD_LIMIT = 2  # sekund (2 sekunddan tez yozsa bloklanadi)


class CheckSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any:
        if not event.message and not event.callback_query:
            return await handler(event, data)

        if event.message:
            user_id = event.message.from_user.id
            message = event.message
        else:
            user_id = event.callback_query.from_user.id
            message = event.callback_query.message

        if message.chat.type != "private":
            return

        # 🛑 Flood nazorat
        now = time.time()
        last_time = user_last_message_time.get(user_id, 0)
        if now - last_time < FLOOD_LIMIT:
            await message.answer("⚠️ Juda tez yozayapsiz, biroz kuting.")
            return
        user_last_message_time[user_id] = now


        # 🔹 DB dan kanal/guruhlar ro‘yxatini olish
        channels = channels_db.get_channels()
        user = users_db.get_user(user_id=user_id)

        # Agar user bo‘lmasa, yangi yozuv ochamiz
        if not user:
            users_db.add_user(
                username=message.from_user.username,
                name=message.from_user.full_name,
                user_id=user_id
            )
            user_channels = []
        else:
            user_channels = parse_channels(user[0][4])

        # 🔹 Real tekshiruv (parallel asyncio bilan)
        async def check_one_channel(ch_id: str):
            try:
                member = await data["bot"].get_chat_member(chat_id=int(ch_id), user_id=user_id)
                if member.status in ["member", "administrator", "creator"]:
                    return ch_id, True
                return ch_id, False
            except Exception:
                return ch_id, False

        results = await asyncio.gather(
            *[check_one_channel(str(ch[3])) for ch in channels]
        )

        not_subscribed = [ch for ch, ok in results if not ok]
        if user_channels != [] and not_subscribed != []:
            for channel in user_channels:
                if channel in not_subscribed:
                    not_subscribed.remove(channel)

        # ✅ Agar hamma joyga obuna bo‘lsa
        if not not_subscribed:
            return await handler(event, data)
        else:
            # ❌ Obuna bo‘lmaganlar ro‘yxatini chiqaramiz
            keyboard = generate_channels_keyboard(
                notSubscriptions=[c for c in channels if str(c[3]) in not_subscribed]
            )
            if message.text == "/start":
                welcome_text = (
                    "🎬 **Kino Botimizga xush kelibsiz!** 🎬\n\n"
                    "Bu yerda siz eng so‘nggi filmlarni topishingiz va yuklab olishingiz mumkin.\n\n"
                    "🔹 Filmlarni qidirish uchun, kino kodini yuboring.\n"
                    "🔹 Yoki quyidagi tugmalardan foydalaning:\n"
                    "   • /new - Yangi filmlar\n"
                    "   • /top - Top reytingdagi filmlar\n\n"
                    "Yoqimli tomosha! 🍿\n\n"
                    "❌ Botdan foydalanish uchun.\nIltimos quyidagi kanal(lar)ga obuna bo‘ling:"
                )
                await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)
            else:
                try:
                    await message.bot.delete_message(
                        chat_id=message.chat.id,
                        message_id=message.message_id - 1
                    )
                except Exception as e:
                    print(f"Hato yuz berdi: {e}")
                await message.answer(
                    "❌ Botdan foydalanish uchun.\nIltimos quyidagi kanallarga obuna bo‘ling:",
                    reply_markup=keyboard
                )
            return






