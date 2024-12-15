from aiogram import Dispatcher
from huggingface_hub import login
from bot_init import dp, bot, logger
from handlers import router

async def main():
    dp.include_router(router)
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())