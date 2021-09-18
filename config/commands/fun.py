import discord
from discord.ext import commands
from config.views import counter

class Fun(commands.Cog, description="For just having an great fun time"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="counter", aliases=["ctr"], help="Will start an counter")
    @commands.is_owner()
    async def counter(self, ctx):
        await ctx.trigger_typing()
        ctrmbed = discord.Embed(
            colour=self.bot.color,
            title="Click the button for counting"
        )
        ctrmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        view = counter.CounterView(client=self.bot)
        view.message = await ctx.send(embed=ctrmbed, view=view)

def setup(bot):
    bot.add_cog(Fun(bot))