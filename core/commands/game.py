import discord
from discord.ext import commands
import core.utils.context as ctx
import core.views.gameview as gv

class Game(commands.Cog, description="If you are bored... use these"):
    def __init__(self, bot):
        self.bot = bot

    # Counter
    @commands.command(name="counter", aliases=["ctr"], help="Will start an counter")
    async def counter(self, ctx:ctx.JakeTheDogContext):
        ctrmbed = discord.Embed(
            colour=self.bot.colour,
            description="Click the button for counting"
        )
        view = gv.CounterView(ctx)
        view.message = await ctx.send(embed=ctrmbed, view=view)

    # RockPaperScissors
    @commands.command(name="rockpaperscissors", aliases=["rps"], help="Will start an Rock-Paper-Scissors game")
    async def rockpaperscissors(self, ctx:commands.Context):
        rpsmbed = discord.Embed(
            colour=self.bot.colour,
            description="Choose your **tool** with the buttons:",
            timestamp=ctx.message.created_at
        )
        rpsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = gv.RPSView(ctx)
        view.message = await ctx.send(embed=rpsmbed, view=view)

    # Guess
    @commands.command(name="guess", aliases=["gs"], help="Will start an guessing game")
    async def guess(self, ctx:commands.Context):
        gsmbed = discord.Embed(
            colour=self.bot.colour,
            description="Try to **guess** now"
        )
        gsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = gv.GuessView(ctx)
        view.message = await ctx.send(embed=gsmbed, view=view)

    # TicTacToe
    @commands.command(name="tictactoe", aliases=["ttt"], help="Will start an tic-tac-toe game")
    @commands.is_owner()
    async def tictactoe(self, ctx:commands.Context):
        await ctx.send('Tic Tac Toe: X goes first', view=gv.TicTacToeView())

def setup(bot):
    bot.add_cog(Game(bot))