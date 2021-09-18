import discord
from discord.ext import commands

class OnConnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print(F"---------------------------------------------------\nLogged in as: {self.bot.user} - {self.bot.user.id}\nMain prefix is: {self.bot.prefix}\nGuilds bot is in: {len(self.bot.guilds)}\nThe Bot is online now\n---------------------------------------------------")
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        await self.bot.aiosession.close()

def setup(bot):
    bot.add_cog(OnConnect(bot))
