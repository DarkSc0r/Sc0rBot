import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild

        if guild is None:
            await ctx.send("This command can only be used inside the server.")
            return
    
        