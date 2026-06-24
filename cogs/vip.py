import discord
from discord.ext import commands
import settings

class vip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_vip(self, member:discord.member):
        if member.guild_permissions.administrator:
            return True
        if member.guild_permissions.manage_messages:
            return True
        return any(role.id == settings.VIP_ID for role in member.roles)
        
    @commands.command(aliases=["usinf", "uinfo"])
    async def userinfo(self, ctx, member:discord.Member=None):
        if member == None:
            member = ctx.message.author
        
        if not await self.is_vip(ctx.author):
            await ctx.send("Polls can only be created by Moderators.")
            return
        
        await ctx.message.delete()
        
        roles = [role for role in member.roles]

        embed = discord.Embed(
            title="User Info",
            description=f"{member.display_name}'s info:",
            color=discord.Color.from_rgb(113, 14, 18),
            timestamp=ctx.message.created_at
        )

        embed.set_thumbnail(url=member.avatar)
        
        embed.add_field(name="Name:", value=f"{member.name}")
        embed.add_field(name="Created At:", value=member.created_at.strftime("%a - %B %#d, %Y || %I:%M %p "))
        embed.add_field(name="Joined At:", value=member.joined_at.strftime("%a - %B %#d, %Y || %I:%M %p "))
        
        embed.add_field(name=f"Roles ({len(roles)}):", value=" ".join([role.mention for role in roles]))
        embed.add_field(name="Top Role:", value=member.top_role.mention)
        
        embed.add_field(name="Bot?", value=member.bot)

        await ctx.send(embed=embed)
async def setup(bot:commands.Bot):
    await bot.add_cog(vip(bot))