import discord
from discord.ext import commands

class OnConnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_connect(self):
        print(F"---------------------------------------------------\nLogged in as: {self.bot.user} - {self.bot.user.id}\nMain prefix is: {self.bot.prefix}\nServers bot is in: {len(self.bot.guilds)}\nThe Bot is online now\n---------------------------------------------------")
        await self.bot.change_presence(activity=discord.Game(name=F"@{self.bot.user.name} for prefix | {self.bot.prefix} help for help"))

def setup(bot):
    bot.add_cog(OnConnect(bot))