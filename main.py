import json
import settings
import discord
from discord.ext import commands

# tut stuff
from colorama import Back, Fore, Style
import time

# intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
        self.cogslist = [
            "cogs.moderation",
            "cogs.vip"
        ]
    
    async def setup_hook(self):
        for ext in self.cogslist:
            await self.load_extension(ext)

    async def on_ready(self):
        prfx = (Back.BLACK + Fore.LIGHTMAGENTA_EX + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.CYAN + Style.NORMAL)
        print(f"{prfx} Logged in as {Fore.RED + bot.user.name}{Fore.RESET}")
        print(f"{prfx} Member id: {Fore.RED + settings.MEMBERS_ID}{Fore.RESET}")
        print(f"{prfx} {Fore.RED + bot.user.name}{Fore.CYAN} Online!{Fore.RESET}")

with open('config.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['DISCORD_TOKEN']

bot = Bot()

bot.run(TOKEN)