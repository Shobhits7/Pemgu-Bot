import discord
from discord.ext import commands
from config.views import viewgame

class Game(commands.Cog, description="If you are bored... use these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="tictactoe", aliases=["ttt"], help="Will start an tic-tac-toe game")
    @commands.is_owner()
    async def tictactoe(self, ctx):
        await ctx.send('Tic Tac Toe: X goes first', view=viewgame.TicTacToeView())
    
    @commands.command(name="guess", aliases=["gs"], help="Will start an guessing game")
    async def guess(self, ctx):
        gsmbed = discord.Embed(
            colour=self.bot.color,
            title="Started the game",
            description="Try to guess now"
        )
        gsmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        view = viewgame.GuessView(bot=self.bot, ctx=ctx)
        view.message = await ctx.send(embed=gsmbed, view=view)

def setup(bot):
    bot.add_cog(Game(bot))