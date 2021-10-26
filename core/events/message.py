import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if message.content in (F"<@{self.bot.user.id}>", F"<@!{self.bot.user.id}>"):
            prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", message.guild.id)
            pfmbed = discord.Embed(
                color=self.bot.color,
                title=F"My Prefix here is:",
                description=F"> {self.bot.prefix if not prefix else prefix}",
                timestamp=message.created_at
            )
            pfmbed.set_footer(text=message.author, icon_url=message.author.display_avatar.url)
            await message.channel.send(embed=pfmbed)
        if self.bot.afks.get(message.author.id):
            omafkmbed = discord.Embed(
                color=self.bot.color,
                title="Removed your AFK",
                description=F"> Reason: **{self.bot.afks[message.author.id]['reason']}**\n> Since: **{discord.utils.format_dt(self.bot.afks[message.author.id]['time'], style='R')}**",
                timestamp=message.created_at
            )
            await message.channel.send(embed=omafkmbed)
            del self.bot.afks[message.author.id]

def setup(bot):
    bot.add_cog(OnMessage(bot))