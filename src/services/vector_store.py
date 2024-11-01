from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from ..config import Config

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_store = Chroma(
            persist_directory=Config.VECTOR_STORE_PATH,
            embedding_function=self.embeddings
        )
    
    async def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        return await self.vector_store.aadd_texts(texts=texts, metadatas=metadatas)
    
    async def similarity_search(self, query: str, k: int = 4):
        return await self.vector_store.asimilarity_search(query, k=k) 