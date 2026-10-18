from langchain_huggingface import HuggingFaceEmbeddings
import logging

logger= logging.getLogger(__name__)

def get_embedding_model():
    try:
        model = HuggingFaceEmbeddings(
            model_name= "sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs = {"device": "cpu"},
            encode_kwargs = {"normalize_embeddings": True}          #normalize vectors to unit length for similarity comparisons
        )
        logger.info("embedding model initialised successfully")
        return model
    except Exception:
        logger.exception("Failed to initialise embedding model")
        raise
  




