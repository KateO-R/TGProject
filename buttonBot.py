import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery

from config import TOKEN1
import keyboards as kb

bot = Bot(token=TOKEN1)
dp = Dispatcher()

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('This bot can: \n /start \n /help \n /links \n /dynamic')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Hi! {message.from_user.full_name}', reply_markup=kb.main)

@dp.message(F.text == 'Hello!')
async def hello_message(message: Message):
    await message.answer(f'Hello, {message.from_user.full_name}!')

@dp.message(F.text == 'Buy!')
async def buy_message(message: Message):
    await message.answer(f'Good buy, {message.from_user.full_name}!')

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer(f'Hi! {message.from_user.full_name}', reply_markup=kb.inline_keyboard_test)

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer('News are downloading', show_alert=True)
    await callback.message.answer('Latest news')


@dp.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer(f'Hi! {message.from_user.full_name}', reply_markup=kb.show_more_keyboard())

@dp.callback_query(F.data == 'show_more')
async def show_more(callback: CallbackQuery):
    await callback.message.edit_text('Choose an option:', reply_markup=kb.options_keyboard())

@dp.callback_query(F.data == 'option_1')
async def option_1(callback: CallbackQuery):
    await callback.message.answer('You selected Option 1!')

@dp.callback_query(F.data == 'option_2')
async def option_2(callback: CallbackQuery):
    await callback.message.answer('You selected Option 2!')


async def main():
    await dp.start_polling(bot)

# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())

