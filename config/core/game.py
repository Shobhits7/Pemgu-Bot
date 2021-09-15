import discord
from discord.ext import commands
from config.views import tictactoe

class Game(commands.Cog, description="If you are bored... use these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="tictactoe", aliases=["ttt"], help="Will start an tic-tac-toe game")
    @commands.is_owner()
    async def tictactoe(self, ctx):
        await ctx.send('Tic Tac Toe: X goes first', view=tictactoe.TicTacToeView())

def setup(bot):
    bot.add_cog(Game(bot))