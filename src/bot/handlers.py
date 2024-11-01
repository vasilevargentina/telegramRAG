from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.query_service import QueryService
from ..database.models import User
from sqlalchemy import select, update
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.models import User
from ..config import Config
from ..services.vector_store import VectorStore
from sqlalchemy import func

router = Router()
query_service = QueryService()

@router.message(Command("start"))
async def start_handler(message: Message, session: AsyncSession):
    await message.answer(
        "👋 Welcome to the Q&A Bot!\n\n"
        "I can answer questions based on the content from specified Telegram channels.\n"
        "Use /ask followed by your question to get started.\n\n"
        f"You have {5} queries available today."
    )

@router.message(Command("ask"))
async def ask_handler(message: Message, session: AsyncSession):
    question = message.text.replace("/ask", "").strip()
    if not question:
        await message.answer(
            "Please provide your question after /ask command.\n"
            "Example: /ask What are the latest updates?"
        )
        return
    
    try:
        answer = await query_service.get_answer(question)
        await message.answer(answer)
    except Exception as e:
        await message.answer(
            "Sorry, I encountered an error while processing your question. "
            "Please try again later."
        )

@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(
        "🤖 Bot Commands:\n\n"
        "/start - Start the bot\n"
        "/ask [question] - Ask a question\n"
        "/help - Show this help message\n"
        "/status - Check your daily query limit\n"
        "/vectorinfo - Check vector store status\n\n"
        "Example: /ask What are the latest updates?"
    )

@router.message(Command("status"))
async def status_handler(message: Message, session: AsyncSession):
    result = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()
    
    if user:
        queries_left = Config.MAX_QUERIES_PER_DAY - user.queries_today
        await message.answer(
            f"You have {queries_left} queries remaining today.\n"
            "The limit resets daily."
        )
    else:
        await message.answer(
            f"You have {Config.MAX_QUERIES_PER_DAY} queries available today."
        ) 

@router.message(Command("vectorinfo"))
async def vectorinfo_handler(message: Message, session: AsyncSession):
    try:
        # Get vector store stats
        vector_store = VectorStore()
        vector_info = await vector_store.get_collection_info()
        
        # Get database message count
        result = await session.execute(select(func.count(Message.id)))
        db_count = result.scalar()
        
        # Format response
        await message.answer(
            "📊 Vector Store Status:\n\n"
            f"Documents in vector store: {vector_info['total_documents']}\n"
            f"Messages in database: {db_count}\n"
            f"Collection name: {vector_info['collection_name']}"
        )
    except Exception as e:
        await message.answer(
            "Sorry, couldn't retrieve vector store information."
        ) 