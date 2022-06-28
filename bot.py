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
