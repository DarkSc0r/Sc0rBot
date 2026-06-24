import discord
from discord.ext import commands
from datetime import timedelta
import settings

class welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.get_channel(settings.WELCOME_CHANNEL_ID)
        rules_channel = member.guild.get_channel(settings.RULES_CHANNEL_ID)
        get_rules_channel = member.guild.get_channel(settings.GET_ROLES_CHANNEL_ID)
        embed = discord.Embed(
            title=f"Welcome!!",
            description=f"Glad you joined the server {member.mention}! " \
             f"PLEASE don't forget to go to the {rules_channel.mention} channel to see our rules in this server! " \
             f"To get access to the ENTIRE(almost) server, please make your way to the {get_rules_channel.mention} channel and fill out all the roles you want! " \
             f"The <@&{settings.MEMBER_ID}> is how you get access!!",
            color=discord.Color.from_rgb(72, 141, 206),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=member.avatar)

        await welcome_channel.send(member.mention, embed=embed, allowed_mentions=discord.AllowedMentions(users=True))
    

async def setup(bot:commands.Bot):
    await bot.add_cog(welcome(bot))