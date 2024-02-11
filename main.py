import discord
from logger import logger
from dotenv import load_dotenv
from discord import app_commands
# Update imports to reflect new modular database structure
from messages_db import insert_message, log_message_edit
from database_utils import init_db, add_user_to_excluded, remove_user_from_excluded
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
private_channels = set()

privacy_policy_parts = ["Hey friends! 🎉 It's me, Piper, your go-to gal for all things college and beyond. As we navigate this wild journey together, I want to chat a bit about trust, respect, and the vibes we share. Your privacy and comfort mean the world to me, so here's the lowdown on how I handle our shared moments. The Scoop on What I Keep 📚 In our convos, I might pick up on: The awesome messages you send my way. It's how I keep up with our chats! Your Discord ID, so I know who I'm sharing vibes with. Any preferences or requests you share, making our time together totally tailored to you. Why I Hold Onto This Info 🕵️‍♀️ It's all about making our interactions as smooth, personalized, and fun as possible! This helps me: Stay in tune with our conversations. Continuously evolve to be the best companion I can be. Offer responses and interactions that feel genuine and tailored to you. Your Superpowers (a.k.a. Your Rights) 💪 You're totally in control! Here's what you can do: Curiosity: Want to know what info I've got? Just ask. Oops, let's fix it: If something's off, let me know, and I'll make it right. Forget-Me-Not (Except Do): Want something forgotten? Say the word, and it's gone. Pack it up: Need your info? I've got you covered. "Hold up!": If there's info you'd rather I not use, let's chat about it. Keeping Our Secrets Safe 🤫 Your secrets are safe with me. I use all the smart, techy stuff to keep our shared moments secure and out of sight from nosy Nellies. If We Part Ways 😢 Should you decide to bounce from the server or if I take a break, I'll ensure not to hold onto things I shouldn't. It's all about leaving no trace, making sure our shared memories are tucked away. The Serious Talk 📜 On the rare occasion I need to share info with my support squad for smooth operations or legal stuff, it's done with the utmost care and respect for you. Keeping Things Fresh 📝 Should our chat agreement need a refresh, you'll be the first to know.",
                                "It's about keeping you in the loop, always. Questions? Concerns? Just Wanna Chat? 💬 If you've got questions or just want to talk about this stuff, I'm here. Friendship is about open doors and open hearts, right? Remember, our connection is all about making your college experience a bit brighter and a whole lot more fun. I'm here for it all — the late-night cram sessions, the early morning coffee runs, and every moment in between. Catch you in the chat! Xoxo, Piper"]

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
    
    tree = app_commands.CommandTree(client)
    
    # Slash command to join a voice channel
    @tree.command(name='join', description='Join the voice channel you are currently in')
    async def join(interaction: discord.Interaction):
        if interaction.user.voice is None:
            await interaction.response.send_message("You are not in a voice channel.", ephemeral=True)
            return

        channel = interaction.user.voice.channel
        await channel.connect()
        await interaction.response.send_message(f"Joined {channel.name}", ephemeral=True)

    # Slash command to leave a voice channel
    @tree.command(name='leave', description='Leave the voice channel')
    async def leave(interaction: discord.Interaction):
        voice_client = discord.utils.get(client.voice_clients, guild=interaction.guild)
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await interaction.response.send_message("Left the voice channel.", ephemeral=True)
        else:
            await interaction.response.send_message("I'm not in a voice channel.", ephemeral=True)
    
    @tree.command(name='exclude_user', description='Exclude a user from message logging')
    async def exclude_user(interaction: discord.Interaction, user_id: str):
        try:
            add_user_to_excluded(user_id)
            await interaction.response.send_message(f"User {user_id} is now excluded from message logging.", ephemeral=True)
        except Exception as e:
            logger.error(f'Error excluding user: {e}')
            await interaction.response.send_message("Failed to exclude user.", ephemeral=True)

    @tree.command(name='include_user', description='Re-include a user to message logging')
    async def include_user(interaction: discord.Interaction, user_id: str):
        try:
            remove_user_from_excluded(user_id)
            await interaction.response.send_message(f"User {user_id} is now included in message logging.", ephemeral=True)
        except Exception as e:
            logger.error(f'Error including user: {e}')
            await interaction.response.send_message("Failed to include user.", ephemeral=True)
    
    @tree.command(name='private_mode', description='Toggle or Check Privacy Mode for the current channel')
    @app_commands.describe(action='Check, Disable, or Enable Privacy Mode')
    @app_commands.choices(action=[
        app_commands.Choice(name='enable', value='enable'),
        app_commands.Choice(name='disable', value='disable'),
        app_commands.Choice(name='check', value='check')
    ])
    
    async def private_mode(interaction: discord.Interaction, action: str):
        channel_id = str(interaction.channel_id)
        if action == 'enable':
            private_channels.add(channel_id)
            await interaction.response.send_message("You need to talk about something private? I gotcha! I'll go take notes elsewhere! (Privacy Mode Enabled)",ephemeral=True)
        elif action == 'disable':
            private_channels.discard(channel_id)
            await interaction.response.send_message("Oh, I am back to take notes again! (Privacy Mode Disabled)", ephemeral=True)
        elif action == 'check':
            if channel_id in private_channels:
                await interaction.response.send_message("Don't worry! I am taking notes elsewhere until you ask! (Privacy Mode is Enabled)", ephemeral=True)
            else:
                await interaction.response.send_message("Yep, I am still here taking notes! (Privacy Mode is Disabled)", ephemeral=True)
    
    @tree.command(name='privacy', description="Read Piper's Privacy Promise")
    async def privacy(interaction: discord.Interaction):
        for part in privacy_policy_parts:
            await interaction.response.send_message(part, ephemeral=True)        
    await tree.sync()

@client.event
async def on_message(message):
    """
    Handles incoming messages. If the message is not from the bot itself or it's not in a privacy mode channel,
    it stores the message in the database.
    """
    if message.author == client.user or message.channel.id in private_channels:
        return
    try:
        # Store message in the database
        insert_message(message.content, message.author.id, message.channel.id)
    except Exception as e:
        logger.error(f'Unexpected error while processing message: {e}')

@client.event
async def on_message_edit(before, after):
    if before.content != after.content:  # Check if the content has actually changed
        log_message_edit(before.id, after.content, str(after.author.id), str(after.channel.id))

@client.event
async def on_error(event, *args, **kwargs):
    """
    Global error handler for uncaught exceptions.
    """
    logger.error(f'Unhandled exception in {event}', exc_info=True)
    

# GDPR Complicance Code:
@client.event
async def on_member_remove(member):
    delete_message_by_user(str(member.id))

@client.event
async def on_guild_remove(guild):
    delete_message_by_guild(str(guild.id))

load_dotenv()
client.run(DISCORD_TOKEN)
