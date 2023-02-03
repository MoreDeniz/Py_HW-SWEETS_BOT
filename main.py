
from aiogram import Bot, Dispatcher, executor, types
from handlers import dp
import emoji

total = 150

async def on_start(_):
    print('Бот запущен')
    print(emoji.emojize(':thumbs_up: :red_heart: :yellow_heart:'))

executor.start_polling(dp, skip_updates=True, on_startup=on_start)