import discord
from discord.ext import commands

import config


class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_staff(self, member):
        if member.guild_permissions.administrator:
            return True

        if member.guild_permissions.manage_messages:
            return True

        return any(role.id == config.STAFF_ROLE_ID for role in member.roles)

    @commands.command()
    async def poll(self, ctx, *, question):
        if ctx.guild is None:
            await ctx.send("Polls can only be made inside the server.")
            return

        if not self.is_staff(ctx.author):
            await ctx.send("You need to be staff to create polls.", delete_after=6)
            return

        embed = discord.Embed(
            title="New Poll",
            description=question,
            color=discord.Color.blurple(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(
            name="Vote",
            value="\U0001F44D Yes\n\U0001F44E No",
            inline=False
        )
        embed.set_footer(
            text=f"Poll started by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )

        poll_message = await ctx.send(
            content=f"<@&{config.MEMBER_ROLE_ID}>",
            embed=embed
        )

        await poll_message.add_reaction("\U0001F44D")
        await poll_message.add_reaction("\U0001F44E")


async def setup(bot):
    await bot.add_cog(Polls(bot))