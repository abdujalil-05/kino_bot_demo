from aiogram import Router
from aiogram.types import ChatJoinRequest, ChatMemberUpdated
from aiogram import Bot
import json
import ast

from data.db.users import users_db
from data.db.channels import channels_db

router = Router()


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


# ✅ Join request handler
@router.chat_join_request()
async def join_request_handler(request: ChatJoinRequest):
    user = request.from_user
    chat_id = str(request.chat.id)

    # DB'dan user kanallarini olish
    users = users_db.get_user(user_id=user.id)
    user_channels_str = users[0][4] if users else []

    # Toza listga aylantirish
    user_channels = parse_channels(user_channels_str)
    print(user_channels)


    # Kanalni qo‘shish (agar yo‘q bo‘lsa)
    if chat_id not in user_channels:
        user_channels.append(chat_id)

        # DB ga yozish (listni stringga aylantirib saqlash kerak)
        print(user_channels)
        users_db.user_add_channel(
            user_id=user.id,
            channel_id=json.dumps(user_channels)  # json qilib yoziladi
        )


# ✅ Bot guruhga yoki kanalga qo‘shilganda
@router.my_chat_member()
async def bot_added_to_chat(update: ChatMemberUpdated):
    chat = update.chat
    new_status = update.new_chat_member.status
    old_status = update.old_chat_member.status

    bot: Bot = update.bot  # bot obyektini olish
    me = await bot.get_me()

    # faqat botning statusi o'zgarganda
    # if update.new_chat_member.user.id == me.id:
    if old_status in ("left", "kicked") and new_status in ("member", "administrator"):
            # kanal yoki guruhga qo'shilgan
            channel_name = chat.title
            channel_id = chat.id
            username = chat.username if chat.username else None

            # foydalanuvchilar sonini olish
            try:
                members_count = await bot.get_chat_member_count(chat.id)
            except Exception:
                members_count = 0

            # DB ga yozamiz
            print("bot kanalga qo'shildi")
            channels_db.add_bot_channel(channel_name, channel_id, username, members_count)

            # faqat guruhga xabar yuborish mumkin
            if chat.type in ("group", "supergroup"):
                await bot.send_message(chat.id, f"✅ Bot '{channel_name}' ga muvaffaqiyatli qo‘shildi!")