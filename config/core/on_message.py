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
            data = read_json("prefixes")
            if str(message.guild.id) in data:
                prefix = data[str(message.guild.id)]
            else:
                prefix = "~b"
            ompmbed = discord.Embed(
                colour=self.bot.color,
                title=F"My Prefix here is {prefix}",
                timestamp=message.created_at
            )
            ompmbed.set_footer(text=message.author.display_name, icon_url=message.author.avatar_url)
            return await message.send(embed=ompmbed)
        

def setup(bot):
    bot.add_cog(OnMessage(bot))
