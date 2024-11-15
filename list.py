import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3

from config import TOKEN1

bot = Bot(token=TOKEN1)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()
    confirm = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Hello! What is your name?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("How old are you?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("What is your grade?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    confirmation_message = (
        f"Please check the data you put in: your name is {user_data['name']}, "
        f"{user_data['age']} years old, your grade is {user_data['grade']}. "
        "Please type Yes if everything is correct and No if you need to correct your data."
    )
    await message.answer(confirmation_message)
    await state.set_state(Form.confirm)

@dp.message(Form.confirm)
async def confirm(message: Message, state: FSMContext):
    if message.text.lower() == 'yes':
        user_data = await state.get_data()

        conn = sqlite3.connect('school_data.db')
        cur = conn.cursor()
        cur.execute('''
        INSERT INTO users (name, age, grade) VALUES(?, ?, ?)''',
                    (user_data['name'], user_data['age'], user_data['grade']))
        conn.commit()
        conn.close()

        await message.answer("Thank you, you are now in the school data list.")
        await state.clear()
    elif message.text.lower() == 'no':
        await message.answer("Please try again. Press /start to begin.")
        await state.clear()
    else:
        await message.answer("Please type Yes or No.")

async def main():
    await dp.start_polling(bot)

# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())