from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from sqlalchemy import update
from ..database.models import User
from ..database.database import AsyncSessionLocal
from ..services.telegram_collector import TelegramCollector
import logging

logger = logging.getLogger(__name__)

async def reset_daily_queries():
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(User).values(
                queries_today=0,
                last_query_reset=datetime.utcnow()
            )
        )
        await session.commit()

async def collect_messages():
    logger.info("Starting message collection...")
    try:
        async with AsyncSessionLocal() as session:
            collector = TelegramCollector(session)
            await collector.collect_messages()
        logger.info("Message collection completed successfully")
    except Exception as e:
        logger.error(f"Error during message collection: {str(e)}")

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    
    # Reset query counts at midnight UTC
    scheduler.add_job(
        reset_daily_queries,
        trigger=CronTrigger(hour=0, minute=0),
        id='reset_daily_queries',
        replace_existing=True
    )
    
    # Collect messages every hour
    scheduler.add_job(
        collect_messages,
        trigger=CronTrigger(minute='*/5'),  # Run every 5 minutes
        id='collect_messages',
        replace_existing=True
    )
    
    return scheduler 