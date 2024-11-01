from datetime import datetime, timedelta
from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import User
from ..config import Config
from ..database.database import AsyncSessionLocal

class QueryLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if event.text and event.text.startswith('/ask'):
            session: AsyncSession = data['session']
            
            # Get or create user
            result = await session.execute(
                select(User).where(User.telegram_id == event.from_user.id)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                user = User(
                    telegram_id=event.from_user.id,
                    username=event.from_user.username
                )
                session.add(user)
                await session.commit()
            
            # Check if we need to reset daily counter
            if datetime.utcnow() - user.last_query_reset > timedelta(days=1):
                await session.execute(
                    update(User)
                    .where(User.telegram_id == event.from_user.id)
                    .values(queries_today=0, last_query_reset=datetime.utcnow())
                )
                await session.commit()
                user.queries_today = 0
            
            # Check query limit
            if user.queries_today >= Config.MAX_QUERIES_PER_DAY:
                await event.answer(
                    "You've reached your daily query limit. Please try again tomorrow."
                )
                return
            
            # Increment query count
            user.queries_today += 1
            await session.commit()
        
        return await handler(event, data) 

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with AsyncSessionLocal() as session:
            data['session'] = session
            return await handler(event, data) 