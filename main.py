import os
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F
from dotenv import load_dotenv

from src.telegram import router

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = Bot(token=API_TOKEN)  # Создание экземпляра бота
dp = Dispatcher()


async def main():
    """
    Основная функция для запуска бота.
    """
    print("Starting telegram bot")
    dp.include_routers(router)  # Подключаем маршрутизатор
    await polling()  # Запускаем цикл опроса


async def polling():
    """
    Функция для опроса обновлений от Telegram.
    """
    while True:
        await dp.start_polling(bot, skip_updates=True)  # Запускаем опрос


if __name__ == "__main__":
    asyncio.run(main())  # Запуск основного цикла
