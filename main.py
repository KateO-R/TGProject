import asyncio
import requests
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from googletrans import Translator
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
import random
from gtts import gTTS
import os

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

router = Router()

translator = Translator()

class TranslateState(StatesGroup):
    waiting_for_message = State()

@router.message(Command('photo'))
async def react_photo(message: Message):
    list = ['https://i.pinimg.com/originals/e2/16/80/e2168035565a9ebc9c1b3efd192d3776.jpg', 'https://i.pinimg.com/736x/86/ea/fb/86eafbfa7d658123b6699c35f84bd6c4.jpg', 'https://i.pinimg.com/564x/45/82/a3/4582a33b57f05e1506a3a0ce11d716d4.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='This is cool picture for you!')

@router.message(F.photo)
async def react_photo(message: Message):
    list = ['Nice picture!', 'I have never seen it before!', 'Wow!That`s cool']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')


@router.message(Command('weather'))
async def show_weather(message: Message):
    api_key = "bfb2bef52e1935d5ff2a3156c9fc3402"
    city = "Leukerbad"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            weather_report = (
                    f"Weather in {city}:\n"
                    f"Description: {weather_description}\n"
                    f"Temperature: {temperature}°C\n"
                    f"Wind Speed: {wind_speed} m/s"
            )
        else:
            weather_report = "Sorry, I couldn't fetch the weather data at the moment."

    except Exception as e:
        weather_report = f"An error occurred: {e}"

    await message.answer(weather_report)

@router.message(Command('help'))
async def help(message: Message):
    await message.answer('This bot can: \n /start \n /help \n /weather \n /photo')

@router.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video_cat.mp4')
    await bot.send_video(message.chat.id, video)

@router.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('sound.mp3')
    await bot.send_audio(message.chat.id, audio)

@router.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('sample3.ogg')
    await message.answer_voice(voice)

@router.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile("TG02.pdf")
    await bot.send_document(message.chat.id, doc)
@router.message(Command('train'))
async def train(message: Message):
    training_list = [
        "Workout 1:\\n1. Crunches: 3 sets of 15 repetitions\\n2. Bicycle: 3 sets of 20 repetitions (each side)\\n3. Plank: 3 sets of 30 seconds",
        "Workout 2:\\n1. Leg Raises: 3 sets of 15 repetitions\\n2. Russian Twist: 3 sets of 20 repetitions (each side)\\n3. Plank with Raised Leg: 3 sets of 20 seconds (each leg)",
        "Workout 3:\\n1. Crunches with Raised Legs: 3 sets of 15 repetitions\\n2. Horizontal Scissors: 3 sets of 20 repetitions\\n3. Side Plank: 3 sets of 20 seconds (each side)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f'This is your mini work-out for today {rand_tr}')
    tts = gTTS(text=rand_tr, lang='en')
    tts.save('training.mp3')
    audio = FSInputFile('training.mp3')
    await bot.send_audio(message.chat.id, audio)
    os.remove('training.mp3')

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Hi! {message.from_user.full_name}')

# Обработчик команды /translate
@router.message(Command('translate'))
async def start_translation(message: Message, state: FSMContext):
    await message.reply("Write me a message for translation.")
    await state.set_state(TranslateState.waiting_for_message)

# Обработчик состояния перевода
@router.message(TranslateState.waiting_for_message)
async def translate_to_english(message: Message, state: FSMContext):
    # Перевод текста на английский
    translated = translator.translate(message.text, dest='en')
    # Отправка переведенного текста обратно пользователю
    await message.reply(translated.text)
    # Завершение состояния
    await state.clear()

# Обработчик для всех остальных сообщений (эхо)
@router.message()
async def echo(message: Message):
    await message.send_copy(chat_id=message.chat.id)

# Основная функция запуск
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())
