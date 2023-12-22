from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def product_pagination_button(index, total_products):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ortga", callback_data="back"),
                InlineKeyboardButton(text=f"{index + 1}/{total_products}", callback_data="show"),
                InlineKeyboardButton(text="Keyingi", callback_data="next"),
            ]
        ]
    )
    return markup