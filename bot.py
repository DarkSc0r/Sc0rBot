import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import config

load_dotenv()

class DiscordBot(commands.Bot):
    async def setup_hook(self):
        for cog in config.COGS:
            await self.load_extension(cog)
            print(f"Loaded {cog}")


handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True
intents.voice_states = True

bot = DiscordBot(command_prefix=config.COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

token = os.getenv("DISCORD_TOKEN")

if token is None:
    raise ValueError("DISCORD_TOKEN was not found in your .env file.")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)