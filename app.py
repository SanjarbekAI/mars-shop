from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from default_keyboards import user_main_menu
from environs import Env

from inline_keyboards import mars_bozor_pagination
from sql.insert import insert_product
from sql.select import get_all_products
from states import ProductAddState
from utils import next_product, previous_product

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
PROXY = env.str("PROXY")
DB_NAME = env.str("DB_NAME")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, proxy=PROXY)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    text = "Botimizga xush kelibsiz."
    await message.answer(text=text, reply_markup=user_main_menu)


@dp.message_handler(text="➕ Mahsulot qo'shish")
async def add_product_handler(message: types.Message):
    text = "Iltimos rasmini kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await ProductAddState.photo.set()


@dp.message_handler(state=ProductAddState.photo, content_types=types.ContentTypes.PHOTO)
async def get_photo_handler(message: types, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    text = "Iltimos mahsulot nomini kiriting"
    await message.answer(text=text)
    await ProductAddState.name.set()


@dp.message_handler(state=ProductAddState.name)
async def get_name_handler(message: types, state: FSMContext):
    await state.update_data(name=message.text)
    text = "Iltimos mahsulot haqida ma'lumot kiriting"
    await message.answer(text=text)
    await ProductAddState.info.set()


@dp.message_handler(state=ProductAddState.info)
async def get_info_handler(message: types, state: FSMContext):
    await state.update_data(info=message.text)
    text = "Iltimos mahsulot narxini kiriting"
    await message.answer(text=text)
    await ProductAddState.price.set()


@dp.message_handler(state=ProductAddState.price)
async def get_price_handler(message: types, state: FSMContext):
    await state.update_data(price=message.text, status="active", chat_id=message.chat.id)
    data = await state.get_data()
    product = await insert_product(data)
    if product:
        text = "Mahsulot bozorga qo'shildi ✅"
    else:
        text = "Botda xatolik bor ❌"
    await message.answer(text=text, reply_markup=user_main_menu)
    await state.finish()


@dp.message_handler(text="🚀 Mars Bozor")
async def mars_bozor_handler(message: types.Message, state:FSMContext):
    products = await get_all_products()
    if products:
        await state.update_data(index=0)
        product = products[0]
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}"
        await message.answer_photo(photo=photo, caption=caption, reply_markup=await mars_bozor_pagination(len(products), 0))
    else:
        text = "Aktiv mahsulotlar mavjud emas"
        await message.answer(text=text, reply_markup=user_main_menu)


@dp.callback_query_handler(text="next_product")
async def next_product_handler(call: types.CallbackQuery, state:FSMContext):
    products = await get_all_products()
    data = await state.get_data()
    index = data.get('index')

    product = await next_product(products, index)
    if product:
        await call.message.delete()
        index = index + 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan keyin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(text="previous_product")
async def previous_product_handler(call: types.CallbackQuery, state: FSMContext):
    products = await get_all_products()
    data = await state.get_data()
    index = data.get('index')

    product = await previous_product(products, index)
    if product:
        await call.message.delete()
        index = index - 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                        reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan oldin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
