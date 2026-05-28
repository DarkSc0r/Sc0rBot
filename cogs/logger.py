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
            color=discord.Color.from_rgb(208, 109, 3),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(name="Message: ", value=message.content or "No Content Found", inline=False)

        embed.add_field(name="User: ", value=message.author)
        embed.add_field(name="Channel: ", value=message.channel)

        embed.add_field(name="Deleted By: ", value=deleter, inline=False)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.get_channel(settings.WELCOME_CHANNEL_ID)
        rules_channel = member.guild.get_channel(settings.RULES_CHANNEL_ID)
        get_rules_channel = member.guild.get_channel(settings.GET_ROLES_CHANNEL_ID)
        embed = discord.Embed(
            title=f"Welcome!!",
            description=f"Glad you joined the server {member.mention}! " \
             f"PLEASE don't forget to go to the {rules_channel.mention} channel to see our rules in this server!" \
             f"To get access to the ENTIRE(almost) server, please make your way to the {get_rules_channel.mention} channel and fill out all the roles you want!" \
             f"The <@&{settings.MEMBER_ID}> is how you get access!!",
            color=discord.Color.from_rgb(72, 141, 206),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=member.avatar)

        await welcome_channel.send(embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
    
async def setup(bot:commands.Bot):
    await bot.add_cog(logger(bot))