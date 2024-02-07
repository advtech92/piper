import logging
from logging.handlers import TimedRotatingFileHandler
import requests
import json

# Discord Webhook URL
from dotenv import load_dotenv
from config import WEBHOOK_URL
load_dotenv()

class DiscordLoggingHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({'content': log_entry})
        try:
            response = requests.post(WEBHOOK_URL, headers=headers, data=payload)
            if response.status_code != 204:
                print(f"Error sending log to Discord: {response.status_code}")
        except Exception as e:
            print(f"Failed to send log to Discord: {e}")

def setup_logging():
    # Create a logger
    logger = logging.getLogger('Piper')
    logger.setLevel(logging.INFO)  # Adjust as needed
    
    # File handler for logging to a file
    file_handler = TimedRotatingFileHandler('piper.log', when='midnight', interval=1)
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file_handler)
    
    # Discord handler for logging errors to Discord
    discord_handler = DiscordLoggingHandler()
    discord_handler.setLevel(logging.ERROR)  # Only send errors to Discord
    discord_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(message)s'))
    logger.addHandler(discord_handler)
    
    return logger

# Initialize the logger
logger = setup_logging()
