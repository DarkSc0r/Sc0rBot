import discord
from discord.ext import commands
from datetime import timedelta
import settings

class logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return

        log_channel = message.guild.get_channel(settings.LOG_CHANNEL_ID)

        if log_channel is None:
            return

        deleter = None
        now = discord.utils.utcnow()

        after = now - timedelta(seconds=5)

        async for entry in message.guild.audit_logs(
            limit=3, 
            action=discord.AuditLogAction.message_delete,
            after=after
        ):
            if entry.target.id == message.author.id:
                deleter = entry.user
                break

        if deleter is None:
            deleter = "Unknown"

        embed = discord.Embed(
            title="Audit Logger",
            description="Message Deleted",
            color=discord.Color.from_rgb(255, 24, 44),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=message.author.avatar)

        embed.add_field(name="Message: ", value=message.content or "No Content Found", inline=False)

        embed.add_field(name="User: ", value=message.author)
        embed.add_field(name="Channel: ", value=message.channel)

        embed.add_field(name="Deleted By: ", value=deleter, inline=False)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        elif after.author.bot:
            return

        log_channel = before.guild.get_channel(settings.LOG_CHANNEL_ID)

        if log_channel is None:
            return

        editor = before.author

        if editor is None:
            editor = "Unknown"

        embed = discord.Embed(
            title="Audit Logger",
            description="Message Edited",
            color=discord.Color.from_rgb(208, 109, 3),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=before.author.avatar)

        embed.add_field(name="Before: ", value=before.content or "No Content Found")
        embed.add_field(name="After: ", value=after.content)

        embed.add_field(name="User: ", value=before.author, inline=False)
        embed.add_field(name="Channel: ", value=before.channel, inline=False)

        embed.add_field(name="Edited By: ", value=editor, inline=False)

        await log_channel.send(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(logger(bot))