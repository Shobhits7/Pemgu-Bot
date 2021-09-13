import discord
from discord.ext import commands

class OnReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(F"---------------------------------------------------\nLogged in as: {self.bot.user} - {self.bot.user.id}\nMain prefix is: {self.bot.prefix}\nGuilds bot is in: {len(self.bot.guilds)}\nThe Bot  is online now\n---------------------------------------------------")

def setup(bot):
    bot.add_cog(OnReady(bot))
