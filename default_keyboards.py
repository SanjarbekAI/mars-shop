from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🚀 Mars Bozor"),
            KeyboardButton(text="🖱 Mahsulotlarim"),
        ],
        [
            KeyboardButton(text="👤 Profil"),
            KeyboardButton(text="➕ Mahsulot qo'shish"),
        ]
    ], resize_keyboard=True
)