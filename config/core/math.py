import discord
from discord.ext import commands

class Math(commands.Cog, description="Cheating tests with these"):
    def __init__(self, bot):
        self.bot = bot
    
    # Sum
    @commands.command(name="sum", help="Will give the sum for the given 2 numbers", usage="<num1> <num2>")
    async def sum(self, ctx:commands.Context, num1:int, num2:int):
        await ctx.send(num1 + num2)

def setup(bot):
    bot.add_cog(Math(bot))