import sys
import traceback
import disnake
import asyncio
from disnake.ext import commands
from constants import C_RED


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Неправильный канал
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send(
                embed=disnake.Embed(
                    title="Неправильный канал",
                    description=(
                        "🚫 Вы уверены что ID канала "
                        "или упоминание канала было правильное"
                    ),
                    color=C_RED
                ).set_footer(
                    text=(
                        "Вы можете упоминуть канал (пример: #general)"
                        " или использовать id канала (пример: 83351608458669515)"
                    )
                )
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed=disnake.Embed(
                    title="отсутствует",
                    description=(
                        "🚫 У вас нет разрешения чтобы сделать это "
                        f"{ctx.author.name} "
                    ),
                    color=C_RED
                )
            )

      
