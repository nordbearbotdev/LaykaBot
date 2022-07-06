# Импорты
import logging
import discord
import datetime
import traceback
import psutil
import os
import sqlite3
import functools
import asyncio

from cogs.utils import checks
from discord.ext import commands
from collections import Counter

log = logging.getLogger()

LOGGING_CHANNEL = 344986487676338187


class Stats:
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    async def on_command(self, ctx):
        command = ctx.command.qualified_name
        self.bot.command_stats[command] += 1
        message = ctx.message
        destination = None
        if ctx.guild is None:
            destination = 'Приватное сообщение'
            guild_id = None
        else:
            destination = '#{0.channel} ({0.guild})'.format(message)
            guild_id = ctx.guild.id

        log.info('{0.created_at}: {0.author.name} в {1}: {0.content}'.format(
            message, destination))

    async def on_socket_response(self, msg):
        self.bot.socket_stats[msg.get('t')] += 1

    @commands.command(hidden=True)
    @commands.is_owner()
    async def commandstats(self, ctx, limit=20):
        counter = self.bot.command_stats
        width = len(max(counter, key=len))
        total = sum(counter.values())

        if limit > 0:
            common = counter.most_common(limit)
        else:
            common = counter.most_common()[limit:]
        output = '\n'.join('{0:<{1}}: {2}'.format(k, width, c)
                           for k, c in common)

        await ctx.send('```\n{}\n```'.format(output))

    @commands.command(hidden=True)
    async def socketstats(self, ctx, limit=20):
        delta = datetime.datetime.utcnow() - self.bot.uptime
        minutes = delta.total_seconds() / 60
        total = sum(self.bot.socket_stats.values())
        cpm = total / minutes
        width = len(max(self.bot.socket_stats, key=lambda x: len(str(x))))
        con = self.bot.socket_stats.most_common(limit)
        fancy = '\n'.join('{0:<{1}}: {2:>12,}'.format(str(k), width, c)
                         for k, c in con)

        await ctx.send('{0:,} наблюдаемые события сокета ({1:.2f}/minute):\n```{2}```'.format(total, cpm, fancy))

    def get_bot_uptime(self, *, brief=False):
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if not brief:
            if days:
                fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
            else:
                fmt = '{h} hours, {m} minutes, and {s} seconds'
        else:
            fmt = '{h}h {m}m {s}s'
            if days:
                fmt = '{d}d ' + fmt

        return fmt.format(d=days, h=hours, m=minutes, s=seconds)

    @commands.command()
    async def uptime(self, ctx):
      # Показывает насколько бот долго на сервере
        em = discord.Embed(title="Локальное время", description=str(
            datetime.datetime.utcnow())[:-7], colour=0x14e818)
        em.set_author(name=self.bot.user.name,
                      icon_url=self.bot.user.avatar_url)
        em.add_field(name="Current uptime",
                     value=self.get_bot_uptime(brief=True), inline=True)
        em.add_field(name="Start time", value=str(
            self.bot.uptime)[:-7], inline=True)
        await ctx.send(embed=em)
        # await ctx.send('Uptime: **{}**'.format(self.get_bot_uptime()))






    def get_activity(self, g, diff):
        self.c.execute('''SELECT count(*) as c, author
                          FROM messages
                          WHERE (server=? AND unix > ?)
                          GROUP BY author
                          ORDER BY c DESC;''',
                          (g.id, diff))
        record = self.c.fetchall()
        return record



    @commands.group(invoke_without_command=True)
    async def activity(self, ctx, unit: str="месяц"):
        unit = unit.lower()
        time_dict = {
            "day": 86400,
            "week": 604800,
            "month": 2592000,
            "year": 31556952
        }
        if unit not in time_dict:
            unit = "месяц"
        time_seconds = time_dict.get(unit, 2592000)
        now = int(datetime.datetime.utcnow().timestamp())
        diff = now - time_seconds
        thing = functools.partial(self.get_activity, ctx.guild, diff)
        #record = await self.bot.loop.run_in_executor(None, thing)
        self.c.execute('''SELECT count(*) as c, author
                          FROM messages
                          WHERE (server=? AND unix > ?)
                          GROUP BY author
                          ORDER BY c DESC;''',
                          (ctx.guild.id, diff))
        record = self.c.fetchall()
        e = discord.Embed(title=f"Активность за последним {unit}", description=f"{sum(x[0] for x in record)} сообщений от {len(record)} главы")
        for n, v in enumerate(record[:25]):
            try:
                name = ctx.guild.get_member(int(v[1])).name
            except AttributeError:
                name = f"Неизвестный пользователь"
            e.add_field(name=f"{n+1}. {name}", value=f"{v[0]} сообщение")
        
        await ctx.send(embed=e)

    
    
    
    @activity.command(aliases=['characters', 'words'])
    async def char(self, ctx, unit: str="day"):
        if ctx.author.id != 106429844627169280 and unit != "day":
            return await ctx.send("График активности для временных интервалов более одного дня занимает слишком много времени, извините!")
        unit = unit.lower()
        time_dict = {
            "day": 86400,
            "week": 604800,
            "month": 2592000,
            "year": 31556952
        }
        if unit not in time_dict:
            unit = "month"
        time_seconds = time_dict.get(unit, 2592000)
        now = int(datetime.datetime.utcnow().timestamp())
        diff = now - time_seconds
        self.c.execute('''SELECT SUM(LENGTH(content)) as c, author, COUNT(*)
                          FROM messages
                          WHERE (server=? AND unix > ?)
                          GROUP BY author
                          ORDER BY c DESC LIMIT 25;''',
                          (ctx.guild.id, diff))
        record = self.c.fetchall()
        e = discord.Embed(title="Текущая таблица лидеров", description=f"Активность за последним {unit}")
        for n, v in enumerate(record):
            try:
                name = ctx.guild.get_member(int(v[1])).name
            except AttributeError:
                name = f"Неизвестный пользователь"
            ratio = int(v[0] / v[2])
            e.add_field(name=f"{n+1}. {name}", value=f"{v[0]:,} символы ({ratio} c/m)")
        
        await ctx.send(embed=e)

    @commands.command(aliases=['stats'])
    async def about(self, ctx):
        embed = discord.Embed(description='Layka bot 0.1')
        embed.title = 'О боте:'
        embed.colour = 0x738bd7

        owner = self.bot.get_user(self.bot.owner_id)

        embed.set_author(name=str(owner), icon_url=owner.avatar_url)

        total_members = sum(1 for _ in self.bot.get_all_members())
        total_online = len(
            {m.id for m in self.bot.get_all_members() if m.status is discord.Status.online})
        total_unique = len(self.bot.users)

        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)

        text = len(text_channels)
        voice = len(voice_channels)

        embed.add_field(
            name='Пользователи', value=f'{total_members} весь\n{total_unique} уникальный\n{total_online} уникальных в онлайне')
        embed.add_field(
            name='Каналы', value=f'{text + voice} весь\n{text} текст\n{voice} войсе')

        memory_usage = self.process.memory_full_info().uss / 1024**2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(
            name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')

        embed.add_field(name='Guilds', value=len(self.bot.guilds))
        embed.add_field(name='Commands Run', value=sum(
            self.bot.command_stats.values()))
        embed.add_field(name='Uptime', value=self.get_bot_uptime(brief=True))
        embed.set_footer(text='Сделано с  💖 с помощью discord.py',
                         icon_url='http://i.imgur.com/5BFecvA.png')
        await ctx.send(embed=embed)

    async def send_guild_stats(self, e, guild):
        e.add_field(name='Name', value=guild.name)
        e.add_field(name='ID', value=guild.id)
        e.add_field(
            name='Owner', value=f'{guild.owner} (ID: {guild.owner.id})')

        bots = sum(m.bot for m in guild.members)
        total = guild.member_count
        online = sum(m.status is discord.Status.online for m in guild.members)
        e.add_field(name='Members', value=str(total))
        e.add_field(name='Bots', value=f'{bots} ({bots/total:.2%})')
        e.add_field(name='Online', value=f'{online} ({online/total:.2%})')

        if guild.icon:
            e.set_thumbnail(url=guild.icon_url)

        if guild.me:
            e.timestamp = guild.me.joined_at

        ch = self.bot.get_channel(LOGGING_CHANNEL)
        await ch.send(embed=e)

    async def on_guild_join(self, guild):
        e = discord.Embed(colour=0x53dda4, title='New Guild')  # green colour
        await self.send_guild_stats(e, guild)

    async def on_guild_remove(self, guild):
        e = discord.Embed(colour=0xdd5f53, title='Left Guild')  # red colour
        await self.send_guild_stats(e, guild)

    async def on_command_error(self, ctx, error):
        ignored = (commands.NoPrivateMessage, commands.DisabledCommand, commands.CheckFailure,
                   commands.CommandNotFound, commands.UserInputError, discord.Forbidden)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        e = discord.Embed(title='Command Error', colour=0xcc3366)
        e.add_field(name='Name', value=ctx.command.qualified_name)
        e.add_field(name='Author', value=f'{ctx.author} (ID: {ctx.author.id})')

        fmt = f'Channel: {ctx.channel} (ID: {ctx.channel.id})'
        if ctx.guild:
            fmt = f'{fmt}\nGuild: {ctx.guild} (ID: {ctx.guild.id})'

        e.add_field(name='Location', value=fmt, inline=False)

        exc = ''.join(traceback.format_exception(
            type(error), error, error.__traceback__, chain=False))
        e.description = f'```py\n{exc}\n```'
        e.timestamp = datetime.datetime.utcnow()
        ch = self.bot.get_channel(LOGGING_CHANNEL)
        await ch.send(embed=e)


old_on_error = commands.Bot.on_error


async def on_error(self, event, *args, **kwargs):
    e = discord.Embed(title='Event Error', colour=0xa32952)
    e.add_field(name='Event', value=event)
    e.description = '```py\n%s\n```' % traceback.format_exc()
    try:
        big_xd = f"Name: {args[0].guild.name}\nID: {args[0].guild.id}"
        e.add_field(name="location", value=big_xd)
    except:
        pass


    e.timestamp = datetime.datetime.utcnow()
    ch = self.get_channel(LOGGING_CHANNEL)
    try:
        await ch.send(embed=e)
    except:
        await ch.send("tried sending an error but no xd")


def setup(bot):
    if not hasattr(bot, 'command_stats'):
        bot.command_stats = Counter()

    if not hasattr(bot, 'socket_stats'):
        bot.socket_stats = Counter()

    bot.add_cog(Stats(bot))
    commands.Bot.on_error = on_error


def teardown(bot):
    commands.Bot.on_error = old_on_error
