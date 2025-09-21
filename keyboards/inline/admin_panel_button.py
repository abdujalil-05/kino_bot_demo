from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

admin_panel_menu = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            InlineKeyboardButton(text="🎬 Kino qo'shish ✅", callback_data="add_movie"),
            InlineKeyboardButton(text="🎞️ Serial qo'shish", callback_data="add_serial"),
        ],
        
        [
            InlineKeyboardButton(text="🟥 Kinoni o'chirish ✅", callback_data="delete_movie"),
            InlineKeyboardButton(text="🗑️ Serialni o'chirish", callback_data="delete_movie"),
        ],
        [
            InlineKeyboardButton(text="👮🏻‍♀️ Admin qo'shish ✅", callback_data="add_admin"),
            InlineKeyboardButton(text="📊 Statistika", callback_data="statistika"),

        ],
        [
            InlineKeyboardButton(text="🚫 Adminlikdan olish ✅", callback_data="delete_admin"),
        ],
        [
            InlineKeyboardButton(text="🔐 Zayafka yig'ish ✅", callback_data="private_channel_group"),
            InlineKeyboardButton(text="🟢 Kanal guruh qo'shish", callback_data="public_channel_group"),

        ],
        [
            InlineKeyboardButton(text="🗑️ Kanalni o'chirish ✅", callback_data="delete_channel_group"),
        ],
    ]
)

def admin_channels_menu_generate(channels):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=channel[1], callback_data=f"channel,{channel[1]},{channel[2]}")]
        for channel in channels
      
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="back 🔙", callback_data="channel,back")
    ])

    return keyboard

def admin_delete_channels_menu_generate(channels):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"{channel[0]}", callback_data=f"delete,{channel[1]},{channel[3]}") if channel[0] == "back" else InlineKeyboardButton(text=f"{channel[2]} | {channel[1]}", callback_data=f"delete,{channel[1]},{channel[3]}")]
        for channel in channels
            
    ])
    # ✅ "Tekshirish" tugmasi callback uchun
    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="back 🔙", callback_data="delete,back")
    ])
    return keyboard



def delete_channel_group_keyboard(channel):
    print(channel)
    keyboard = InlineKeyboardMarkup(
        inline_keyboard= [
            [
                InlineKeyboardButton(text="Ha ✅", callback_data=f"yes_delete,{channel}"),
                InlineKeyboardButton(text="Yo'q ❌", callback_data="no_delete"),

            ],
        ]
    )
    return keyboard



def delete_admin_inline_button(admins):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"👮🏻‍♀️ {admin[1]}", callback_data=f"admin,{admin[2]}")]
        for admin in admins
      
    ])

    keyboard.inline_keyboard.append([
        InlineKeyboardButton(text="back 🔙", callback_data="admin,back")
    ])

    return keyboard