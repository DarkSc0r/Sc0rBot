import discord
from discord.ext import commands

import config


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_log_channel(self):
        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(config.LOG_CHANNEL_ID)

        return channel

    def is_staff(self, member):
        if member.guild_permissions.administrator:
            return True

        if member.guild_permissions.manage_messages:
            return True

        return any(role.id == config.STAFF_ROLE_ID for role in member.roles)

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    async def clean(self, ctx, member: discord.Member = None, amount: int = None):
        if ctx.guild is None:
            await ctx.send("This command can only be used inside the server.")
            return

        if not self.is_staff(ctx.author):
            await ctx.send("You need to be staff to use this command.", delete_after=6)
            return

        if member is None or amount is None:
            await ctx.send("Use it like this: `!clean @user 7`", delete_after=8)
            return

        if amount <= 0:
            await ctx.send("The amount needs to be at least `1`.", delete_after=8)
            return

        if amount > config.CLEAN_MAX_DELETE:
            await ctx.send(
                f"You can only clean up to `{config.CLEAN_MAX_DELETE}` messages at once.",
                delete_after=8
            )
            return

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        deleted_count = 0

        def should_delete(message):
            nonlocal deleted_count

            if deleted_count >= amount:
                return False

            if message.pinned:
                return False

            if message.author.id != member.id:
                return False

            deleted_count += 1
            return True

        deleted_messages = await ctx.channel.purge(
            limit=config.CLEAN_SEARCH_LIMIT,
            check=should_delete,
            bulk=False
        )

        await ctx.send(
            f"Cleaned `{len(deleted_messages)}` message(s) from {member.mention}.",
            delete_after=6
        )

        log_channel = await self.get_log_channel()

        embed = discord.Embed(
            title="Messages Cleaned",
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Moderator", value=f"{ctx.author.mention} (`{ctx.author.id}`)", inline=False)
        embed.add_field(name="Target", value=f"{member.mention} (`{member.id}`)", inline=False)
        embed.add_field(name="Channel", value=ctx.channel.mention, inline=False)
        embed.add_field(name="Deleted", value=len(deleted_messages), inline=True)
        embed.add_field(name="Requested", value=amount, inline=True)

        await log_channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))