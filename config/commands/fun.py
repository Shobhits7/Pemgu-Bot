import discord
from discord.ext import commands
from config.views.counter import CounterView

class Fun(commands.Cog, description="For people who can't go out because vidcon-19"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="counter", aliases="ctr", help="Will start an counter")
    async def counter(self, ctx):
        await ctx.trigger_typing()
        ctrmbed = discord.Embed(
            colour=self.bot.color,
            title="Click the button for counting"
        )
        await ctx.send(embed=ctrmbed, view=CounterView(client=self.bot))

def setup(bot):
    bot.add_cog(Fun(bot))