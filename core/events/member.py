import discord
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        fetch = await self.bot.fetch_user(member.id)
        welcome = await self.bot.postgres.fetchval("SELECT * FROM welcome WHERE guild_id=$1", member.guild.id)
        if welcome:
            msg = await self.bot.postgres.fetchval("SELECT msg FROM welcome WHERE guild_id=$1", member.guild.id)
            msg = msg.replace(".guild", member.guild.name).replace(".member", member.mention)
            mi = [
                F"***Username:*** {member.name}",
                F"***Discriminator:*** {member.discriminator}",
                F"***ID:*** {member.id}",
                F"***Mention:*** {member.mention}",
                F"***Registered:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})"
            ]
            omjmbed = discord.Embed(
                colour=self.bot.colour if not fetch.accent_colour else fetch.accent_colour,
                title="A new member has appeared",
                description=msg,
                timestamp=discord.utils.utcnow()
            )
            omjmbed.set_thumbnail(url=member.display_avatar.url)
            if fetch.banner: omjmbed.set_image(url=fetch.banner.url)
            omjmbed.add_field(name="Information:", value="\n".join(m for m in mi))
            omjmbed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await member.guild.system_channel.send(embed=omjmbed)

def setup(bot):
    bot.add_cog(Member(bot))