import re
import time

import discord
from discord.ext import commands

import config


INVITE_PATTERN = re.compile(
    r"(discord\.gg/|discord\.com/invite/|discordapp\.com/invite/)",
    re.IGNORECASE
)

URL_PATTERN = re.compile(
    r"(https?://|www\.|[a-z0-9-]+\.(com|net|org|gg|io|co|me|dev|app|xyz|tv|site|online|store|info|biz)(/|\b))",
    re.IGNORECASE
)


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.recent_messages = {}
        self.violations = {}

    async def get_log_channel(self):
        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(config.LOG_CHANNEL_ID)

        return channel

    def is_staff(self, member):
        if member.guild_permissions.manage_messages:
            return True

        return any(role.id == config.STAFF_ROLE_ID for role in member.roles)

    def has_excessive_caps(self, content):
        letters = [char for char in content if char.isalpha()]

        if len(letters) < config.AUTOMOD_CAPS_MIN_LETTERS:
            return False

        uppercase = [char for char in letters if char.isupper()]
        return len(uppercase) / len(letters) >= config.AUTOMOD_CAPS_PERCENT

    def has_blocked_word(self, content):
        lowered = content.lower()

        for word in config.BLOCKED_WORDS:
            if word.lower() in lowered:
                return word

        return None

    def is_spam(self, message):
        now = time.time()
        user_messages = self.recent_messages.setdefault(message.author.id, [])

        user_messages.append((now, message.content))
        cutoff = now - config.AUTOMOD_SPAM_SECONDS
        self.recent_messages[message.author.id] = [
            item for item in user_messages if item[0] >= cutoff
        ]

        recent = self.recent_messages[message.author.id]

        if len(recent) >= config.AUTOMOD_SPAM_MESSAGE_LIMIT:
            return True

        repeated = [item for item in recent if item[1] == message.content]
        return len(repeated) >= config.AUTOMOD_REPEAT_MESSAGE_LIMIT

    async def punish_message(self, message, reason):
        try:
            await message.delete()
        except discord.Forbidden:
            await message.channel.send(
                "I need **Manage Messages** to delete automod messages.",
                delete_after=8
            )
            return

        self.violations[message.author.id] = self.violations.get(message.author.id, 0) + 1

        await message.channel.send(
            f"\u26A0\uFE0F {message.author.mention}, your message was removed: **{reason}**",
            delete_after=8
        )

        embed = discord.Embed(
            title="Automod Action",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="User", value=f"{message.author.mention} (`{message.author.id}`)", inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.add_field(name="Message", value=message.content[:1024] or "No text", inline=False)
        embed.add_field(name="Violations", value=self.violations[message.author.id], inline=True)

        log_channel = await self.get_log_channel()
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        if message.content.startswith(config.COMMAND_PREFIX):
            return

        if config.AUTOMOD_IGNORE_STAFF and self.is_staff(message.author):
            return

        blocked_word = self.has_blocked_word(message.content)

        if config.AUTOMOD_BLOCK_INVITES and INVITE_PATTERN.search(message.content):
            await self.punish_message(message, "Discord invite links are not allowed")
            return

        if config.AUTOMOD_BLOCK_LINKS and URL_PATTERN.search(message.content):
            await self.punish_message(message, "Links are not allowed")
            return

        if blocked_word:
            await self.punish_message(message, "Blocked word")
            return

        if config.AUTOMOD_BLOCK_CAPS and self.has_excessive_caps(message.content):
            await self.punish_message(message, "Too many capital letters")
            return

        if config.AUTOMOD_BLOCK_SPAM and self.is_spam(message):
            await self.punish_message(message, "Spam")


async def setup(bot):
    await bot.add_cog(AutoMod(bot))