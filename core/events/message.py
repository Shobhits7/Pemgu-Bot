import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return

def setup(bot):
    bot.add_cog(OnMessage(bot))