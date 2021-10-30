import discord
from discord.ext import commands

class OnConnect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.uptime = discord.utils.utcnow()
        oni = [
            F"Logged in as: {self.bot.user} - {self.bot.user.id}",
            F"Main prefix is: {self.bot.default_prefix}",
            F"Servers bot is in: {len(self.bot.guilds)}",
            "The Bot is online now"
        ]
        print("\n".join(o for o in oni))
        await self.bot.change_presence(activity=discord.Game(name=F"@{self.bot.user.name} for prefix | {self.bot.default_prefix} help for help"), status=discord.Status.do_not_disturb)

def setup(bot):
    bot.add_cog(OnConnect(bot))