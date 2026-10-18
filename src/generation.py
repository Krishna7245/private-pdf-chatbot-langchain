from dotenv import load_dotenv
from langchain_groq import ChatGroq
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def get_chat_model():
    logger.info("Initialising the chat model")
    try:
        model = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature= 0 
        )
        logger.info("model initialised successfully ")
        return model

    except Exception:
        logger.exception("failed to initialise model")
        raise

        