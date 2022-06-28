import os
import disocrd
import random
from discord.ext import commands

PREFIX = ''

clinet = commands.Bot( command_prefix = PREFIX )
client.remove_command( 'help' )

@client.event

async def on_ready():
  print('Под поключен✅')
