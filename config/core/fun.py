import discord
from discord.ext import commands
import config.views.funview as vf

class Fun(commands.Cog, description="For just having an great fun time"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="counter", aliases=["ctr"], help="Will start an counter")
    async def counter(self, ctx):
        ctrmbed = discord.Embed(
            colour=self.bot.color,
            title="Click the button for counting"
        )
        ctrmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        view = vf.CounterView(client=self.bot)
        view.message = await ctx.send(embed=ctrmbed, view=view)

def setup(bot):
    bot.add_cog(Fun(bot))