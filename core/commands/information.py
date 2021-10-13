import discord, time, os, io, inspect
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
            "[Support](https://discord.gg/bWnjkjyFRz)",
            F"Discord.PY Version {discord.__version__}"
            F"In {len(self.bot.guilds)} Servers",
            F"Has {len(self.bot.commands)}",
            F"Owner is <@{self.bot.owner_id}>"
        ]
        abmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{self.bot.user.name} About",
            description="\n".join(a for a in ai),
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=abmbed)

    # Colours
    @commands.command(name="colours", aliases=["clrs"], help="Will give you the colours from the given image")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def colours(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/colors/?url={user.avatar.with_format('png')}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        clrsmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user}'s image colours",
            timestamp=ctx.message.created_at
        )
        clrsmbed.set_image(url="attachment://colours.png")
        clrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(fp=response, filename="colours.png"), embed=clrsmbed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another user's avatar")
    async def avatar(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        avmbed = discord.Embed(
            colour=self.bot.colour,
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
            colour=self.bot.colour,
            title=F"{user}'s Banner",
            timestamp=ctx.message.created_at
        )
        if fetch.banner: brmbed.set_image(url=fetch.banner.url)
        else: brmbed.description = "The user doesn't have a banner"
        brmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
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
            F"***Badges:*** {', '.join([flag.replace('_', '').title() for flag, enabled in member.public_flags if enabled])}",
            F"***Activity:*** {'*Nothing*' if not member.activity else member.activity.name}",
            F"***Status:*** {member.status}",
            F"***Web-Status:*** {member.web_status}",
            F"***Desktop-Status:*** {member.desktop_status}",
            F"***Mobile-Status:*** {member.mobile_status}",
            F"***Registered:*** {discord.utils.format_dt(member.created_at, style='F')} ({discord.utils.format_dt(member.created_at, style='R')})"
        ]
        si = [
            F"***Joined:*** {discord.utils.format_dt(member.joined_at, style='F')} ({discord.utils.format_dt(member.joined_at, style='R')})",
            F"***Roles [{len(member.roles)}]:*** {', '.join(role.mention for role in member.roles)}",
            F"***Top-Role:*** {member.top_role.mention}",
            F"***Boosting:*** {'True' if member in ctx.guild.premium_subscribers else 'False'}",
            F"***Nickname:*** {member.nick}",
            F"***Voice:*** {'*Not in a voice*' if not member.voice else member.voice.channel.mention}",
            F"***Server-Permissions:*** {', '.join([perm.replace('_', ' ').title() for perm, enabled in member.guild_permissions if enabled])}",
        ]
        uimbed = discord.Embed(
            colour=self.bot.colour if not fetch.accent_colour else fetch.accent_colour,
            title=F"{member}'s' Information",
            timestamp=ctx.message.created_at
        )
        uimbed.add_field(name="Global-Information:", value="\n".join(g for g in gi), inline=False)
        uimbed.add_field(name="Server-Information:", value="\n".join(s for s in si), inline=False)
        uimbed.set_author(name=member, icon_url=member.display_avatar.url)
        if member.guild_avatar: uimbed.set_thumbnail(url=member.guild_avatar.url)
        if fetch.banner: uimbed.set_image(url=fetch.banner.url)
        uimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=uimbed)

    # Spotify
    @commands.command(name="spotify", help="Will show your or the given member's spotify activity if possible")
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
                spotifymbed.colour = activity.colour
                spotifymbed.url = activity.track_url
                spotifymbed.title = activity.title
                spotifymbed.description = "\n".join(s for s in si)
                spotifymbed.set_author(name=member, icon_url=member.display_avatar.url)
                spotifymbed.set_image(url=activity.album_cover_url)
                await ctx.send(embed=spotifymbed)
                break
        else:
            spotifymbed.colour = self.bot.colour
            spotifymbed.title = F"{member} is not listening to Spotify"
            await ctx.send(embed=spotifymbed)

    # Icon
    @commands.command(name="icon", aliases=["ic"], help="Will show the server's icon")
    @commands.guild_only()
    async def icon(self, ctx:commands.Context):
        icmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{ctx.guild}'s Icon",
            timestamp=ctx.message.created_at
        )
        icmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if ctx.guild.icon: icmbed.set_thumbnail(url=ctx.guild.icon.url)
        else: icmbed.description = "__**Icon:**__ Server doesn't have a icon"
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
            F"***Badges:*** {', '.join([flag.replace('_', ' ').title() for flag, enabled in ctx.guild.owner.public_flags if enabled])}",
            F"***Registered:*** {discord.utils.format_dt(ctx.guild.owner.created_at, style='F')} ({discord.utils.format_dt(ctx.guild.owner.created_at, style='R')})"
        ]
        si = [
            F"***Name:*** {ctx.guild}",
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
            F"***Boosters:*** {ctx.guild.premium_subscription_count}",
            F"***Tier:*** {ctx.guild.premium_tier}",
            F"***Categories:*** {len(ctx.guild.categories)}",
            F"***Channels:*** {len(ctx.guild.channels)}",
            F"***AFK-Channel:*** {'*No AFK channel*' if not ctx.guild.afk_channel else ctx.guild.afk_channel.mention}",
            F"***AFK-Timeout:*** {ctx.guild.afk_timeout}"
        ]
        simbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{ctx.guild}'s Information",
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
            F"***Name:*** {emoji.name}",
            F"***ID:*** {emoji.id}",
            F"***Animated:*** {emoji.animated}",
            F"***Requires-Colons:*** {emoji.require_colons}",
            F"***Available:*** {emoji.available}",
            F"***Twitch:*** {emoji.managed}",
            F"***Created-At:*** {discord.utils.format_dt(emoji.created_at)}"
        ]
        emmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{emoji.name}'s Information",
            description="\n".join(e for e in ei),
            timestamp=ctx.message.created_at
        )
        emmbed.set_image(url=emoji.url)
        emmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=emmbed)

    # Ping
    @commands.command(name="ping", aliases=["pi"], help="Will show bot's ping")
    async def ping(self, ctx:commands.Context):
        unpimbed = discord.Embed(
            colour=self.bot.colour,
            title="🎾 Pinging...",
            timestamp=ctx.message.created_at
        )
        unpimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        start = time.perf_counter()
        unpimsg = await ctx.send(embed=unpimbed)
        end = time.perf_counter()
        dopimbed = discord.Embed(
            colour=self.bot.colour,
            title="🏓 Pong:",
            description=F"Websocket: {self.bot.latency * 1000}ms\nTyping: {(end - start) * 1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await unpimsg.edit(embed=dopimbed)

    # Permissions
    @commands.command(name="permissions", aliases=["perms"], help="Will show the permissions that the bot has in this guild")
    async def permissions(self, ctx:commands.Context):
        ok_emote = "<:fine:896063337958350919>"
        allowed_emote = "<:allow:896062865071566898>"
        denied_emote = "<:deny:896062993090084974>"
        permsmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{ok_emote} Bot Permissions",
            description="",
            timestamp=ctx.message.created_at
        )
        for permission, value in ctx.me.guild_permissions:
            permission = permission.replace("_", " ").title()
            if value:
                permsmbed.description += F"{allowed_emote} - {permission}\n"
            if not value:
                permsmbed.description += F"{denied_emote} - {permission}\n"
        permsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=permsmbed)

    # Invite
    @commands.command(name="invite", aliases=["ie"], help="Will make a send the link for adding  the bot")
    async def invite(self, ctx:commands.Context):
        iembed = discord.Embed(
            colour=self.bot.colour,
            title="Here is the invite link for adding the bot",
            url=discord.utils.oauth_url(client_id=self.bot.user.id, scopes=("bot", "applications.commands"), permissions=discord.Permissions(administrator=True)),
            description="Thank you for adding and inviting me!",
            timestamp=ctx.message.created_at
        )
        iembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=iembed)

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

    # RickAndMorty
    @commands.group(name="rickandmorty", aliases=["ram"], help="Some Rick and Morty commands, use subcommands", invoke_without_command=True)
    async def rickandmorty(self, ctx:commands.Context):
        await ctx.send_help(ctx.command.cog)

    # RickAndMorty-Character
    @rickandmorty.command(name="character", aliases=["char"], help="Will show information about the given character")
    async def character(self, ctx:commands.Context, *, character:str):
        session = await self.bot.session.get(F"https://rickandmortyapi.com/api/character/?name={character}")
        if session.status != 200:
            await ctx.send("Couldn't find that character in Rick And Morty")
            return
        response = await session.json()
        session.close()
        ci = [
            F"Stauts: {response['results'][0]['status']}",
            F"Species: {response['results'][0]['species']}",
            F"Type: {'Unknown' if not response['results'][0]['type'] else response['results'][0]['type']}",
            F"Gender: {response['results'][0]['gender']}",
            F"Origin: {response['results'][0]['origin']['name']}",
            F"Location: {response['results'][0]['location']['name']}",
            F"Created: {response['results'][0]['created']}"
        ]
        ramchmbed = discord.Embed(
            colour=self.bot.colour,
            url=response['results'][0]['url'],
            title=F"{response['results'][0]['name']}'s Information",
            description="\n".join(c for c in ci),
            timestamp=ctx.message.created_at,
        )
        ramchmbed.set_image(url=response['results'][0]['image'])
        await ctx.send(embed=ramchmbed)

    # RickAndMorty-Location
    @rickandmorty.command(name="location", aliases=["loc"], help="Will show information about the given location")
    async def location(self, ctx:commands.Context, *, location:str):
        session = await self.bot.session.get("...")
        response = await session.json()

    # RickAndMorty-Episode
    @rickandmorty.command(name="episode", aliases=["ep"], help="Will show information about the given episode")
    async def episode(self, ctx:commands.Context, *, episode:int):
        session = await self.bot.session.get("...")
        response = await session.json()

def setup(bot):
    bot.add_cog(Information(bot))