from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Telegram
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    TELEGRAM_API_ID = os.getenv("TELEGRAM_API_ID")
    TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH")
    TARGET_CHANNELS = os.getenv("TARGET_CHANNELS", "").split(",")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///qa_bot.db")
    
    # Vector Store
    VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./vector_store")
    
    # Message collection
    MESSAGE_HISTORY_DAYS = int(os.getenv("MESSAGE_HISTORY_DAYS", "30"))
    
    # Query limits
    MAX_QUERIES_PER_DAY = int(os.getenv("MAX_QUERIES_PER_DAY", "5"))
    
    # Telegram User Session
    SESSION_STRING = os.getenv("SESSION_STRING")