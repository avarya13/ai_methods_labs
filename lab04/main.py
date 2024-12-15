from bot_init import dp, bot, logger
from handlers import router

async def main() -> None:
    """
    Основная функция для запуска бота.
    
    Включает маршрутизатор и запускает процесс опроса бота.
    """
    dp.include_router(router)
    logger.info("Бот запущен")
    await dp.start_polling(bot)


# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())