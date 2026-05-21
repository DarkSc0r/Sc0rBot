import discord
from discord.ext import commands

import config


PUBLIC_COMMANDS = [
    ("!commands", "Shows this command list."),
    ("!afk <reason>", "Sets your AFK status so people know you are away."),
    ("!rank", "Shows your text chat level and XP."),
    ("!rank @user", "Shows another member's text chat level and XP."),
    ("!voicerank", "Shows your voice level, XP, and voice time."),
    ("!voicerank @user", "Shows another member's voice level, XP, and voice time."),
    ("!vrank", "Short version of !voicerank."),
    ("!leaderboard", "Shows text and voice leaderboards."),
    ("!lb", "Short version of !leaderboard."),
    ("!report @user <reason>", "Creates a private report ticket for staff.")
]

STAFF_COMMANDS = [
    ("!poll <question>", "Creates a yes/no poll and pings the member role."),
    ("!clean @user <amount>", "Deletes that many recent messages from a user in the current channel."),
    ("!close", "Closes a report ticket channel.")
]

AUTOMATIC_FEATURES = [
    "Text XP is earned by chatting normally.",
    "Voice XP is earned by spending time in voice channels.",
    "Edited and deleted messages are logged.",
    "Audit log actions are sent to the logs channel.",
    "Automod can block invites, links, spam, caps, and blocked words."
]


class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def format_commands(self, command_items):
        return "\n".join(
            f"`{name}` - {description}"
            for name, description in command_items
        )

    @commands.command(name="commands", aliases=["cmds", "commandlist"])
    async def commands_list(self, ctx):
        embed = discord.Embed(
            title="Server Commands",
            description=f"Prefix: `{config.COMMAND_PREFIX}`",
            color=discord.Color.blurple(),
            timestamp=discord.utils.utcnow()
        )

        embed.add_field(
            name="Public Commands",
            value=self.format_commands(PUBLIC_COMMANDS),
            inline=False
        )
        embed.add_field(
            name="Staff Commands",
            value=self.format_commands(STAFF_COMMANDS),
            inline=False
        )
        embed.add_field(
            name="Automatic Features",
            value="\n".join(f"- {feature}" for feature in AUTOMATIC_FEATURES),
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CommandList(bot))
