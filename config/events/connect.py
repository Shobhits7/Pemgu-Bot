import discord
from discord.ext import commands

class OnConnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_connect(self):
        print(F"---------------------------------------------------\nLogged in as: {self.user} - {self.user.id}\nMain prefix is: {self.prefix}\nGuilds bot is in: {len(self.guilds)}\nThe Bot is online now\n---------------------------------------------------")
        await self.change_presence(activity=discord.Game(name=F"@{self.user.name} for prefix | {self.prefix} help for help"))

def setup(bot):
    bot.add_cog(OnConnect(bot))