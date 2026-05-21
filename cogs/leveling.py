import json
import os
import random
import time

import discord
from discord.ext import commands

import config


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.levels = self.load_json_file(config.XP_FILE)
        self.voice_levels = self.load_json_file(config.VOICE_XP_FILE)
        self.xp_cooldowns = {}
        self.voice_join_times = {}

    def load_json_file(self, filename):
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)

        return {}

    def save_json_file(self, filename, data):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    async def get_log_channel(self):
        channel = self.bot.get_channel(config.LOG_CHANNEL_ID)

        if channel is None:
            channel = await self.bot.fetch_channel(config.LOG_CHANNEL_ID)

        return channel

    def get_user_level_data(self, user_id):
        user_id = str(user_id)

        if user_id not in self.levels:
            self.levels[user_id] = {
                "level": 1,
                "xp": 0,
                "total_xp": 0
            }

        return self.levels[user_id]

    def xp_needed_for_next_level(self, level):
        return 100 + ((level - 1) * 75)

    async def add_xp(self, message):
        now = time.time()

        if self.xp_cooldowns.get(message.author.id, 0) > now:
            return

        self.xp_cooldowns[message.author.id] = now + config.XP_COOLDOWN_SECONDS

        user_data = self.get_user_level_data(message.author.id)
        gained_xp = random.randint(config.TEXT_XP_MIN, config.TEXT_XP_MAX)

        user_data["xp"] += gained_xp
        user_data["total_xp"] += gained_xp

        leveled_up = False

        while user_data["xp"] >= self.xp_needed_for_next_level(user_data["level"]):
            user_data["xp"] -= self.xp_needed_for_next_level(user_data["level"])
            user_data["level"] += 1
            leveled_up = True

        self.save_json_file(config.XP_FILE, self.levels)

        if leveled_up:
            await message.channel.send(
                f"\U0001F389 {message.author.mention} leveled up to **Level {user_data['level']}**!"
            )

    def get_voice_data(self, user_id):
        user_id = str(user_id)

        if user_id not in self.voice_levels:
            self.voice_levels[user_id] = {
                "level": 1,
                "xp": 0,
                "total_xp": 0,
                "total_seconds": 0
            }

        return self.voice_levels[user_id]

    def voice_xp_needed_for_next_level(self, level):
        return 100 + ((level - 1) * 100)

    def add_voice_xp(self, member, seconds):
        minutes = int(seconds // 60)
        if minutes <= 0:
            return None

        user_data = self.get_voice_data(member.id)
        gained_xp = minutes * config.VOICE_XP_PER_MINUTE

        user_data["xp"] += gained_xp
        user_data["total_xp"] += gained_xp
        user_data["total_seconds"] += int(seconds)

        leveled_up = False

        while user_data["xp"] >= self.voice_xp_needed_for_next_level(user_data["level"]):
            user_data["xp"] -= self.voice_xp_needed_for_next_level(user_data["level"])
            user_data["level"] += 1
            leveled_up = True

        self.save_json_file(config.VOICE_XP_FILE, self.voice_levels)

        return {
            "minutes": minutes,
            "xp": gained_xp,
            "leveled_up": leveled_up,
            "level": user_data["level"]
        }

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_data = self.get_user_level_data(member.id)
        needed_xp = self.xp_needed_for_next_level(user_data["level"])

        embed = discord.Embed(
            title=f"{member.display_name}'s Text Rank",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Level", value=user_data["level"], inline=True)
        embed.add_field(name="XP", value=f"{user_data['xp']} / {needed_xp}", inline=True)
        embed.add_field(name="Total XP", value=user_data["total_xp"], inline=True)

        await ctx.send(embed=embed)

    @commands.command(aliases=["vrank"])
    async def voicerank(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_data = self.get_voice_data(member.id)
        needed_xp = self.voice_xp_needed_for_next_level(user_data["level"])
        total_minutes = user_data["total_seconds"] // 60

        embed = discord.Embed(
            title=f"{member.display_name}'s Voice Rank",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Voice Level", value=user_data["level"], inline=True)
        embed.add_field(name="Voice XP", value=f"{user_data['xp']} / {needed_xp}", inline=True)
        embed.add_field(name="Total Voice XP", value=user_data["total_xp"], inline=True)
        embed.add_field(name="Voice Time", value=f"{total_minutes} minutes", inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        text_lines = []
        voice_lines = []

        sorted_text_users = sorted(
            self.levels.items(),
            key=lambda user: user[1]["total_xp"],
            reverse=True
        )
        sorted_voice_users = sorted(
            self.voice_levels.items(),
            key=lambda user: user[1]["total_xp"],
            reverse=True
        )

        for place, (user_id, user_data) in enumerate(sorted_text_users[:10], start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"User ID {user_id}"

            text_lines.append(
                f"**{place}.** {name} - Level **{user_data['level']}** | `{user_data['total_xp']} XP`"
            )

        for place, (user_id, user_data) in enumerate(sorted_voice_users[:10], start=1):
            member = ctx.guild.get_member(int(user_id))
            name = member.display_name if member else f"User ID {user_id}"
            total_minutes = user_data["total_seconds"] // 60

            voice_lines.append(
                f"**{place}.** {name} - Voice Level **{user_data['level']}** | `{user_data['total_xp']} XP` | `{total_minutes} min`"
            )

        embed = discord.Embed(
            title="Server Leaderboards",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(
            name="Text XP",
            value="\n".join(text_lines) if text_lines else "Nobody has earned text XP yet.",
            inline=False
        )
        embed.add_field(
            name="Voice XP",
            value="\n".join(voice_lines) if voice_lines else "Nobody has earned voice XP yet.",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        if not message.content.startswith(config.COMMAND_PREFIX):
            await self.add_xp(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if before.channel == after.channel:
            return

        if before.channel is None and after.channel is not None:
            self.voice_join_times[member.id] = time.time()
            return

        if before.channel is not None and after.channel is None:
            joined_at = self.voice_join_times.pop(member.id, None)

            if joined_at is None:
                return

            result = self.add_voice_xp(member, time.time() - joined_at)

            if result and result["leveled_up"]:
                log_channel = await self.get_log_channel()
                await log_channel.send(
                    f"\U0001F399 {member.mention} reached **Voice Level {result['level']}**!"
                )

            return

        if before.channel is not None and after.channel is not None:
            self.voice_join_times.setdefault(member.id, time.time())


async def setup(bot):
    await bot.add_cog(Leveling(bot))