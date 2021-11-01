import discord, time, inspect, os, io, typing
from discord.ext import commands

class Information(commands.Cog, description="Stalking people is wrong and bad!"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {"Authorization": os.getenv("DAGPI")}

    # About
    @commands.command(name="about", aliases=["ab"], help="Will show the bot's information")
    async def about(self, ctx:commands.Context):
        ai = [
            F"[Source Code](https://github.com/lvlahraam/Pemgu-Bot)",
            F"[Invite]({discord.utils.oauth_url(client_id=self.bot.user.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))})",
            "[Support](https://discord.gg/Gw9wjvusQX)",
            F"[Top.gg](https://top.gg/bot/{self.bot.user.id})",
            F"Discord.PY Version {discord.__version__}",
            F"In {len(self.bot.guilds)} Servers",
            F"Has {len(self.bot.commands)} Commands",
            F"Made by <@{self.bot.owner_id}>"
        ]
        abmbed = discord.Embed(
            color=self.bot.color,
            title=F"{self.bot.user.name} About",
            description="\n".join(a for a in ai),
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=abmbed)

    # Uptime
    @commands.command(name="uptime", aliases=["up"], help="Will the bot's uptime")
    async def uptime(self, ctx:commands.Context):
        upmbed = discord.Embed(
            color=self.bot.color,
            description=F"Uptime: {discord.utils.format_dt(self.bot.uptime, style='f')} ({discord.utils.format_dt(self.bot.uptime, style='R')})",
            timestamp=ctx.message.created_at
        )
        upmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=upmbed)

    # ServerList
    @commands.command(name="serverlist", aliases=["sl"], help="Will give the list of bot's servers")
    async def serverlist(self, ctx:commands.Context):
        si = []
        for guild in self.bot.guilds:
            si.append(F"{guild.name} - {guild.id} | {guild.owner.mention} {guild.owner.name}#{guild.owner.discriminator}")
        sis = "\n".join(s for s in si)
        slmbed = discord.Embed(
            color=self.bot.color,
            title=F"Bot's Servers {len(self.bot.guilds)}",
            description=self.bot.trim(sis, 603),
            timestamp=ctx.message.created_at
        )
        slmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=slmbed)

    # Invite
    @commands.command(name="invite", aliases=["ie"], help="Will make an invite link for the bot or the given bot")
    async def invite(self, ctx:commands.Context, bot:discord.Member=None):
        bot = self.bot.user if not bot else bot
        iembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        iembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if not bot.bot:
            iembed.title = "The given user is not a bot"
            return await ctx.send(embed=iembed)
        link = discord.utils.oauth_url(client_id=bot.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions.all())
        iembed.url = link
        ggurl = F"https://top.gg/bot/{bot.id}"
        session = await self.bot.session.get(ggurl)
        if session.status != 404:
            iembed.description = F"[Top.gg]({ggurl})"
        iembed.title = F"Here is the invite link for adding the {bot}"
        await ctx.send(embed=iembed)

    # Ping
    @commands.command(name="ping", aliases=["pi"], help="Will show bot's ping")
    async def ping(self, ctx:commands.Context):
        unpimbed = discord.Embed(
            color=self.bot.color,
            title="🎾 Pinging...",
            timestamp=ctx.message.created_at
        )
        unpimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        tstart = time.perf_counter()
        unpimsg = await ctx.send(embed=unpimbed)
        tend = time.perf_counter()
        pstart = time.perf_counter()
        await self.bot.postgres.fetch("SELECT 1")
        pend = time.perf_counter()
        dopimbed = discord.Embed(
            color=self.bot.color,
            title="🏓 Pong:",
            description=F"Websocket: {self.bot.latency*1000}ms\nTyping: {(tend-tstart)*1000}ms\nPostgres: {(pend-pstart)*1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await unpimsg.edit(embed=dopimbed)

    # Source
    @commands.command(name="source", aliases=["src"], help="Will show the bots source")
    async def source(self, ctx:commands.Context, command:str=None):
        srcmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        srcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        prefix = ctx.clean_prefix
        source_url = 'https://github.com/lvlahraam/Pemgu-Bot'
        if command is None:
            srcmbed.title = F"Click here for the source code of this bot"
            srcmbed.url = source_url
            return await ctx.send(embed=srcmbed)
        if command == 'help':
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace('.', ' '))
            if obj is None:
                srcmbed.url = source_url
                srcmbed.title = F"Click here for the source code of this bot"
                srcmbed.description = "I couldn't find that command"
                return await ctx.send(embed=srcmbed)
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename
        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith('discord'):
            location = os.path.relpath(filename).replace('\\', '/')
        else:
            location = module.replace('.', '/') + '.py'
            source_url = 'https://github.com/Rapptz/discord.py'
            branch = 'master'
        final_url = f'{source_url}/tree/main/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}'
        srcmbed.url = final_url
        srcmbed.title = F"Click here for the source code of the `{prefix}{command}` command"
        srcmbed.set_footer(text=f"{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}\n{ctx.author}", icon_url=ctx.author.display_avatar)
        await ctx.send(embed=srcmbed)

    # Color
    @commands.command(name="color", aliases=["clr"], help="Will give info about the given color")
    async def color(self, ctx:commands.Context, *, color:discord.Color):
        hex_color = str(color)[1:] if "#" in str(color) else str(color)
        session = await self.bot.session.get(F"https://api.alexflipnote.dev/color/{hex_color}")
        if session.status != 200:
            raise commands.BadColorArgument
        response = await session.json()
        session.close()
        clrmbed = discord.Embed(
            color=color,
            title=F"Information about: {response.get('name')}",
            description=F"**HEX:** {response.get('hex')}\n**RGB:** {response.get('rgb')[4:-2]}\n**Int:** {response.get('int')}\n**Brightness:** {response.get('brightness')}",
            timestamp=ctx.message.created_at
        )
        clrmbed.set_thumbnail(url=response.get("image"))
        clrmbed.set_image(url=response.get("image_gradient"))
        clrmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=clrmbed)

    # Colors
    @commands.command(name="colors", aliases=["clrs"], help="Will give you the colors from the given image")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def colors(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/colors/?url={user.avatar.with_format('png')}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        clrsmbed = discord.Embed(
            color=self.bot.color,
            title=F"{user}'s image colors",
            timestamp=ctx.message.created_at
        )
        clrsmbed.set_image(url="attachment://colors.png")
        clrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(fp=response, filename="colors.png"), embed=clrsmbed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another user's avatar")
    async def avatar(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        avmbed = discord.Embed(
            color=self.bot.color,
            title=F"{user}'s Avatar",
            timestamp=ctx.message.created_at
        )
        avmbed.set_image(url=user.display_avatar.url)
        avmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=avmbed)

    # Banner
    @commands.command(name="banner", aliases=["br"], help="Will show your or another user's banner")
    async def banner(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        fetch = await self.bot.fetch_user(user.id)
        brmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        brmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if fetch.banner:
            brmbed.title = F"{user}'s Banner"
            brmbed.set_image(url=fetch.banner.url)
        else: brmbed.title = F"{user} doesn't have banner"
        await ctx.send(embed=brmbed)

    # UserInfo
    @commands.command(name="userinfo", aliases=["ui"], help="Will show user info")
    @commands.guild_only()
    async def userinfo(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        fetch = await self.bot.fetch_user(member.id)
        gi = [
            F"***Username:*** {member.name}",
            F"***Discriminator:*** {member.discriminator}",
            F"***ID:*** {member.id}",
            F"***Mention:*** {member.mention}",
            F"***Activity:*** {'*Nothing*' if not member.activity else member.activity.name}",
            F"***Status:*** {member.status}",
            F"***Web-Status:*** {member.web_status}",
            F"***Desktop-Status:*** {member.desktop_status}",
            F"***Mobile-Status:*** {member.mobile_status}",
            F"***Registered:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})"
        ]
        si = [
            F"***Joined:*** {discord.utils.format_dt(member.joined_at, style='F')} ({discord.utils.format_dt(member.joined_at, style='R')})",
            F"***Roles:*** [{len(member.roles)}]",
            F"***Top-Role:*** {member.top_role.mention}",
            F"***Boosting:*** {'True' if member in ctx.guild.premium_subscribers else 'False'}",
            F"***Nickname:*** {member.nick}",
            F"***Voice:*** {'*Not in a voice*' if not member.voice else member.voice.channel.mention}"
        ]
        uimbed = discord.Embed(
            color=self.bot.color if not fetch.accent_color else fetch.accent_color,
            title=F"{member}'s' Information",
            timestamp=ctx.message.created_at
        )
        uimbed.add_field(name="Global-Information:", value="\n".join(g for g in gi), inline=False)
        uimbed.add_field(name="Server-Information:", value="\n".join(s for s in si), inline=False)
        if member.guild_avatar: uimbed.set_thumbnail(url=member.guild_avatar.url)
        if fetch.banner: uimbed.set_image(url=fetch.banner.url)
        uimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=uimbed)

    # Permissions
    @commands.command(name="permissions", aliases=["perms"], help="Will show your or the given member's permissions")
    @commands.guild_only()
    async def permissions(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        ai = []
        di = []
        for permission, value in member.guild_permissions:
            permission = permission.replace("_", " ").title()
            if value:
                ai.append(permission)
            if not value:
                di.append(permission)
        permsmbed = discord.Embed(
            color=self.bot.color,
            title=F"{member}'s Permissions",
            timestamp=ctx.message.created_at
        )
        permsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if len(ai) != 0:
            permsmbed.add_field(name="✅ Allowed:", value="\n".join(a for a in ai))
        if len(di) != 0:
            permsmbed.add_field(name="❎ Denied:", value="\n".join(d for d in di))
        await ctx.send(embed=permsmbed)

    # Spotify
    @commands.command(name="spotify", aliases=["sy"], help="Will show your or the given member's spotify activity")
    async def spotify(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        spotifymbed = discord.Embed(
            timestamp=ctx.message.created_at
        )
        spotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                si = [
                    F"**Artists:** {', '.join(artist for artist in activity.artists)}",
                    F"**Album:** {activity.album}",
                    F"**Duration:** {time.strftime('%H:%M:%S', time.gmtime(activity.duration.total_seconds()))}",
                    F"**Track-ID:** {activity.track_id}",
                    F"**Party-ID:** {activity.party_id}",
                    F"**Listening-Since:** {discord.utils.format_dt(activity.created_at, style='f')} ({discord.utils.format_dt(activity.created_at, style='R')})"
                ]
                spotifymbed.color = activity.color
                spotifymbed.url = activity.track_url
                spotifymbed.title = activity.title
                spotifymbed.description = "\n".join(s for s in si)
                spotifymbed.set_author(name=member, icon_url=member.display_avatar.url)
                spotifymbed.set_thumbnail(url=activity.album_cover_url)
                await ctx.send(embed=spotifymbed)
                break
        else:
            spotifymbed.color = self.bot.color
            spotifymbed.title = F"{member} is not listening to Spotify"
            await ctx.send(embed=spotifymbed)

    # Icon
    @commands.command(name="icon", aliases=["ic"], help="Will show the server's icon")
    @commands.guild_only()
    async def icon(self, ctx:commands.Context):
        icmbed = discord.Embed(
            color=self.bot.color,
            title=F"{ctx.guild}'s Icon",
            timestamp=ctx.message.created_at
        )
        icmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if ctx.guild.icon:
            icmbed.set_thumbnail(url=ctx.guild.icon.url)
        else: icmbed.title = F"{ctx.guild.name} doesn't have icon"
        await ctx.send(embed=icmbed)

    # ServerInfo
    @commands.command(name="serverinfo", aliases=["si"], help="Will show the server's info")
    @commands.guild_only()
    async def serverinfo(self, ctx:commands.Context):
        oi = [
            F"***Username:*** {ctx.guild.owner.name}",
            F"***Discriminator:*** {ctx.guild.owner.discriminator}",
            F"***ID:*** {ctx.guild.owner.id}",
            F"***Mention:*** {ctx.guild.owner.mention}",
            F"***Registered:*** {discord.utils.format_dt(ctx.guild.owner.created_at, style='F')} ({discord.utils.format_dt(ctx.guild.owner.created_at, style='R')})"
        ]
        si = [
            F"***Name:*** {ctx.guild.name}",
            F"***ID:*** {ctx.guild.id}",
            F"***Description:*** {'*No Description*' if not ctx.guild.description else ctx.guild.description}",
            F"***Created-At:*** {discord.utils.format_dt(ctx.guild.created_at, style='F')} ({discord.utils.format_dt(ctx.guild.created_at, style='R')})",
            F"***Region:*** {ctx.guild.region}",
            F"***MFA:*** {ctx.guild.mfa_level}",
            F"***Verification:*** {ctx.guild.verification_level}",
            F"***File-Size-Limit:*** {ctx.guild.filesize_limit}",
            F"***Members:*** {ctx.guild.member_count}",
            F"***Default-Role:*** {ctx.guild.default_role.mention}",
            F"***Boost-Role:*** {'*No boost-role*' if not ctx.guild.premium_subscriber_role else ctx.guild.premium_subscriber_role.mention}",
            F"***Boost-Level:*** {ctx.guild.premium_tier}",
            F"***Boosters:*** {', '.join(self.bot.trim(booster.name, 20) for booster in ctx.guild.premium_subscribers)}",
            F"***Categories:*** {len(ctx.guild.categories)}",
            F"***Channels:*** {len(ctx.guild.channels)}",
            F"***AFK-Channel:*** {'*No AFK channel*' if not ctx.guild.afk_channel else ctx.guild.afk_channel.mention}",
            F"***AFK-Timeout:*** {ctx.guild.afk_timeout}"
        ]
        simbed = discord.Embed(
            color=self.bot.color,
            title=F"{ctx.guild.name}'s Information",
            timestamp=ctx.message.created_at
        )
        simbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        simbed.add_field(name="Owner-Information:", value="\n".join(o for o in oi), inline=False)
        simbed.add_field(name="Server-Information:", value="\n".join(s for s in si), inline=False)
        if ctx.guild.icon: simbed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner: simbed.set_image(url=ctx.guild.banner.url)
        await ctx.send(embed=simbed)

    # EmojiInfo
    @commands.command(name="emojiinfo", aliases=["ei"], help="Will give information about the given emoji")
    @commands.guild_only()
    async def emojiinfo(self, ctx:commands.Context, emoji:typing.Union[discord.Emoji, discord.PartialEmoji]):
        ei = [
            F"***Name:*** {emoji.name}",
            F"***ID:*** {emoji.id}",
            F"***Animated:*** {emoji.animated}",
            F"***Requires-Colons:*** {emoji.require_colons}",
            F"***Available:*** {emoji.available}",
            F"***Twitch:*** {emoji.managed}",
            F"***Created-At:*** {discord.utils.format_dt(emoji.created_at)}"
        ]
        emmbed = discord.Embed(
            color=self.bot.color,
            title=F"{emoji.name}'s Information",
            description="\n".join(e for e in ei),
            timestamp=ctx.message.created_at
        )
        emmbed.set_image(url=emoji.url)
        emmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=emmbed)

def setup(bot):
    bot.add_cog(Information(bot))