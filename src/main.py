import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from .config import Config
from .database.database import init_db
from .bot.handlers import router
from .bot.middlewares import QueryLimitMiddleware, DatabaseMiddleware
from .utils.scheduler import setup_scheduler, collect_messages

async def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
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
    
    # Perform initial message collection
    logger.info("Starting initial message collection...")
    await collect_messages()
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main()) 