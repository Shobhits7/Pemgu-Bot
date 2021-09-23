import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if F"<@!{self.bot.user.id}>" == message.content or F"<@{self.bot.user.id}>" == message.content:
            prefix = await self.bot.postgresql.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
            if len(prefix) == 0:
                prefix = self.bot.prefix
            else:
                prefix = prefix[0].get("prefix")
            ompmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"My Prefix here is `{prefix}`",
                timestamp=message.created_at
            )
            ompmbed.set_footer(text=message.author, icon_url=message.author.avatar.url)
            return await message.channel.send(embed=ompmbed)

def setup(bot):
    bot.add_cog(OnMessage(bot))
