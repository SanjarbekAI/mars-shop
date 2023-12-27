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

phone_share = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="☎️ Telefon raqamni yuborish", request_contact=True)
    ]], resize_keyboard=True
)