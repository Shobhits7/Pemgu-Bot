import discord
from discord.ext import commands

class OnCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.bot_check_once()
    async def blacklist(self, ctx):
        if ctx.author.id in self.bot.blacklist_ids:
            return False
        return True

def setup(bot):
    bot.add_cog(OnCheck(bot))