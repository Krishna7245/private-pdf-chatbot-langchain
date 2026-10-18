from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def ingest_pdf(pdf_path):

    pdf_path = Path(pdf_path)              #Converted the supplied path into a path object on which we can perform checks

    if pdf_path.exists() is False:
        logger.error("PDF not found")
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.is_file() is False:
        logger.error("provided path is not a file")
        raise ValueError("The provided path is not a file.")
    if pdf_path.suffix.lower()!=".pdf":
        logger.error("provided file is not a pdf")
        raise ValueError("The provided file is not a PDF.")

    loader = PyPDFLoader(str(pdf_path))
    documents = loader.load()
    logger.info("pdf ingestion completed. Pages loaded: %d", len(documents))

    return documents


