import asyncio
import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN
import random

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def react_photo(message: Message):
    list = ['https://i.pinimg.com/originals/e2/16/80/e2168035565a9ebc9c1b3efd192d3776.jpg', 'https://i.pinimg.com/736x/86/ea/fb/86eafbfa7d658123b6699c35f84bd6c4.jpg', 'https://i.pinimg.com/564x/45/82/a3/4582a33b57f05e1506a3a0ce11d716d4.jpg']
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='This is cool picture for you!')

@dp.message(F.text == 'What is AI?')
async def aitext(message: Message):
    await message.answer('Artificial Intelligence (AI) refers to the development of computer systems and software that can perform tasks typically requiring human intelligence. These tasks include reasoning, learning, problem-solving, perception, language understanding, and decision-making. ')

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Nice picture!', 'I have never seen it before!', 'Wow!That`s cool']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)


@dp.message(Command('weather'))
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

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('This bot can: \n /start \n /help \n /weather \n /photo')
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Hi! I am TG bot!')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
