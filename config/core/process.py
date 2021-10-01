import discord
from discord.ext import commands
from config.utils.blacklist import users

class OnProcess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def process_commands(self, message:discord.Message):
        if message.author.bot or message.author.id in users:
            return
        ctx = await self.get_context(message, cls=commands.Context)
        await self.invoke(ctx)

def setup(bot):
    bot.add_cog(OnProcess(bot))