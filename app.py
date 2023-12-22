from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from default_keyboards import user_main_menu
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN, proxy="http://proxy.server:3128")
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def start_handler(message: types.Message):
    text = "Botimizga xush kelibsiz."
    await message.answer(text=text, reply_markup=user_main_menu)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
