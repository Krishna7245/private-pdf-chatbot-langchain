from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logger = logging.getLogger(__name__)

def chunk_documents(documents):
    logger.info("started document chunking")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 120,
        add_start_index = True    #records each chunk's starting character position in its metadata
    )

    chunks = splitter.split_documents(documents)
   
    logger.info("Total chunks created: %d", len(chunks))
    logger.info("document chunking completed. Total chunks created: %d", len(chunks))
    return chunks

