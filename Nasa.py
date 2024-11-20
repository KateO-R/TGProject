# This bot is to get random photos from Front Hazard Avoidance Camera of Mars rover
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from datetime import datetime, timedelta

from config import TOKEN1, NASA_API_KEY

bot = Bot(token=TOKEN1)
dp = Dispatcher()

def fetch_random_mars_photo():
   url = f'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&camera=fhaz&api_key={NASA_API_KEY}'
   response = requests.get(url)
   data = response.json()
   photos = data['photos']
   if not photos:
      return None  # Возвращаем None, если список фото пуст
   random_photo = random.choice(photos)
   return random_photo

@dp.message(Command('random_mars'))
async def send_random_mars_photo(message: Message):
   photo= fetch_random_mars_photo()
   if photo is None:
      await message.answer("No photos for today")
      return

   photo_url = photo['img_src']
   rover_name = photo['rover']['name']
   camera_name = photo['camera']['full_name']
   date_taken = photo['earth_date']

   caption = f"Rover: {rover_name}\n Camera: {camera_name}\n Date: {date_taken}"
   await message.answer_photo(photo=photo_url, caption=caption)

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())