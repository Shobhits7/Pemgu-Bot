import discord
from discord.ext import commands
from config.utils.json import read_json, write_json

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if F"<@!{self.bot.user.id}>" == message.content or F"<@{self.bot.user.id}>" == message.content:
            self.bot.prefix
    
    @commands.Cog.listener()
    async def on_message_edit(self, old, new):
        await self.bot.process_commands(new)

def setup(bot):
    bot.add_cog(OnMessage(bot))
