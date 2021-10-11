import discord
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        welcome = await self.bot.postgres.fetchval("SELECT * FROM welcome WHERE guild_id=$1", member.guild.id)
        if welcome:
            msg = await self.bot.postgres.fetchval("SELECT msg FROM welcome WHERE guild_id=$1", member.guild.id)
            mi = [
                F"***Username:*** {member.name}",
                F"***Discriminator:*** {member.discriminator}",
                F"***ID:*** {member.id}",
                F"***Mention:*** {member.mention}",
                F"***Registered:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})"
            ]
            omjmbed = discord.Embed(
                colour=self.bot.colour,
                title="A new member has appeared",
                description="\n".join(m for m in mi),
                timestamp=discord.utils.utcnow()
            )
            omjmbed.set_author(name=member.guild.name, icon_url=member.guild.icon.url)
            omjmbed.set_image(url=member.display_avatar.url)
            omjmbed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await member.guild.system_channel.send(content=F"Welcome to {member.guild.name} {member.mention}" if not msg else msg, embed=omjmbed)

def setup(bot):
    bot.add_cog(Member(bot))