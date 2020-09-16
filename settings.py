import logging

from decouple import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger()

TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
