import discord
from discord.ext import commands

class whoistest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.command()
    async def whoistest(self, ctx, member : discord.Member=None):
        '''
        Shows Breif Detailed Whois of Member
        '''
        if member == None:
            member = ctx.author

        fetchedMember = await self.client.fetch_user(member.id)

        if member.bot == True:
            botText = "<:toggle_on:876407676513443871>"
        else:
            botText = "<:toggle_off:876407718322245752>"

        if member.premium_since == None:
            premiumText = "Not Boosting"
        else:
            premiumText = f"{discord.utils.format_dt(member.premium_since, style='f')} ({discord.utils.format_dt(member.premium_since, style='R')})"

        if str(member.status).title() == "Online":
            statusEmote = "<:status_online:596576749790429200>"
        elif str(member.status).title() == "Idle":
            statusEmote = "<:status_idle:596576773488115722>"
        elif str(member.status).title() == "Dnd":
            statusEmote = "<:status_dnd:596576774364856321>"
        elif str(member.status).title() == "Streaming":
            statusEmote = "<:status_streaming:596576747294818305>"
        else:
            statusEmote = "<:status_offline:596576752013279242>"

        roles = ""
        for role in member.roles:
            if role is ctx.guild.default_role: continue
            roles = f"{roles} {role.mention}"
        if roles != "":
            roles = f"{roles}"

        if member.avatar.is_animated() == True:
            text1 = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) | [JPG]({member.avatar.replace(format='jpg', size=2048).url}) | [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) | [WEBP]({member.avatar.replace(format='webp', size=2048).url}) | [GIF]({member.avatar.replace(format='gif', size=2048).url})"
            avatar = text1.replace("cdn.discordapp.com", "media.discordapp.net")
        else:
            text1 = f"[PNG]({member.avatar.replace(format='png', size=2048).url}) | [JPG]({member.avatar.replace(format='jpg', size=2048).url}) | [JPEG]({member.avatar.replace(format='jpeg', size=2048).url}) | [WEBP]({member.avatar.replace(format='webp', size=2048).url})"
            avatar = text1.replace("cdn.discordapp.com", "media.discordapp.net")

        fetchedMember = await self.client.fetch_user(member.id)

        if fetchedMember.banner:
            if fetchedMember.banner.is_animated() == True:
                text1 = f"[PNG]({fetchedMember.banner.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) **|** [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url}) | [GIF]({fetchedMember.banner.replace(format='gif', size=2048).url})"
                banner = text1.replace("cdn.discordapp.com", "media.discordapp.net")
            else:
                text1 = f"[PNG]({fetchedMember.avatar.replace(format='png', size=2048).url}) | [JPG]({fetchedMember.banner.replace(format='jpg', size=2048).url}) | [JPEG]({fetchedMember.banner.replace(format='jpeg', size=2048).url}) | [WEBP]({fetchedMember.banner.replace(format='webp', size=2048).url})"
                banner = text1.replace("cdn.discordapp.com", "media.discordapp.net")
        else:
            banner = "banner not found"

        guild = ctx.guild

        desktopStatus = ":desktop: <:redTick:596576672149667840>"
        webStatus = ":globe_with_meridians: <:redTick:596576672149667840>"
        mobileStatus = ":mobile_phone:  <:redTick:596576672149667840>"

        if str(member.desktop_status) == "online" or str(member.desktop_status) == "idle" or str(member.desktop_status) == "dnd" or str(member.desktop_status) == "streaming":
            desktopStatus = ":desktop: <:greenTick:596576670815879169>"

        if str(member.web_status) == "online" or str(member.web_status) == "idle" or str(member.web_status) == "dnd" or str(member.web_status) == "streaming":
            webStatus = ":globe_with_meridians: <:greenTick:596576670815879169>"

        if str(member.mobile_status) == "online" or str(member.mobile_status) == "idle" or str(member.mobile_status) == "dnd" or str(member.mobile_status) == "streaming":
            mobileStatus = "<:mobile:886311078949167174> <:greenTick:596576670815879169>"


        joined = sorted(ctx.guild.members, key=lambda mem: mem.joined_at)
        pos = joined.index(member)
        positions = []
        for i in range(-3, 4):
            line_pos = pos + i
            if line_pos < 0:
                continue
            if line_pos >= len(joined):
                break
            positions.append("{0:<4}{1}{2:<20}".format(str(line_pos + 1) + ".", " " * 4 + ("->" if joined[line_pos] == member else " "), str(joined[line_pos])))
        join_seq = "{}".format("\n".join(positions))

        members = [*sorted(ctx.guild.members, key=lambda m: m.joined_at)]
        x = members.index(ctx.author)
        join_pos = "\n".join(map(str, members[x - 3: x + 3]))

        embed = discord.Embed(title=f"{member}", url=f"https://discord.com/users/{member.id}", description=f"""
\U0001f4db Nickname: {member.nick}
<:gtextchannel:876408281290117130>: Discriminator:  {member.discriminator}
<a:mention:886307604811366410> Mention: {member.mention}
<:greenTick:858439706827685918> Member ID: {member.id}
<:toggle_on:876407676513443871> Created: {discord.utils.format_dt(member.created_at, style="f")} ({discord.utils.format_dt(member.created_at, style="R")})
<:toggle_on:876407676513443871> Joined: {discord.utils.format_dt(member.joined_at, style="f")} ({discord.utils.format_dt(member.joined_at, style="R")})
:robot: Bot?: {botText}
<a:boosting:886308446968881222> Boosting: {premiumText}
<:idle:886311520374497320> Current status: {str(member.status).title()}
:video_game: Current activity: {str(member.activity.type).split('.')[-1].title() if member.activity else 'Not playing'} {member.activity.name if member.activity else ''}
<a:discord:886308080260894751> Client: {desktopStatus} **|** {webStatus} **|** {mobileStatus}
<:greactionrole:876407797569433600> Top Role: {member.top_role.mention}
<:greactionrole:876407797569433600> Roles: {roles}
:rainbow: Top Role Color: {member.color}
:rainbow: Member Accent color: {fetchedMember.accent_color}
Avatar: {avatar}
Banner: {banner}
> Joined at Position!
```diff
{join_seq}
```
        """, timestamp=discord.utils.utcnow(), color=0x2F3136)
        embed.set_thumbnail(url=member.avatar.url)
        if fetchedMember.banner:
            embed.set_image(url=fetchedMember.banner.url)
        query = member.id
        await ctx.replsend(embed=embed)

def setup(bot):
    bot.add_cog(whoistest(bot))
