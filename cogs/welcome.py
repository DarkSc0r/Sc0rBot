import discord
from discord.ext import commands

import config

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_welcome_channel(self):
        channel = self.bot.get_channel(config.WELCOME_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(config.WELCOME_CHANNEL_ID)

        return channel
    
    async def get_log_channel(self):
        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(config.LOG_CHANNEL_ID)

        return channel
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = await self.get_welcome_channel()

        embed = discord.Embed(
            title="Welcome!",
            description=f"{member.mention} joined the server.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Member count", value=member.guild.member_count, inline=True)
        embed.add_field(name="Account Created", value=discord.utils.format_dt(member.created_at, style="D"), inline=True)

        await welcome_channel.send(embed=embed)

        log_channel = await self.get_log_channel()

        log_embed = discord.Embed(
            title="Member Joined",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )

        log_embed.add_field(name="User", value=f"{member.mention} {'{member.id}'}", inline=True)
        log_embed.add_field(name="Acount Created", value=discord.utils.format_dt(member.created_at, style="D"), inline=True)
        log_embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)

        await log_channel.send(embed=log_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = await self.get_log_channel()

        embed = discord.Embed(
            title="Member Left",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="User", value=f"{member} ('{member.id}')", inline=True)
        embed.add_field(name="Joined Server", value=discord.utils.format_dt(member.joined, style="D"), inline=True)
        embed.add_field(name="Member Count", value=member.guild.member_count, inline=True)

        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Welcome(bot))