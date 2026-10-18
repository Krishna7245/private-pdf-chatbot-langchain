import logging

logger = logging.getLogger(__name__)

def create_retriever(vector_store):

    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k": 5}            #retrieve the five most similar chunks.
    )
    logger.info("Retriever configured successfully")
    return retriever

