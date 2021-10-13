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
                colour=self.bot.colour,
                title=F"My Prefix here is:",
                description=F"> {self.bot.prefix if not prefix else prefix}",
                timestamp=message.created_at
            )
            pfmbed.set_footer(text=message.author, icon_url=message.author.display_avatar.url)
            await message.channel.send(embed=pfmbed)

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        self.bot.dmsgs.append(F"**{message.content}** - {message.author} | {discord.utils.format_dt(discord.utils.utcnow(), style='F')} ({discord.utils.format_dt(discord.utils.utcnow(), style='R')})")

    @commands.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        self.bot.emsgs.append(F"***Before:***\n**{before.content}** - {before.author}\n{discord.utils.format_dt(discord.utils.utcnow(), style='F')} ({discord.utils.format_dt(discord.utils.utcnow(), style='R')})\n***After:***\n**{after.content}** - {after.author}\n{discord.utils.format_dt(discord.utils.utcnow(), style='F')} ({discord.utils.format_dt(discord.utils.utcnow(), style='R')})")

def setup(bot):
    bot.add_cog(OnMessage(bot))