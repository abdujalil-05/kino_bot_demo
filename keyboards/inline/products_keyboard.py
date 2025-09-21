from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

products = {
    "course_python": "🐍 Python kursi",
    "course_java": "☕ Java kursi",
    "course_js": "🌐 JavaScript kursi",
    "course_csharp": "🔷 C# kursi",
    "course_flutter": "📱 Flutter kursi",
    "course_html": "📱 HTML kursi",
    "course_back": "🔙 ortga"
    # ... shu tarzda 20 ta mahsulot
}


category = InlineKeyboardMarkup(
    inline_keyboard= [
        [
            
            InlineKeyboardButton(text="💻 Kurslar", callback_data="courses"),
            InlineKeyboardButton(text="📕 Kitoblar", callback_data="books"),
        ],
        [
            InlineKeyboardButton(text="📥 Elon berish", url="t.me/bosh_director"),
        ],
        [
            InlineKeyboardButton(text="🔎 Qidirish", switch_inline_query_current_chat=""),
        ],
        [
            InlineKeyboardButton(text="📲 Ulashish", switch_inline_query="Yaxshi bot ekan"),
        ],
    ]
)


# def generate_courses_keyboard(products: dict) -> InlineKeyboardMarkup:
#     keyboard = []
#     row = []
#     for i, (code, name) in enumerate(products.items(), start=1):
#         row.append(
#             InlineKeyboardButton(text=name, callback_data=f"course_{code}")
#         )
#         if i % 2 == 0:  # Har qatorga 2 ta tugma
#             keyboard.append(row)
#             row = []
#     if row:
#         keyboard.append(row)

#     return InlineKeyboardMarkup(inline_keyboard=keyboard)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_courses_keyboard(products: dict) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    
    for i, (code, name) in enumerate(products.items(), start=1):
        # Agar bu "back" tugmasi bo'lsa, uni alohida qatorda qo'yamiz
        if code == "course_back":
            if row:                # agar yarim qator tugmalar qolgan bo‘lsa, uni ham qo‘shib yuboramiz
                keyboard.append(row)
                row = []
            keyboard.append([InlineKeyboardButton(text=name, callback_data=f"course_{code}")])
            continue

        # Oddiy tugma
        row.append(InlineKeyboardButton(text=name, callback_data=f"course_{code}"))

        if len(row) == 2:   # Har qatorga 2 ta tugma
            keyboard.append(row)
            row = []

    # Agar oxirida yarim qator qolgan bo‘lsa, uni ham qo‘shamiz
    if row:
        keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


coursesMenu = generate_courses_keyboard(products)
