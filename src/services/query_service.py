from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from .vector_store import VectorStore
from ..config import Config

class QueryService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.vector_store.as_retriever(),
            memory=self.memory
        )
    
    async def get_answer(self, question: str) -> str:
        result = await self.qa_chain.ainvoke({"question": question})
        return result["answer"] 