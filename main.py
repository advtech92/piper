import discord
from logger import logger
from dotenv import load_dotenv
# Update imports to reflect new modular database structure
from messages_db import insert_message
from database_utils import init_db
from guild_introductions_db import has_introduced, record_introduction
from config import DISCORD_TOKEN
from discord.errors import HTTPException, Forbidden

# Setup our bot Piper!
logger.info("Starting Piper...")

# Initialize the database
init_db()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """
    Handles the event when the bot has successfully connected to Discord.
    It checks each guild to send an introduction message if it hasn't already.
    """
    logger.info(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if not has_introduced(str(guild.id)):
            try:
                default_channel = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages), None)
                if default_channel:
                    await default_channel.send("Hi there! I'm Piper, a bit of a shy observer here to learn from all the wonderful conversations happening. I promise to quietly listen and keep everything between us. I won't chime in for now, just soaking it all in. Thanks for letting me be a part of your space! 📚✨")
                    record_introduction(str(guild.id), guild.name)
            except HTTPException as e:
                logger.error(f'HTTPException while sending introduction message: {e}')
            except Forbidden as e:
                logger.error(f'Forbidden: Cannot send introduction message due to lack of permissions: {e}')
            except Exception as e:
                logger.error(f'Unexpected error while sending introduction message: {e}')

@client.event
async def on_message(message):
    """
    Handles incoming messages. If the message is not from the bot itself,
    it stores the message in the database.
    """
    if message.author == client.user:
        return
    try:
        # Store message in the database
        insert_message(message.content, message.author.id, message.channel.id)
    except Exception as e:
        logger.error(f'Unexpected error while processing message: {e}')

@client.event
async def on_error(event, *args, **kwargs):
    """
    Global error handler for uncaught exceptions.
    """
    logger.error(f'Unhandled exception in {event}', exc_info=True)

load_dotenv()
client.run(DISCORD_TOKEN)
