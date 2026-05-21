import discord
from discord.ext import commands


class Afk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.afk_users = {}

    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
        self.afk_users[ctx.author.id] = reason

        embed = discord.Embed(
            title="AFK Set",
            description=f"{ctx.author.mention} is now AFK.",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Reason", value=reason, inline=False)

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.afk_users and not message.content.startswith("!afk"):
            self.afk_users.pop(message.author.id)

            await message.channel.send(
                f"Welcome back {message.author.mention}, I removed your AFK status.",
                delete_after=5
            )

        for user in message.mentions:
            if user.id in self.afk_users:
                reason = self.afk_users[user.id]

                await message.channel.send(
                    f"{user.mention} is currently AFK: {reason}",
                    delete_after=8
                )


async def setup(bot):
    await bot.add_cog(Afk(bot))