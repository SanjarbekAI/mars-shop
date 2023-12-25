from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def mars_bozor_pagination(total_products, index):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅️", callback_data="previous_product"),
                InlineKeyboardButton(text=f"{index + 1}/{total_products}", callback_data="show"),
                InlineKeyboardButton(text="➡️", callback_data="next_product"),
            ]
        ]
    )
    return markup