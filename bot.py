import os
import disocrd
import random
import disnake
from disnake.ext import commands
import database as db
import constants as var
from discord.ext import commands

PREFIX = ''

clinet = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event

async def on_ready():
  print('Под поключен✅')

@bot.event
async def on_guild_join(guild):
    if not await db.PLUGINS.count_documents({"_id": guild.id}, limit=1):
        await db.PLUGINS.insert_one({

            "_id": guild.id,
            "Leveling": False,
            "Moderation": True,
            "ReactionRoles": True,
            "Welcome": False,
            "Verification": False,
            "Chatbot": True,
            "AutoMod": False,
            "Fun": True,
            "Giveaway": True
        }) 

@client.commands( pass_context = True)      
