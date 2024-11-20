import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests

from config import TOKEN1, THE_CAT_API_KEY

bot = Bot(token=TOKEN1)
dp = Dispatcher()

def get_cat_breeds():
   url = "https://api.thecatapi.com/v1/breeds"
   headers = {"x-api-key": THE_CAT_API_KEY}
   response = requests.get(url, headers=headers)
   return response.json()

def get_cat_image_by_breed(breed_id):
   url = f'https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}'
   headers = {"x-api-key": THE_CAT_API_KEY}
   response = requests.get(url, headers=headers)
   data = response.json()
   return data[0]['url']

def get_breed_info(breed_name):
   breeds = get_cat_breeds()
   for breed in breeds:
       if breed['name'].lower() == breed_name.lower():
           return breed
   return None

@dp.message(CommandStart())
async def start(message: Message):
   await message.answer('Hi! Write me the name of the cat`s breed and i will send you its picture and some info about')

@dp.message()
async def send_cat_info(message: Message):
   breed_name = message.text
   breed_info = get_breed_info(breed_name)
   if breed_info:
      cat_image_url = get_cat_image_by_breed(breed_info['id'])
      info = (
         f"Breed - {breed_info['name']}\n"
         f"Description - {breed_info['description']}\n"
         f"Lifespan - {breed_info['life_span']} years"
      )
      await message.answer_photo(photo=cat_image_url, caption=info)
   else:
      await message.answer("Breed not found. Try again.")


async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())