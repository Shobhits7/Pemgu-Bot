import discord
from discord.ext import commands, tasks

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        print(F"---------------------------------------------------\nLogged in as: {self.bot.user} - {self.bot.user.id}\nMain prefix is: ~b\nThe Bot  is online now\n---------------------------------------------------")

def setup(bot):
    bot.add_cog(OnReady(bot))
