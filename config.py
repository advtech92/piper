from dotenv import load_dotenv
import os

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
LIFX_TOKEN = os.getenv('LIFX_TOKEN')
WYZE_ACCESS_TOKEN = os.getenv('WYZE_ACCESS_TOKEN')
WYZE_EMAIL = os.getenv('WYZE_EMAIL')
WYZE_PASSWORD = os.getenv('WYZE_PASSWORD')
WYZE_KEY_ID = os.getenv('WYZE_KEY_ID')
WYZE_API_KEY = os.getenv('WYZE_API_KEY')
PV_ACCESSKEY = os.getenv('PICOVOICE_ACCESS_TOKEN')