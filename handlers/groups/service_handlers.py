# from aiogram import types, Router
# from filters.group_filter import IsGroup


# router = Router()


# @router.message(IsGroup(), content_tpyes=types.ContentType.NEW_CHAT_MEMBERS)
# async def new_member(message: types.Message):
#     # members = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
#     members = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
#     await message.reply(f"Xush kelibsiz {members}.")


from aiogram import types, Router
from filters.group_filter import IsGroup
from aiogram.enums import ParseMode
# from aiogram.filters import F

router = Router()

@router.message(IsGroup(), lambda message: message.content_type == types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    # members = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
    members = ", ".join(
        [f"<a href='tg://user?id={m.id}'>{m.full_name}</a>" for m in message.new_chat_members])
    await message.answer(f"Xush kelibsiz {members}.")


@router.message(IsGroup(), lambda message: message.content_type == types.ContentType.LEFT_CHAT_MEMBER)
async def banned_or_left_group_member(message: types.Message):
    if message.from_user.id == message.left_chat_member.id:
        print(message.left_chat_member, type(message.left_chat_member,))
        members = f"<a href='tg://user?id={message.left_chat_member.id}'>{message.left_chat_member.full_name}</a> guruhni tark etdi"
        await message.answer(f"{members}", parse_mode=ParseMode.HTML)
