from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_channels_keyboard(notSubscriptions):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=channel[2], url=channel[1])]
        for channel in notSubscriptions
            
    ])

    # ✅ "Tekshirish" tugmasi callback uchun
    # keyboard.inline_keyboard.append([
    #     InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subs")
    # ])

    return keyboard

