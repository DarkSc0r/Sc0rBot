import discord
from discord.ext import commands, tasks
import json
import os
import settings

class level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_members = set()
        self.voice_exp_loop.start()

    def cog_unload(self):
        self.voice_exp_loop.cancel()

    os.chdir(r'C:/Users/darks/Dev\Python/DiscordBot/DarkSc0rServer/level_info')

    @commands.command(name='leaderboard', aliases=['lb'])
    async def leaderboard(self, ctx, leaderboard_type='message'):
        leaderboard_type = leaderboard_type.lower()

        if leaderboard_type == 'voice':
            file_name = 'users_voice.json'
            title = 'Voice Leaderboard'
            emoji = '🎙️'
            color = discord.Color.from_rgb(155, 89, 182)
        else:
            file_name = 'users_message.json'
            title = 'Message Leaderboard'
            emoji = '💬'
            color = discord.Color.from_rgb(52, 152, 219)

        with open(file_name, 'r') as f:
            users = json.load(f)

        sorted_users = sorted(
            users.items(),
            key=lambda user_data: user_data[1]['experience'],
            reverse=True
        )

        embed = discord.Embed(
            title=f'{emoji} {title}',
            description='Top server members by XP',
            color=color
        )

        embed.set_author(
            name=ctx.guild.name,
            icon_url=ctx.guild.icon.url if ctx.guild.icon else None
        )

        medals = ['🥇', '🥈', '🥉']
        leaderboard_text = ''

        for place, (user_id, data) in enumerate(sorted_users[:10], start=1):
            member = ctx.guild.get_member(int(user_id))

            if member is None:
                name = 'Unknown User'
            else:
                name = member.display_name

            rank = medals[place - 1] if place <= 3 else f'`#{place}`'
            xp = data['experience']
            level = data['level']

            if place == 1:
                leaderboard_text += (
                    f'{rank} **{name}** 👑\n'
                    f'> Level `{level}`  |  XP `{xp}`\n\n'
                )
            else:
                leaderboard_text += (
                    f'{rank} **{name}**\n'
                    f'> Level `{level}`  |  XP `{xp}`\n\n'
                )

        if leaderboard_text == '':
            leaderboard_text = 'No users yet.'

        embed.add_field(
            name='Rankings',
            value=leaderboard_text,
            inline=False
        )

        author_id = str(ctx.author.id)
        your_rank = None

        for place, (user_id, data) in enumerate(sorted_users, start=1):
            if user_id == author_id:
                your_rank = place
                your_level = data['level']
                your_xp = data['experience']
                break

        if your_rank is not None:
            embed.add_field(
                name='Your Rank',
                value=f'You are `#{your_rank}` with level `{your_level}` and `{your_xp}` XP.',
                inline=False
            )

        embed.set_footer(text=f'{len(sorted_users)} ranked members')

        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('users_message.json', 'r') as m:
            users_message = json.load(m)

        with open('users_voice.json', 'r') as v:
            users_voice = json.load(v)

        await update_data(users_message, member)

        await update_data(users_voice, member)

        with open('users_message.json', 'w') as m:
            json.dump(users_message, m)

        with open('users_voice.json', 'w') as v:
            json.dump(users_voice, v)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        with open('users_message.json', 'r') as m:
            users_message = json.load(m)

        await update_data(users_message, message.author)
        await add_exp(users_message, message.author, 5)
        await level_up(users_message, message.author, "Messaging")

        with open('users_message.json', 'w') as m:
            json.dump(users_message, m)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return
        
        voice_user = (member.guild.id, member.id)

        if before.channel is None and after.channel is not None:
            self.voice_members.add(voice_user)
        elif before.channel is not None and after.channel is None:
            self.voice_members.discard(voice_user)

    @tasks.loop(minutes=1)
    async def voice_exp_loop(self):
        with open('users_voice.json', 'r') as v:
            users_voice = json.load(v)

        for guild_id, member_id in list(self.voice_members):
            guild = self.bot.get_guild(guild_id)

            if guild is None:
                self.voice_members.discard((guild_id, member_id))
                continue

            member = guild.get_member(member_id)

            if member is None or member.voice is None or member.voice.channel is None:
                self.voice_members.discard((guild_id, member_id))
                continue

            await update_data(users_voice, member)
            await add_exp(users_voice, member, 5)
            await level_up(users_voice, member, "Voice")

        with open('users_voice.json', 'w') as v:
            json.dump(users_voice, v)

    @voice_exp_loop.before_loop
    async def before_voice_exp_loop(self):
        await self.bot.wait_until_ready()

    @voice_exp_loop.error
    async def voice_exp_loop_error(self, error):
        print(f"Voice EXP loop error: {error}")

async def update_data(users, user):
    user_id = str(user.id)
    
    if user_id not in users:
        users[user_id] = {}
        users[user_id]['experience'] = 0
        users[user_id]['level'] = 1

async def add_exp(users, user, exp):
    user_id = str(user.id)
    users[user_id]['experience'] += exp
    
async def level_up(users, user, level_type):
    user_id = str(user.id)
    experience = users[user_id]['experience']
    lvl_start = users[user_id]['level']
    lvl_end = int(experience ** (1/4))
    level_channel = user.guild.get_channel(settings.LEVEL_CHANNEL_ID)

    if lvl_start < lvl_end:
        await level_channel.send(f'{user.mention} has leveled up their {level_type} level to level {lvl_end}')
        users[user_id]['level'] = lvl_end

async def setup(bot:commands.Bot):
    await bot.add_cog(level(bot))