import discord
from discord.ext import commands
import settings

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_staff(self, member:discord.member):
        if member.guild_permissions.administrator:
            return True
        if member.guild_permissions.manage_messages:
            return True
        return any(role.id == settings.STAFF_ID for role in member.roles)

    @commands.command()
    async def poll(self, ctx, *, question):
        if not await self.is_staff(ctx.author):
            await ctx.send("Polls can only be created by Moderators.")
            return

        await ctx.message.delete()

        embed = discord.Embed(
            title="New Poll",
            description=question,
            color=discord.Color.from_rgb(113, 14, 18),
            timestamp=ctx.message.created_at
        )

        embed.add_field(name="Vote", value="👍 - Yes\n\n👎 - No", inline=False)
        poll_message = await ctx.send(content=f"<@&{settings.MEMBER_ID}>", embed=embed)
        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")

    @commands.command(aliases=["sd"])
    async def shutdown(self, ctx):
        if not await self.is_staff(ctx.author):
            await ctx.send("Polls can only be created by Moderators.")
            return
        
        await ctx.message.delete()

        await ctx.send(f"{ctx.author.mention} is shutting down the bot...")
        await self.bot.close()


async def setup(bot:commands.Bot):
    await bot.add_cog(moderation(bot))