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
    
        embed = discord.Embed(
            title=guild.name,
            color=discord.Color.blurple(),
            timestamp=discord.utils.utcnow()
        )

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        owner = guild.owner or await guild.fetch_member(guild.owner_id)
        
        embed.add_field(name="Owner", value=owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created", value=discord.utils.format_dt(guild.created_at, style="D"), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)

        await ctx.send(embed=embed)

    
async def setup(bot):
    await bot.add_cog(Info(bot))
