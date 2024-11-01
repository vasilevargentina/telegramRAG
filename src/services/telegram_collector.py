from telethon import TelegramClient
from datetime import datetime, timedelta
from ..config import Config
from .vector_store import VectorStore
from ..database.models import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class TelegramCollector:
    def __init__(self, session: AsyncSession):
        self.client = TelegramClient(
            'qa_bot',
            Config.TELEGRAM_API_ID,
            Config.TELEGRAM_API_HASH
        )
        self.vector_store = VectorStore()
        self.session = session
    
    async def collect_messages(self):
        await self.client.start()
        
        for channel in Config.TARGET_CHANNELS:
            channel_entity = await self.client.get_entity(channel)
            messages = await self.client.get_messages(
                channel_entity,
                limit=None,
                offset_date=datetime.now() - timedelta(days=Config.MESSAGE_HISTORY_DAYS)
            )
            
            # Filter out messages that are already in the database
            existing_messages = await self.session.execute(
                select(Message.message_id).where(Message.channel_id == channel_entity.id)
            )
            existing_ids = {msg[0] for msg in existing_messages}
            
            new_messages = [msg for msg in messages if msg.id not in existing_ids]
            
            # Add to vector store and database
            texts = [msg.text for msg in new_messages if msg.text]
            metadatas = [{"channel_id": channel_entity.id, "message_id": msg.id} 
                        for msg in new_messages if msg.text]
            
            if texts:
                await self.vector_store.add_texts(texts, metadatas)
                
                for msg in new_messages:
                    if msg.text:
                        db_message = Message(
                            channel_id=channel_entity.id,
                            message_id=msg.id,
                            content=msg.text
                        )
                        self.session.add(db_message)
                
                await self.session.commit()
        
        await self.client.disconnect() 