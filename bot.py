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
       
@client.commands( pass_context = True)      
@commnads.has_permession( administrator = True)

# Kick
@client.commands( pass_context = True)      
@commnads.has_permession( administrator = True)


async def kick( ctx, member:)

async def help( ctx ):
  emb = discord.Embed( title = 'Навигация по-командам' )
  
  emb.add_field( name = '{}clear'.format( PREFIX ), value = 'Очистка чата 🗑')
  emb.add_field( name = '{}kick'.format( PREFIX ), value = 'Удаление участника с сервера ❌ ') 
  emb.add_field( name = '{}ban'.format( PREFIX ), value = 'Ограничение доступа к серверу ⚠️ ')
  emb.add_field( name = '{}unban'.format( PREFIX ), value = 'Удаление ограничения к доступу к серверу')

)


# Получение токена
token = open( 'token.txt',  'r' ).readline()

client.run( token )
