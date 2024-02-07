import discord
from logger import logger
from dotenv import load_dotenv
from database import insert_message, has_introduced, record_introduction
from config import DISCORD_TOKEN

# Setup our bot Piper!
logger.info("Starting Piper...")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if not has_introduced(str(guild.id)):
            default_channel = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages), None)
            if default_channel:
                await default_channel.send("Hi there! I'm Piper, a bit of a shy observer here to learn from all the wonderful conversations happening. I promise to quietly listen and keep everything between us. I won't chime in for now, just soaking it all in. Thanks for letting me be a part of your space! 📚✨")
                record_introduction(str(guild.id))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    # Store message in the database
    insert_message(message.content, message.author.id, message.channel.id)

load_dotenv()
client.run(DISCORD_TOKEN)
