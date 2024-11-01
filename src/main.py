import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .config import Config
from .database.database import init_db
from .bot.handlers import router
from .bot.middlewares import QueryLimitMiddleware, DatabaseMiddleware
from .utils.scheduler import setup_scheduler
from .services.telegram_collector import TelegramCollector
from .database.database import get_session

async def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize database
    await init_db()
    
    # Initialize bot and dispatcher
    bot = Bot(token=Config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register middlewares
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(QueryLimitMiddleware())
    
    # Register router
    dp.include_router(router)
    
    # Setup scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    
    # Start message collection in background
    async def start_collector():
        async for session in get_session():
            collector = TelegramCollector(session)
            await collector.collect_messages()
    
    asyncio.create_task(start_collector())
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main()) 