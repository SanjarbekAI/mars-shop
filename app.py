from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from default_keyboards import user_main_menu, phone_share
from environs import Env

from inline_keyboards import mars_bozor_pagination
from sql.insert import insert_product, insert_user
from sql.select import get_all_products, get_user, get_user_all_products
from states import ProductAddState, RegisterState
from utils import next_product, previous_product, login_def

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
PROXY = env.str("PROXY")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, proxy=PROXY)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start", state="*")
async def start_handler(message: types.Message):
    user = await get_user(chat_id=message.chat.id)
    if user:
        text = "Botimizga xush kelibsiz."
        await message.answer(text=text, reply_markup=user_main_menu)
    else:
        text = "Iltimos telefon raqamingizni kiriting"
        await message.answer(text=text, reply_markup=phone_share)
        await RegisterState.phone_number.set()
        
    
@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentTypes.CONTACT)
async def get_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    text = "Iltimos, Mars Space uchun mo'jallangan login ni kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.login.set()
    

@dp.message_handler(state=RegisterState.login)
async def get_login_number(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    text = "Iltimos, Mars Space uchun mo'jallangan password ni kiriting"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.password.set()


@dp.message_handler(state=RegisterState.password)
async def get_password_number(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text, chat_id=message.chat.id)
    data = await state.get_data()
    login = data.get('login')
    password = data.get('password')
    student = login_def(login, password)
    if student:
        await state.update_data(full_name=student)
        data = await state.get_data()
        if await insert_user(data):
            text = f"Tabriklaymiz, siz muvafaqqiyatli ro'yxatdan o'tdingiz ✅ {student}"
            await message.answer(text=text, reply_markup=user_main_menu)
        else:
            text = "Botda nosozlik mavjud"
            await message.answer(text=text)
    else:
        text = "Notog'ri login yoki password kiritdingiz. Qayta urunish uchun /start bosing"
        await message.answer(text=text)
    await state.finish()

@dp.message_handler(text="➕ Mahsulot qo'shish", state="*")
async def add_product_handler(message: types.Message):
    user_products = await get_user_all_products(chat_id=message.chat.id)
    if len(user_products) < 3:
        text = "Iltimos rasmini kiriting"
        await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
        await ProductAddState.photo.set()
    else:
        text = "Siz 3 tadan ko'p mahsulotni bir vaqtda sota olmaysiz. Oldin active mahsulotlardan birini o'chiring."
        await message.answer(text=text)


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


@dp.message_handler(text="🚀 Mars Bozor", state="*")
async def mars_bozor_handler(message: types.Message, state:FSMContext):
    await state.set_state('mars-bozor-state')
    products = await get_all_products()
    if products:
        await state.update_data(index=0)
        product = products[0]
        user = await get_user(chat_id=product[6])
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤{user[1]}\n☎️{user[2]}"
        await message.answer_photo(photo=photo, caption=caption, reply_markup=await mars_bozor_pagination(len(products), 0))
    else:
        text = "Aktiv mahsulotlar mavjud emas"
        await message.answer(text=text, reply_markup=user_main_menu)


@dp.callback_query_handler(text="next_product", state="mars-bozor-state")
async def next_product_handler(call: types.CallbackQuery, state:FSMContext):
    products = await get_all_products()
    data = await state.get_data()
    index = data.get('index')

    product = await next_product(products, index)
    if product:
        user = await get_user(chat_id=product[6])
        await call.message.delete()
        index = index + 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤{user[1]}\n☎️{user[2]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan keyin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(text="previous_product", state="mars-bozor-state")
async def previous_product_handler(call: types.CallbackQuery, state: FSMContext):
    products = await get_all_products()
    data = await state.get_data()
    index = data.get('index')

    product = await previous_product(products, index)
    if product:
        user = await get_user(chat_id=product[6])
        await call.message.delete()
        index = index - 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤{user[1]}\n☎️{user[2]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                        reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan oldin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


@dp.message_handler(text="👤 Profil", state="*")
async def profile_handler(message: types.Message):
    user = await get_user(chat_id=message.chat.id)
    if user:
        text = f"""
👤: {user[1]}
☎️: {user[2]}
*️⃣: {user[3]}
🔑: {user[4]}
        """
        await message.answer(text=text)
    else:
        text = "Iltimos telefon raqamingizni kiriting"
        await message.answer(text=text, reply_markup=phone_share)
        await RegisterState.phone_number.set()


@dp.message_handler(text="🖱 Mahsulotlarim", state="*")
async def mars_bozor_handler(message: types.Message, state:FSMContext):
    await state.set_state('my-products-state')
    products = await get_user_all_products(chat_id=message.chat.id)
    if products:
        user = await get_user(chat_id=message.chat.id)
        await state.update_data(index=0)
        product = products[0]
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤{user[1]}\n☎️{user[2]}"
        await message.answer_photo(photo=photo, caption=caption, reply_markup=await mars_bozor_pagination(len(products), 0))
    else:
        text = "Aktiv mahsulotlar mavjud emas"
        await message.answer(text=text, reply_markup=user_main_menu)


@dp.callback_query_handler(text="next_product", state="my-products-state")
async def next_product_handler(call: types.CallbackQuery, state:FSMContext):
    products = await get_user_all_products(chat_id=call.message.chat.id)
    data = await state.get_data()
    index = data.get('index')

    product = await next_product(products, index)
    if product:
        user = await get_user(chat_id=call.message.chat.id)
        await call.message.delete()
        index = index + 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤{user[1]}\n☎️{user[2]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                   reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan keyin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


@dp.callback_query_handler(text="previous_product", state="my-products-state")
async def previous_product_handler(call: types.CallbackQuery, state: FSMContext):
    products = await get_user_all_products(chat_id=call.message.chat.id)
    data = await state.get_data()
    index = data.get('index')

    product = await previous_product(products, index)
    if product:
        user = await get_user(chat_id=call.message.chat.id)
        await call.message.delete()
        index = index - 1
        photo = product[3]
        caption = f"{product[1]} - {product[4]}\n\n{product[2]}\n\n👤{user[1]}\n☎️{user[2]}"
        await call.message.answer_photo(photo=photo, caption=caption,
                                        reply_markup=await mars_bozor_pagination(len(products), index))
        await state.update_data(index=index)
    else:
        text = "Bundan oldin mahsulot mavjud emas !"
        await call.answer(text=text, show_alert=True)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
