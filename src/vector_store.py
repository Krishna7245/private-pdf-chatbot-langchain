from src.embedding_model import get_embedding_model
from langchain_chroma import Chroma
import logging

logger = logging.getLogger(__name__)

def create_vector_store(chunks):

    try:
        embedding_model = get_embedding_model()

        vector_store = Chroma.from_documents(
            documents = chunks,
            embedding= embedding_model,
            persist_directory= "chroma_db",              #saves the database locally
            collection_name= "pdf_documents"
        )

        logger.info("Vector store created successfully")
        return vector_store
    
    except Exception:
        logger.exception("failed to create vector store")
        raise

