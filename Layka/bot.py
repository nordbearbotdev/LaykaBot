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
       
# Clear   
@client.commands( pass_context = True)      
@commnads.has_permession( administrator = True)

async def clear( ctx, amount = 100 ):
  await ctx.channel.purge( limit = amount )

# Kick
@client.commands( pass_context = True)      
@commnads.has_permession( administrator = True)

async def kick( ctx, member: discord.Member, , reason = None );
  await ctx.channel.purge( limit = 1 )
   
  await member.kick( reason = reason)
  await ctx.send( f'kick user:'
  
    
# Ban 
@client.command( pass_context = True )
@commands.has_permissions( administrator = True )                 

async def ban ( ctx, member: discord.Member, *, reason = None):
  await ctx.channel.purge( limit = 1 )
                 
  await member.ban( reason = reason ) 
  await ctx.send(f'ban user')           
                 
                 
                 
# Unban
@client.command( pass_context = True)                 

async def unban( ctx, *, member )                 

# Help-list                 
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
