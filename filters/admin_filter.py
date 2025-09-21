from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.enums import ChatMemberStatus

from data.db.admins import admins_db

class IsAdminGroup(BaseFilter):
    def __init__(self, bot):
        self.bot = bot

    async def __call__(self, message: Message) -> bool:
        # Faqat guruh va supergroup xabarlarida ishlaydi
        if message.chat.type not in ["group", "supergroup"]:
            return False

        # ChatMember ma'lumotlarini olish
        chat_member = await self.bot.get_chat_member(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )
        
        # Admin yoki owner bo'lsa True, aks holda False
        return chat_member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.type != "private":
            return False
        
        admin_id = message.from_user.id
        admins = admins_db.get_bot_admins()
        for admin in admins:
            if admin_id in admin:
                return True
        return False