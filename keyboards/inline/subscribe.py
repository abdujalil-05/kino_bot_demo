from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# def generate_channels_keyboard(userId):
#     core = Core()
#     user = core.get_user(user_id=userId)
#     channels = user[0][4].split(",") if user and user[0][4] else []

#     getChannels = core.get_channels()
#     notSubscriptions = [
#         (channel[1], channel[2]) for channel in getChannels if channel[1] not in channels
#     ]

#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text=name, url=username, callback_data=f"channel_{username}")]
#         for username, name in notSubscriptions
#     ])

#     # ✅ "Tekshirish" tugmasi callback uchun
#     keyboard.inline_keyboard.append([
#         InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")
#     ])

#     return keyboard





def generate_channels_keyboard(notSubscriptions):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=channel[2], url=channel[1])]
        for channel in notSubscriptions
            
    ])

    # ✅ "Tekshirish" tugmasi callback uchun
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")
    ])

    return keyboard

