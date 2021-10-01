import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if message.author.id == 770646750804312105:
            return await message.channel.send("FUCK OFF LOSER")
        if F"<@!{self.bot.user.id}>" == message.content or F"<@{self.bot.user.id}>" == message.content:
            ompmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"My Prefix here is '{self.bot.prefix}'",
                timestamp=message.created_at
            )
            ompmbed.set_footer(text=message.author, icon_url=message.author.display_avatar.url)
            return await message.channel.send(embed=ompmbed)

def setup(bot):
    bot.add_cog(OnMessage(bot))
