import discord, time, os, io, typing
from discord.ext import commands

class Information(commands.Cog, description="Stalking people is wrong and bad!"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {"Authorization": os.getenv("DAGPI")}

    # About
    @commands.command(name="about", aliases=["ab"], help="Will show the bot's information")
    async def about(self, ctx:commands.Context):
        abmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{self.bot.user.name} About",
            description=F"[Click here for source code](https://github.com/lvlahraam/JakeTheDog-Bot)\n[Click here for Adding Bot]({discord.utils.oauth_url(client_id=self.bot.user.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))})\n[Click here for Joining Support](https://discord.gg/bWnjkjyFRz)\nIn {len(self.bot.guilds)} Servers\nHas {len(self.bot.commands)} Commands\nOwner is <@{self.bot.owner_id}>",
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
            title=F"{user} 's image colours",
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
        uimbed = discord.Embed(
            colour=self.bot.colour if not fetch.accent_colour else fetch.accent_colour,
            title=F"{member}'s' Information",
            timestamp=ctx.message.created_at
        )
        uimbed.description = F"""
        __**Global-Information:**__
        ***Username:*** {member.name}
        ***Discriminator:*** {member.discriminator}
        ***ID:*** {member.id}
        ***Mention:*** {member.mention}
        ***Badges:*** {', '.join([flag.replace("_", " ").title() for flag, enabled in member.public_flags if enabled])}
        ***Activity:*** {'*Nothing*' if not member.activity else member.activity.name}
        ***Status:*** {member.status}
        ***Web-Status:*** {member.web_status}
        ***Desktop-Status:*** {member.desktop_status}
        ***Mobile-Status:*** {member.mobile_status}
        ***Registered:*** {discord.utils.format_dt(member.created_at, style="F")} ({discord.utils.format_dt(member.created_at, style="R")})
        __**Server-Information:**__
        ***Joined:*** {discord.utils.format_dt(member.joined_at, style="F")} ({discord.utils.format_dt(member.joined_at, style="R")})
        ***Roles [{len(member.roles)}]:*** {', '.join(role.mention for role in member.roles)}
        ***Top-Role:*** {member.top_role.mention}
        ***Boosting:*** {'True' if member in ctx.guild.premium_subscribers else 'False'}
        ***Nickname:*** {member.nick}
        ***Voice:*** {'*Not in a voice*' if not member.voice else member.voice.channel.mention}
        ***Server-Permissions:*** {', '.join([perm.replace("_", " ").title() for perm, enabled in member.guild_permissions if enabled])}
        """.replace("\t", "")
        uimbed.set_author(name=member, icon_url=member.display_avatar.url)
        if member.guild_avatar: uimbed.set_thumbnail(url=member.guild_avatar.url)
        if fetch.banner: uimbed.set_image(url=fetch.banner.url)
        uimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=uimbed)

    # Spotify
    @commands.command(name="spotify", help="Will show your or the given member's spotify activity if possible")
    async def spotify(self, ctx:commands.Context, member:discord.Member=None):
        member = ctx.author if not member else member
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                fspotifymbed = discord.Embed(
                    colour=activity.colour,
                    url=activity.track_url,
                    title=activity.title,
                    timestamp=ctx.message.created_at
                )
                fspotifymbed.description = F"""
                **Artists:** {', '.join(artist for artist in activity.artists)}
                **Album:** {activity.album}
                **Duration:** {time.strftime("%H:%M:%S", time.gmtime(activity.duration.total_seconds()))}
                **Track-ID:** {activity.track_id}
                **Party-ID:** {activity.party_id}
                **Listening-Since:** {discord.utils.format_dt(activity.created_at, style='f')} ({discord.utils.format_dt(activity.created_at, style='R')})
                """.replace("\t\t", "")
                fspotifymbed.set_author(name=member, icon_url=member.display_avatar.url)
                fspotifymbed.set_image(url=activity.album_cover_url)
                fspotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=fspotifymbed)
                break
        else:
            badspotifymbed = discord.Embed(
                colour=self.bot.colour,
                title=F"{member} is not listenning to Spotify",
                timestamp=ctx.message.created_at
            )
            badspotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=badspotifymbed)

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
        simbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{ctx.guild}'s Information",
            timestamp=ctx.message.created_at
        )
        simbed.description = F"""
        __**Owner-Information:**__
        ***Username:*** {ctx.guild.owner.name}
        ***Discriminator:*** {ctx.guild.owner.discriminator}
        ***ID:*** {ctx.guild.owner.id}
        ***Mention:*** {ctx.guild.owner.mention}
        ***Badges:*** {', '.join([flag.replace("_", " ").title() for flag, enabled in ctx.guild.owner.public_flags if enabled])}
        ***Registered:*** {discord.utils.format_dt(ctx.guild.owner.created_at, style="F")} ({discord.utils.format_dt(ctx.guild.owner.created_at, style="R")})
        __**Server-Information:**__
        ***Name:*** {ctx.guild}
        ***ID:*** {ctx.guild.id}
        ***Description:*** {'*No Description*' if not ctx.guild.description else ctx.guild.description}
        ***Created-At:*** {discord.utils.format_dt(ctx.guild.created_at, style="F")} ({discord.utils.format_dt(ctx.guild.created_at, style="R")})
        ***Region:*** {ctx.guild.region}
        ***MFA:*** {ctx.guild.mfa_level}
        ***Verification:*** {ctx.guild.verification_level}
        ***File-Size-Limit:*** {ctx.guild.filesize_limit}
        ***Members:*** {ctx.guild.member_count}
        ***Default-Role:*** {ctx.guild.default_role.mention}
        ***Boost-Role:*** {'*No boost-role*' if not ctx.guild.premium_subscriber_role else ctx.guild.premium_subscriber_role.mention}
        ***Boosters:*** {ctx.guild.premium_subscription_count}
        ***Tier:*** {ctx.guild.premium_tier}
        ***Categories:*** {len(ctx.guild.categories)}
        ***Channels:*** {len(ctx.guild.channels)}
        ***AFK-Channel:*** {'*No AFK channel*' if not ctx.guild.afk_channel else ctx.guild.afk_channel.mention}
        ***AFK-Timeout:*** {ctx.guild.afk_timeout}
        """.replace("\t\t", "╰")
        if ctx.guild.icon: simbed.set_thumbnail(url=ctx.guild.icon.url)
        else: simbed.description += "__**Icon:**__ Server doesn't have a icon"
        if ctx.guild.banner: simbed.set_image(url=ctx.guild.banner.url)
        else: simbed.description += "__**Banner:**__ Server doesn't have a banner"
        simbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=simbed)

    # Emoji
    @commands.command(name="emoji", aliases=["em"], help="Will give information about the given emoji")
    async def emoji(self, ctx:commands.Context, emoji:typing.Union[discord.PartialEmoji, discord.Emoji]):
        emmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{emoji.name} 's Information",
            timestamp=ctx.message.created_at
        )
        emmbed.description = F"""
        ***Name:*** {emoji.name}
        ***ID:*** {emoji.id}
        ***Animated:*** {emoji.animated}
        ***Created-At*** {discord.utils.format_dt(emoji.created_at)}
        """.replace("\t", "")
        emmbed.set_image(url=emoji.url)
        emmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=emmbed)

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
        ramchmbed = discord.Embed(
            colour=self.bot.colour,
            url=response['results'][0]['url'],
            title=F"{response['results'][0]['name']} 's Information",
            timestamp=ctx.message.created_at,
        )
        ramchmbed.description = F"""
        Stauts: {response['results'][0]['status']}
        Species: {response['results'][0]['species']}
        Type: {'Unknown' if not response['results'][0]['type'] else response['results'][0]['type']}
        Gender: {response['results'][0]['gender']}
        Origin: {response['results'][0]['origin']['name']}
        Location: {response['results'][0]['location']['name']}
        Created: {response['results'][0]['created']}
        """.replace("\t", "")
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