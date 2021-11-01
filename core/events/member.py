import discord
from discord.ext import commands

class OnMember(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        if member.bot: return
        welcome = await self.bot.postgres.fetchval("SELECT * FROM welcome WHERE guild_id=$1", member.guild.id)
        if welcome:
            fetch = await self.bot.fetch_user(member.id)
            msg = await self.bot.postgres.fetchval("SELECT msg FROM welcome WHERE guild_id=$1", member.guild.id)
            msg = msg.replace(".guild", member.guild.name).replace(".member", member.mention)
            mi = [
                F"***Username:*** {member.name}",
                F"***Discriminator:*** {member.discriminator}",
                F"***ID:*** {member.id}",
                F"***Mention:*** {member.mention}",
                F"***Bot:*** {member.bot}",
                F"***Joined-At:*** {discord.utils.format_dt(member.joined_at, style='F')} ({discord.utils.format_dt(member.joined_at, style='R')})",
                F"***Created-At:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})",
                F"***Member-Count:*** {member.guild.member_count}"
            ]
            omjmbed = discord.Embed(
                color=self.bot.color if not fetch.accent_color else fetch.accent_color,
                title="A new member has appeared",
                description=msg,
                timestamp=discord.utils.utcnow()
            )
            omjmbed.set_thumbnail(url=member.display_avatar.url)
            if fetch.banner: omjmbed.set_image(url=fetch.banner.url)
            omjmbed.add_field(name="Information:", value="\n".join(m for m in mi))
            omjmbed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await member.guild.system_channel.send(embed=omjmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        if member.bot: return
        goodbye = await self.bot.postgres.fetchval("SELECT * FROM goodbye WHERE guild_id=$1", member.guild.id)
        if goodbye:
            fetch = await self.bot.fetch_user(member.id)
            msg = await self.bot.postgres.fetchval("SELECT msg FROM goodbye WHERE guild_id=$1", member.guild.id)
            msg = msg.replace(".guild", member.guild.name).replace(".member", member.mention)
            mi = [
                F"***Username:*** {member.name}",
                F"***Discriminator:*** {member.discriminator}",
                F"***ID:*** {member.id}",
                F"***Mention:*** {member.mention}",
                F"***Bot:*** {member.bot}",
                F"***Joined-At:*** {discord.utils.format_dt(member.joined_at, style='F')} ({discord.utils.format_dt(member.joined_at, style='R')})",
                F"***Created-At:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})",
                F"***Member-Count:*** {member.guild.member_count}"
            ]
            omjmbed = discord.Embed(
                color=self.bot.color if not fetch.accent_color else fetch.accent_color,
                title="A member has been lost",
                description=msg,
                timestamp=discord.utils.utcnow()
            )
            omjmbed.set_thumbnail(url=member.display_avatar.url)
            if fetch.banner: omjmbed.set_image(url=fetch.banner.url)
            omjmbed.add_field(name="Information:", value="\n".join(m for m in mi))
            omjmbed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await member.guild.system_channel.send(embed=omjmbed)

def setup(bot):
    bot.add_cog(OnMember(bot))