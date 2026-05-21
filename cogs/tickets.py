import asyncio

import discord
from discord.ext import commands

import config


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_existing_report_channel(self, guild, member):
        expected_name = f"report-{member.name}".lower()

        for channel in guild.text_channels:
            if channel.name.lower() == expected_name:
                return channel

        return None

    @commands.command()
    async def report(self, ctx, member: discord.Member = None, *, reason=None):
        if ctx.guild is None:
            await ctx.send("Reports can only be made inside the server.")
            return

        if member is None or reason is None:
            await ctx.send("Use it like this: `!report @user reason`")
            return

        existing_channel = self.get_existing_report_channel(ctx.guild, ctx.author)

        if existing_channel:
            await ctx.send(
                f"You already have an open report channel: {existing_channel.mention}",
                delete_after=10
            )
            return

        category = ctx.guild.get_channel(config.REPORT_CATEGORY_ID)
        staff_role = ctx.guild.get_role(config.STAFF_ROLE_ID)

        if category is None:
            await ctx.send("I could not find the report category. Check `REPORT_CATEGORY_ID`.")
            return

        if not isinstance(category, discord.CategoryChannel):
            await ctx.send("`REPORT_CATEGORY_ID` needs to be a category ID, not a text channel ID.")
            return

        if staff_role is None:
            await ctx.send("I could not find the staff role. Check `STAFF_ROLE_ID`.")
            return

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            ctx.author: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            staff_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),
            ctx.guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True
            )
        }

        try:
            ticket_channel = await ctx.guild.create_text_channel(
                name=f"report-{ctx.author.name}",
                category=category,
                overwrites=overwrites,
                reason=f"Report created by {ctx.author}"
            )
        except discord.Forbidden:
            await ctx.send("I do not have permission to create channels. Give me **Manage Channels**.")
            return

        embed = discord.Embed(
            title="\U0001F6A8 Private Report",
            color=discord.Color.red(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="Reported User", value=f"{member.mention} (`{member.id}`)", inline=False)
        embed.add_field(name="Reported By", value=f"{ctx.author.mention} (`{ctx.author.id}`)", inline=False)
        embed.add_field(name="Original Channel", value=ctx.channel.mention, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)

        await ticket_channel.send(
            content=f"{ctx.author.mention} {staff_role.mention}",
            embed=embed
        )

        await ctx.send(
            f"\U0001F4E9 {ctx.author.mention}, I made a private report channel: {ticket_channel.mention}",
            delete_after=10
        )

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def close(self, ctx):
        if not ctx.channel.name.startswith("report-"):
            await ctx.send("This command can only be used inside a report channel.")
            return

        await ctx.send("Closing this report in 5 seconds...")
        await asyncio.sleep(5)
        await ctx.channel.delete()


async def setup(bot):
    await bot.add_cog(Tickets(bot))