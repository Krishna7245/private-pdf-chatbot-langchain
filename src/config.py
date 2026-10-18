import logging
from pathlib import Path

LOG_DIR = Path("logs")             #the directory and file where logs will be stored
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR/"chatbot.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()             #displays logs in the terminal
    ]
)










