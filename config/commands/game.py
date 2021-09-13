import discord
from discord.ext import commands
from config.views.tic_tac_toe import TicTacToeView

class Game(commands.Cog, description="If you are bored... use these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="tictactoe", aliases=["ttt"], help="Will start an tic-tac-toe game")
    async def tictactoe(self, ctx):
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToeView())

def setup(bot):
    bot.add_cog(Game(bot))