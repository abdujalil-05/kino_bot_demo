from aiogram import Router
from aiogram.types import Message

from data.db.movies import movies
from filters.private_chat_filter import IsPrivateChat

import re

router = Router()

# faqat butun sonlar
patterns = r"^\d+$"

@router.message(IsPrivateChat())
async def movie_code_handler(message: Message):
    message_text = message.text or ""
    if re.match(patterns, message_text):
        data = movies.get_movie(message.text)
        if data:
            if data[1]:
                language = ""
                if data[0][3] == "uzbek":
                    language = "🇺🇿 Til: Uzbek tilida"
                elif data[0][3] == "rus":
                    language = "🇷🇺 Til: Rus tilida"
                else:
                    language = "🇺🇸 Til: Ingliz tilida"

                movie_text = (
                    f"🎥 Kino nomi: {data[0][1]}\n\n"
                    f"{language}\n"
                    f"📊 Rating: {data[0][7]}\n"
                    f"📅 Yili: {data[0][2]}\n\n"
                    f"🎭 Kinoning janri: {data[0][4]}\n\n"
                    f"💬 Kino haqida qisqacha: {data[0][6]}\n\n"
                    f"🟢 Bizning kanallarga obuna bo'ling:\n"
                    f"@username\n@username\n@username"
                )

                await message.bot.send_video(
                    chat_id=message.chat.id,
                    video=data[0][5],
                    caption=movie_text,
                )
        else:
            await message.answer("❌ Bunday kodli kino mavjud emas. Iltimos tekshirib qaytadan yuboring!")

        pass
    else:
        await message.answer("❌ Bunday kodli kino mavjud emas. Iltimos tekshirib qaytadan yuboring!")
