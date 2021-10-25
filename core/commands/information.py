import discord, time, inspect, os, io
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
            F"Discord.PY Version {discord.__version__}",
            F"In {len(self.bot.guilds)} Servers",
            F"Has {len(self.bot.commands)} Commands",
            F"Made by <@{self.bot.owner_id}>"
        ]
        abmbed = discord.Embed(
            color=self.bot.color,
            title=F"{self.bot.user.name} About",
            description="> \n".join(a for a in ai),
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=abmbed)

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
            description=self.bot.trim(sis, 600),
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
        iembed.title = F"Here is the invite link for adding the {bot}"
        iembed.url = link
        ggurl = F"https://top.gg/bot/{bot.id}"
        session = await self.bot.session.get(ggurl)
        if session.status != 404:
            iembed.description = F"[Top.gg]({url})"
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
        start = time.perf_counter()
        unpimsg = await ctx.send(embed=unpimbed)
        end = time.perf_counter()
        dopimbed = discord.Embed(
            color=self.bot.color,
            title="🏓 Pong:",
            description=F"> Websocket: {self.bot.latency * 1000}ms\nTyping: {(end - start) * 1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await unpimsg.edit(embed=dopimbed)

    # Source
    @commands.command(name="source", aliases=["src"], help="Will show the bots source")
    async def source(self, ctx:commands.Context, command:str=None):
        source_url = "https://github.com/lvlahraam/Pemgu-Bot"
        if not command:
            return await ctx.send(source_url)
        if command == "help":
            src = type(self.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = self.bot.get_command(command.replace(".", " "))
            if not obj:
                return await ctx.send("Could not find command.")
            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename
        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"
            source_url = "https://github.com/lvlahraam/Pemgu-Bot"
        final_url = F"<{source_url}/blob/main/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        await ctx.send(final_url)

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
        if fetch.banner:
            brmbed.title = F"{user}'s Banner"
            brmbed.set_image(url=fetch.banner.url)
        else: brmbed.title = F"{user} doesn't have banner"
        brmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=brmbed)

    # UserInfo
    @commands.command(name="userinfo", aliases=["ui"], help="Will show user info")
    @commands.guild_only()
    async def userinfo(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        fetch = await self.bot.fetch_user(member.id)
        gi = [
            F"ᓚ***Username:*** {member.name}",
            F"ᓚ***Discriminator:*** {member.discriminator}",
            F"ᓚ***ID:*** {member.id}",
            F"ᓚ***Mention:*** {member.mention}",
            F"ᓚ***Badges:*** {', '.join([flag.replace('_', '').title() for flag, enabled in member.public_flags if enabled])}",
            F"ᓚ***Activity:*** {'*Nothing*' if not member.activity else member.activity.name}",
            F"ᓚ***Status:*** {member.status}",
            F"ᓚ***Web-Status:*** {member.web_status}",
            F"ᓚ***Desktop-Status:*** {member.desktop_status}",
            F"ᓚ***Mobile-Status:*** {member.mobile_status}",
            F"ᓚ***Registered:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})"
        ]
        si = [
            F"ᓚ***Joined:*** {discord.utils.format_dt(member.joined_at, style='F')} ({discord.utils.format_dt(member.joined_at, style='R')})",
            F"ᓚ***Roles:*** [{len(member.roles)}]",
            F"ᓚ***Top-Role:*** {member.top_role.mention}",
            F"ᓚ***Boosting:*** {'True' if member in ctx.guild.premium_subscribers else 'False'}",
            F"ᓚ***Nickname:*** {member.nick}",
            F"ᓚ***Voice:*** {'*Not in a voice*' if not member.voice else member.voice.channel.mention}"
        ]
        uimbed = discord.Embed(
            color=self.bot.color if not fetch.accent_color else fetch.accent_color,
            title=F"{member}'s' Information",
            timestamp=ctx.message.created_at
        )
        uimbed.set_author(name=member, icon_url=member.display_avatar.url)
        uimbed.add_field(name="Global-Information:", value="\n".join(g for g in gi), inline=False)
        uimbed.add_field(name="Server-Information:", value="\n".join(s for s in si), inline=False)
        if member.guild_avatar: uimbed.set_thumbnail(url=member.guild_avatar.url)
        if fetch.banner: uimbed.set_image(url=fetch.banner.url)
        uimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=uimbed)

    # Spotify
    @commands.command(name="spotify", help="Will show your or the given member's spotify activity")
    async def spotify(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        spotifymbed = discord.Embed(
            timestamp=ctx.message.created_at
        )
        spotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                si = [
                    F"ᓚ**Artists:** {', '.join(artist for artist in activity.artists)}",
                    F"ᓚ**Album:** {activity.album}",
                    F"ᓚ**Duration:** {time.strftime('%H:%M:%S', time.gmtime(activity.duration.total_seconds()))}",
                    F"ᓚ**Track-ID:** {activity.track_id}",
                    F"ᓚ**Party-ID:** {activity.party_id}",
                    F"ᓚ**Listening-Since:** {discord.utils.format_dt(activity.created_at, style='f')} ({discord.utils.format_dt(activity.created_at, style='R')})"
                ]
                spotifymbed.color = activity.color
                spotifymbed.url = activity.track_url
                spotifymbed.title = activity.title
                spotifymbed.description = "\n".join(s for s in si)
                spotifymbed.set_author(name=member, icon_url=member.display_avatar.url)
                spotifymbed.set_image(url=activity.album_cover_url)
                await ctx.send(embed=spotifymbed)
                break
        else:
            spotifymbed.color = self.bot.color
            spotifymbed.title = F"{member} is not listening to Spotify"
            await ctx.send(embed=spotifymbed)

    # Permissions
    @commands.command(name="permissions", aliases=["perms"], help="Will show your or the given member's permissions")
    async def permissions(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        ok_emote = "<:ko:896063337958350919>"
        allowed_emote = "<:ye:896062865071566898>"
        denied_emote = "<:no:896062993090084974>"
        permsmbed = discord.Embed(
            color=self.bot.color,
            title=F"{ok_emote} {member}'s Permissions",
            description="",
            timestamp=ctx.message.created_at
        )
        for permission, value in member.guild_permissions:
            permission = permission.replace("_", " ").title()
            if value:
                permsmbed.description += F"> {allowed_emote} - {permission}\n"
            if not value:
                permsmbed.description += F"> {denied_emote} - {permission}\n"
        permsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=permsmbed)

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
            F"ᓚ***Username:*** {ctx.guild.owner.name}",
            F"ᓚ***Discriminator:*** {ctx.guild.owner.discriminator}",
            F"ᓚ***ID:*** {ctx.guild.owner.id}",
            F"ᓚ***Mention:*** {ctx.guild.owner.mention}",
            F"ᓚ***Badges:*** {', '.join([flag.replace('_', ' ').title() for flag, enabled in ctx.guild.owner.public_flags if enabled])}",
            F"ᓚ***Registered:*** {discord.utils.format_dt(ctx.guild.owner.created_at, style='F')} ({discord.utils.format_dt(ctx.guild.owner.created_at, style='R')})"
        ]
        si = [
            F"ᓚ***Name:*** {ctx.guild.name}",
            F"ᓚ***ID:*** {ctx.guild.id}",
            F"ᓚ***Description:*** {'*No Description*' if not ctx.guild.description else ctx.guild.description}",
            F"ᓚ***Created-At:*** {discord.utils.format_dt(ctx.guild.created_at, style='F')} ({discord.utils.format_dt(ctx.guild.created_at, style='R')})",
            F"ᓚ***Region:*** {ctx.guild.region}",
            F"ᓚ***MFA:*** {ctx.guild.mfa_level}",
            F"ᓚ***Verification:*** {ctx.guild.verification_level}",
            F"ᓚ***File-Size-Limit:*** {ctx.guild.filesize_limit}",
            F"ᓚ***Members:*** {ctx.guild.member_count}",
            F"ᓚ***Default-Role:*** {ctx.guild.default_role.mention}",
            F"ᓚ***Boost-Role:*** {'*No boost-role*' if not ctx.guild.premium_subscriber_role else ctx.guild.premium_subscriber_role.mention}",
            F"ᓚ***Boosters:*** {ctx.guild.premium_subscription_count}",
            F"ᓚ***Tier:*** {ctx.guild.premium_tier}",
            F"ᓚ***Categories:*** {len(ctx.guild.categories)}",
            F"ᓚ***Channels:*** {len(ctx.guild.channels)}",
            F"ᓚ***AFK-Channel:*** {'*No AFK channel*' if not ctx.guild.afk_channel else ctx.guild.afk_channel.mention}",
            F"ᓚ***AFK-Timeout:*** {ctx.guild.afk_timeout}"
        ]
        simbed = discord.Embed(
            color=self.bot.color,
            title=F"{ctx.guild.name}'s Information",
            timestamp=ctx.message.created_at
        )
        simbed.add_field(name="Owner-Information:", value="\n".join(o for o in oi), inline=False)
        simbed.add_field(name="Server-Information:", value="\n".join(s for s in si), inline=False)
        if ctx.guild.icon: simbed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner: simbed.set_image(url=ctx.guild.banner.url)
        simbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=simbed)

    # EmojiInfo
    @commands.command(name="emojiinfo", aliases=["ei"], help="Will give information about the given emoji")
    async def emoji(self, ctx:commands.Context, emoji:discord.Emoji):
        ei = [
            F"ᓚ***Name:*** {emoji.name}",
            F"ᓚ***ID:*** {emoji.id}",
            F"ᓚ***Animated:*** {emoji.animated}",
            F"ᓚ***Requires-Colons:*** {emoji.require_colons}",
            F"ᓚ***Available:*** {emoji.available}",
            F"ᓚ***Twitch:*** {emoji.managed}",
            F"ᓚ***Created-At:*** {discord.utils.format_dt(emoji.created_at)}"
        ]
        emmbed = discord.Embed(
            color=self.bot.color,
            title=F"{emoji.name}'s Information",
            description="> \n".join(e for e in ei),
            timestamp=ctx.message.created_at
        )
        emmbed.set_image(url=emoji.url)
        emmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=emmbed)

    # PYPI
    @commands.command(name="pypi", help="Will give information about the given library in PYPI")
    async def pypi(self, ctx:commands.Context, *, library:str):
        pypimbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        pypimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        session = await self.bot.session.get(F"https://pypi.org/pypi/{library}/json")
        if session.status != 200:
            pypimbed.title = "Couldn't find that library in PYPI"
            return await ctx.send(embed=pypimbed)
        response = await session.json()
        session.close()
        pypimbed.url = response['info']['package_url'],
        pypimbed.title = response['info']['name'],
        pypimbed.description = response['info']['summary'],
        pi = [
            F"***Version:*** {response['info']['version']}",
            F"***Download URL:*** {response['info']['download_url']}",
            F"***Documentation URL:*** {response['info']['docs_url']}",
            F"***Home Page:*** {response['info']['home_page']}",
            F"***Yanked:*** {response['info']['yanked']} - {response['info']['yanked_reason']}",
            F"***Keywords:*** {response['info']['keywords']}",
            F"***License:*** {response['info']['license']}"
        ]
        pypimbed.add_field(name="Author Info:", value=F"Name: {response['info']['author']}\nEmail:{response['info']['author_email']}", inline=False)
        pypimbed.add_field(name="Package Info:", value="\n".join(p for p in pi), inline=False)
        pypimbed.add_field(name="Classifiers:", value=",\n    ".join(classifier for classifier in response['info']['classifiers']), inline=False)
        await ctx.send(embed=pypimbed)

def setup(bot):
    bot.add_cog(Information(bot))
