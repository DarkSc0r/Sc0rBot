import discord
from discord.ext import commands

import config


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self):
        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(config.LOG_CHANNEL_ID)

        return channel

    @commands.Cog.listener()
    async def on_audit_log_entry_create(self, entry):
        channel = await self.get_log_channel()

        embed = discord.Embed(
            title="Audit Log Entry",
            color=discord.Color.orange(),
            timestamp=entry.created_at
        )
        embed.add_field(
            name="Action",
            value=str(entry.action).replace("AuditLogAction.", ""),
            inline=False
        )
        embed.add_field(
            name="User",
            value=str(entry.user or f"User ID: {entry.user_id}"),
            inline=True
        )
        embed.add_field(name="Target", value=str(entry.target), inline=True)
        embed.add_field(
            name="Reason",
            value=entry.reason or "No reason provided",
            inline=False
        )

        changes = []

        for name, after_value in entry.after:
            before_value = getattr(entry.before, name, None)
            changes.append(f"`{name}`: `{before_value}` -> `{after_value}`")

        if changes:
            embed.add_field(
                name="Changes",
                value="\n".join(changes[:5])[:1024],
                inline=False
            )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return

        if before.content == after.content:
            return

        log_channel = await self.get_log_channel()

        embed = discord.Embed(
            title="Message Edited",
            color=discord.Color.blue(),
            timestamp=after.edited_at
        )
        embed.add_field(
            name="User",
            value=f"{after.author.mention} (`{after.author.id}`)",
            inline=False
        )
        embed.add_field(name="Channel", value=after.channel.mention, inline=False)
        embed.add_field(name="Before", value=before.content[:1024] or "No text", inline=False)
        embed.add_field(name="After", value=after.content[:1024] or "No text", inline=False)
        embed.add_field(
            name="Jump to Message",
            value=f"[Click here]({after.jump_url})",
            inline=False
        )

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot or message.guild is None:
            return

        log_channel = await self.get_log_channel()

        embed = discord.Embed(
            title="Message Deleted",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(
            name="User",
            value=f"{message.author.mention} (`{message.author.id}`)",
            inline=False
        )
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Message", value=message.content[:1024] or "No text", inline=False)

        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))