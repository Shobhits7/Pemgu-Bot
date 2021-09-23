import discord
from discord.ext import commands
import config.views.funview as fv

class Fun(commands.Cog, description="For just having an great fun time"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="counter", aliases=["ctr"], help="Will start an counter")
    async def counter(self, ctx:commands.Conext):
        ctrmbed = discord.Embed(
            colour=self.bot.colour,
            title="Click the button for counting"
        )
        ctrmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        view = fv.CounterView(client=self.bot)
        view.message = await ctx.send(embed=ctrmbed, view=view)

def setup(bot):
    bot.add_cog(Fun(bot))