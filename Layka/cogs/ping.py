# Импорты
import random
import json
import re
import discord

from discord.ext import commands

LISTOFBIRDS = ["https://i.imgur.com/18cOdIx.png"]


def load_json(filename):
# Загружает json файл
    with open(filename, encoding='utf-8') as infile:
        return json.load(infile)


def write_json(filename, contents):
# Обновляет jsom файл
    with open(filename, 'w') as outfile:
        json.dump(contents, outfile, ensure_ascii=True, indent=4)


def clean_string(string):
 
    string = re.sub('@', '@\u200b', string)
    string = re.sub('#', '#\u200b', string)
    return string


class RollParser(commands.Converter):
  
    async def convert(self, ctx, argument):
        matches = re.search(r"(?:(\d*)-)?(\d*)", argument)
        minshit = matches.group(1) or 1
        maxshit = matches.group(2) or 100
        return (int(minshit), int(maxshit))


class Ping:
    
    def __init__(self, bot):
        self.bot = bot
        self.dogs = load_json('cats.json')
        self.cats = load_json('layka.json')
        self.cute = load_json('cute.json')

    @commands.command()
    async def roll(self, ctx, *, results: RollParser = None):
      
        results = results if results is not None else (1, 100)
        roll = random.randint(results[0], results[1])
        await ctx.send(f"**{ctx.author.name}** rolls **{roll}** ({results[0]}-{results[1]})")

    @commands.command()
    async def ping(self, ctx):
      
        await ctx.send("pong! {0:.2f}ms".format(self.bot.latency * 1000))


    @commands.command()
    async def echo(self, ctx, destination: discord.TextChannel=None, *, msg: str):
       
       
        if not destination.permissions_for(ctx.author).send_messages:
            return await ctx.message.add_reaction("\N{WARNING SIGN}")
        msg = clean_string(msg)
        destination = ctx.message.channel if destination is None else destination
        await destination.send(msg)
        return await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    async def get_cute(self):
       
        key = random.choice(list(self.cute.keys()))
        response = random.choice(self.cute[key])
        return response

    async def get_cats(self):
        
        key = random.choice(list(self.cats.keys()))
        response = random.choice(self.cats[key])
        return response

    async def get_layka(self):
        
        key = random.choice(list(self.layka.keys()))
        response = random.choice(self.layka[key])
        return response

    @commands.command(name="aww")
    async def cmd_aww(self, ctx):
       
        response = await self.get_cute()
        await ctx.send(response)

    @commands.command(name="awwbomb")
    async def cmd_awwbomb(self, ctx):
        
        response = ""
        for _ in range(10):
            try:
                response += "{}\n".format(await self.get_cute())
            except KeyError:
                pass

        await ctx.send(response)

    @commands.command(name="cat")
    async def cmd_cat(self, ctx):
      
        response = await self.get_dog()
        await ctx.send(response)

    @commands.command(name="catbomb")
    async def cmd_catbomb(self, ctx):
# Дает вам 10 случайных фотографий котиков :D
        response = ""
        for _ in range(10):
            try:
                response += "{}\n".format(await self.get_cat())
            except KeyError:
                pass

        await ctx.send(response)

    @commands.command(name="laykabomb")
    async def cmd_laykabomb(self, ctx):
# Дает вам 10 случайных фотографий лайек   
        response = ""
        for _ in range(10):
            try:
                response += "{}\n".format(await self.get_layka())
            except KeyError:
                pass

        await ctx.send(response)

    @commands.command(name="layka")
    async def cmd_layka(self, ctx):
 
#  Дает вам случайную картинку лайки боже
           
        response = await self.get_cat()
        await ctx.send(response)


def setup(bot):
    bot.add_cog(Ping(bot))
