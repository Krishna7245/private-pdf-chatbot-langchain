from src.ingestion import ingest_pdf
from src.chunking import chunk_documents
from src.vector_store import create_vector_store
from src.retrieval import create_retriever
from src.chain import create_rag_chain
import shutil
from pathlib import Path
import src.config
import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting pdf chatbot")

    pdf_path = input("Enter your PDF's Path: ").strip()

    try:
        documents = ingest_pdf(pdf_path)
    except (FileNotFoundError, ValueError, PermissionError):
        logger.exception("PDF ingestion failed")
        print("Could not load the PDF. Check the path and file permissions.")
        return

    logger.info("PDF ingestion completed: %d pages loaded", len(documents))

    try:
        chunks = chunk_documents(documents)
        logger.info("Document chunking completed: %d chunks created", len(chunks))

        if not chunks:
            raise ValueError("No text chunks were created from the PDF.")

        vector_store = create_vector_store(chunks)
        logger.info("Vector store created")

    except Exception:
        logger.exception("Document processing or vector-store creation failed")
        print("Failed to process the PDF. Check logs/chatbot.log for details.")
        return

    try:
        retriever = create_retriever(vector_store)
        logger.info("Retriever initialized")

        rag_chain = create_rag_chain(retriever)
        logger.info("RAG chain initialized")

    except Exception:
        logger.exception("Failed to initialize retriever or RAG chain")
        print("Failed to initialize the chatbot. Check logs/chatbot.log for details.")
        return

    while True:
        print("\n 1. Ask a question.")
        print("2. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            logger.info("User selected Ask a question")

            question = input("Ask a question: ").strip()
            logger.info("Processing question: %s", question)

            if not question:
                logger.warning("empty ques submitted")
                print("Question can't be empty.")
                continue
            try:
                answer = rag_chain.invoke(question)
                logger.info("answer generated successfully")
                print(f"Answer: {answer}")
            except Exception:
                logger.exception("failed to generate an answer")
                print("Something went wrong...")

        elif choice=="2":
            logger.info("User choose to turn off chatbot")
            db_path = Path("chroma_db")
            if db_path.exists():
                shutil.rmtree(db_path)
                logger.info("chroma database directory deleted")

            print("Closing the chatbot...")
            break

        else:
            logger.warning("Invalid menu choice entered")
            print("Invalid choice...Choose b/w 1 and 2")

if __name__ == "__main__":
    main()



