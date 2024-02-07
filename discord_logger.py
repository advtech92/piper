import logging
import json
import requests
from logging.handlers import TimedRotatingFileHandler
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
    # Attach to the root logger to capture logs from all libraries
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)  # Capture all errors
    
    # Format for the messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Discord handler
    discord_handler = DiscordLoggingHandler()
    discord_handler.setLevel(logging.ERROR)
    discord_handler.setFormatter(formatter)
    logger.addHandler(discord_handler)
    
    # File handler (optional)
    file_handler = TimedRotatingFileHandler('bot_errors.log', when='midnight', interval=1)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

setup_logging()
