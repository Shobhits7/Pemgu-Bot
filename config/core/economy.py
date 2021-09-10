import discord
from discord.ext import commands

class Economy(commands.Cog, description="People who gamble"):
    def __init__(self, bot):
        self.bot = bot

    # Economy
    @commands.group(name="economy", help="Will tell you, your economy money", invoke_without_command=True)
    async def economy(self, ctx):
        await ctx.trigger_typing()
        await ctx.send("IN DEVELOPMENT")

def setup(bot):
    bot.add_cog(Economy(bot))