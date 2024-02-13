from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
LIFX_TOKEN = os.getenv('LIFX_TOKEN')