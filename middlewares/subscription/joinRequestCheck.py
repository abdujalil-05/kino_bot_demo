from aiogram import Router, Bot
from aiogram.types import ChatJoinRequest, ChatMemberUpdated

from data.db.users import users_db
import json
import ast

from data.db.channels import channels_db

join_request_check = Router()


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

@join_request_check.chat_join_request()
async def join_request_handler(request: ChatJoinRequest, bot: Bot):
    user = request.from_user
    chat_id = str(request.chat.id)

    # DB'dan user kanallarini olish
    users = users_db.get_user(user_id=user.id)
    user_channels_str = user[0][4] if users != [] else []

    # Toza listga aylantirish
    user_channels = parse_channels(user_channels_str)

    # Kanalni qo‘shish (agar yo‘q bo‘lsa)
    if chat_id not in user_channels:
        user_channels.append(chat_id)

        # DB ga yozish (listni stringga aylantirib saqlash kerak)
        users_db.user_add_channel(
            user_id=user.id,
            channel_id=json.dumps(user_channels)  # json qilib yoziladi
        )


@join_request_check.chat_member()
async def chat_member_handler(update: ChatMemberUpdated):
    user = update.from_user
    chat = update.chat

    old_status = update.old_chat_member.status
    new_status = update.new_chat_member.status

    # 1️⃣ User qo'shildi
    if old_status in ("left", "kicked") and new_status == "member":
        get_user = users_db.get_user(user.id)

        await update.bot.send_message(
            chat.id,
            f"👋 {user.full_name} guruhga qo'shildi!"
        )

    # 2️⃣ User chiqib ketdi
    elif old_status == "member" and new_status == "left":
        await update.bot.send_message(
            chat.id,
            f"👋 {user.full_name} guruhdan chiqib ketdi."
        )

    # 3️⃣ User chiqarib yuborildi (ban)
    elif new_status == "kicked":
        await update.bot.send_message(
            chat.id,
            f"⛔️ {user.full_name} guruhdan chiqarildi."
        )
