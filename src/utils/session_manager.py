from telethon import TelegramClient
from telethon.sessions import StringSession
from ..config import Config
import logging

logger = logging.getLogger(__name__)

# не выполняется
async def create_user_session():
    """Create a user session for the first time"""
    client = TelegramClient(StringSession(), Config.TELEGRAM_API_ID, Config.TELEGRAM_API_HASH)
    await client.start()
    
    # Save the session string
    session_string = client.session.save()
    logger.info(f"Your session string is: {session_string}")
    await client.disconnect()
    return session_string

async def get_client():
    """Get a client using existing session string"""
    if not Config.SESSION_STRING:
        raise ValueError("SESSION_STRING environment variable is not set")
    
    client = TelegramClient(
        StringSession(Config.SESSION_STRING),
        Config.TELEGRAM_API_ID,
        Config.TELEGRAM_API_HASH
    )
    return client 