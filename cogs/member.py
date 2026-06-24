import discord
from discord.ext import commands
import settings

class member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_member(self, member:discord.member):
        if member.guild_permissions.send_messages:
            return True
        return any(role.id == settings.MEMBER_ID for role in member.roles)
        
    @commands.command()
    async def game(self, ctx, member:discord.Member=None):
        if not await self.is_member(ctx.author):
            await ctx.send("You do not have the member role. Please go to the 'Roles' channel to gain this role!")
            return

        await ctx.send(f"{ctx.author.mention} DarkSc0r is working on a game called 'Project: Unknown'."
        " 'Project Unknown' is a game about re-creating life from virtually nothing." \
        " Awaking in a bunker, the player knows nothing. Exiting the bunker reveals a wasteland extending for miles." \
        " Existing in the outside world comes with a cause. Prolonged exposer outside causes sickness." \
        " Retreating back into your bunker you find a few items."
        " (Omitting on difficulty) There is a crafting bench, bed, and rations." \
        " Eventually you learn that you can survival outside, but the time is very limited." \
        " You gather resources and eventually are able to expand your bunker(Bunker Upgrading)." \
        " Learning new recipes and the world around you, you are eventually able to create a Protective Suit." \
        " This suit allows you to exist in the waste land for longer. With this you are able to explore more." \
        " This leads to the player finding abandoned labs as well as other TBD structures." \
        " In these structures you find new, much harder, recipes." \
        " You also find Lore Items which help you figure out what happened." \
        " Exploring enough structures will get you the ultimate recipe. The Creation Recipe." \
        " This is the way to 'beat' the game. It tells the player how to re-create life.")

    # @commands.command(aliases='lb')
    # async def leaderboard(self):
    #     ...

async def setup(bot:commands.Bot):
    await bot.add_cog(member(bot))