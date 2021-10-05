import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if F"<@!{self.bot.user.id}>" in message.content:
            prefix = await self.bot.postgres.fetch("SELECT prefix FROM prefixes WHERE guild_id=$1", message.guild.id)
            pfmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"My Prefix here is:",
                description=F"> {self.bot.prefix if not prefix else prefix}",
                timestamp=message.created_at
            )
            pfmbed.set_footer(text=message.author, icon_url=message.author.display_avatar.url)
            await message.send(embed=pfmbed)

def setup(bot):
    bot.add_cog(OnMessage(bot))