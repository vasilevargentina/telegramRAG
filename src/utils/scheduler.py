from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from sqlalchemy import update
from ..database.models import User
from ..database.database import AsyncSessionLocal

async def reset_daily_queries():
    async with AsyncSessionLocal() as session:
        await session.execute(
            update(User).values(
                queries_today=0,
                last_query_reset=datetime.utcnow()
            )
        )
        await session.commit()

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    
    # Reset query counts at midnight UTC
    scheduler.add_job(
        reset_daily_queries,
        trigger=CronTrigger(hour=0, minute=0),
        id='reset_daily_queries',
        replace_existing=True
    )
    
    return scheduler 