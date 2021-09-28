import discord, time, os, inspect
from discord.ext import commands

class Utility(commands.Cog, description="Useful commands that are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # About
    @commands.command(name="about", aliases=["ab"], help="Will show the bot's information")
    async def about(self, ctx:commands.Context):
        abmbed = discord.Embed(
            colour=self.bot.colour,
            title="About Bot",
            description=F"[Click here for Adding Bot]({discord.utils.oauth_url(client_id=self.bot.user.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))})\n[Click here for Joining Support](https://discord.gg/bWnjkjyFRz)\nIn {len(self.bot.guilds)} Servers\nHas {len(self.bot.commands)} Commands\nOwner is lvlahraam#8435",
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=abmbed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another user's avatar", usage="[user]")
    async def avatar(self, ctx:commands.Context, user:discord.User = None):
        user = ctx.author if not user else user
        avmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} Avatar",
            timestamp=ctx.message.created_at
        )
        avmbed.set_image(url=user.display_avatar.url)
        avmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=avmbed)

    # Banner
    @commands.command(name="banner", aliases=["br"], help="Will show your or another user's banner", usage="[user]")
    async def banner(self, ctx:commands.Context, user:discord.User = None):
        user = ctx.author if not user else user
        image = await self.bot.fetch_user(user.id)
        brmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} Banner",
            timestamp=ctx.message.created_at
        )
        if image.banner and image.banner.url:
            brmbed.set_image(url=image.banner.url)
        else:
            brmbed.description = "The user doesn't have a banner"
        brmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=brmbed)

    # UserInfo
    @commands.command(name="userinfo", aliases=["ui"], help="Will show user info", usage="[user]")
    @commands.guild_only()
    async def userinfo(self, ctx:commands.Context, *, member:discord.Member = None):
        member = ctx.author if not member else member
        image = await self.bot.fetch_user(member.id)
        uimbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{member} Information",
            description="`Global-Information` is for the user in discord\n`Server-Information` is for the user in server",
            timestamp=ctx.message.created_at
        )
        uimbed.description += F"""
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
        if member.avatar:
            uimbed.set_thumbnail(url=member.display_avatar.url)
        else: uimbed.description += "__**Avatar:**__ User doesn't have a avatar"
        if image.banner:
            uimbed.set_image(url=image.banner.url)
        else: uimbed.description += "__**Banner:**__ User doesn't have a banner"
        uimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=uimbed)

    # ServerInfo
    @commands.command(name="serverinfo", aliases=["si"], help="Will show the server's info")
    @commands.guild_only()
    async def serverinfo(self, ctx:commands.Context):
        simbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{ctx.guild.name} 's Information",
            description="`Owner-Information` is for the user that owns this server\n`Server-Information` is for the actual server",
            timestamp=ctx.message.created_at
        )
        simbed.description += F"""
        __**Owner-Information:**__
        ***Username:*** {ctx.guild.owner.name}
        ***Discriminator:*** {ctx.guild.owner.discriminator}
        ***ID:*** {ctx.guild.owner.id}
        ***Mention:*** {ctx.guild.owner.mention}
        ***Badges:*** {', '.join([flag.replace("_", " ").title() for flag, enabled in ctx.guild.owner.public_flags if enabled])}
        ***Registered:*** {discord.utils.format_dt(ctx.guild.owner.created_at, style="F")} ({discord.utils.format_dt(ctx.guild.owner.created_at, style="R")})
        __**Server-Information:**__
        ***Name:*** {ctx.guild.name}
        ***ID:*** {ctx.guild.id}
        ***Description:*** {'*No Description*' if not ctx.guild.description else ctx.guild.description}
        ***Created-At:*** {discord.utils.format_dt(ctx.guild.created_at, style="F")} ({discord.utils.format_dt(ctx.guild.created_at, style="R")})
        ***Region:*** {ctx.guild.region}
        ***MFA:*** {ctx.guild.mfa_level}
        ***Verification:*** {ctx.guild.verification_level}
        ***File-Size-Limit:*** {ctx.guild.filesize_limit}
        ***Members:*** {ctx.guild.member_count}
        ***Default-Role:*** {ctx.guild.default_role.mention}
        ***Boost-Role:*** {ctx.guild.premium_subscriber_role.mention}
        ***Boosters:*** {ctx.guild.premium_subscription_count}
        ***Tier:*** {ctx.guild.premium_tier}
        ***Categories:*** {len(ctx.guild.categories)}
        ***Channels:*** {len(ctx.guild.channels)}
        ***AFK-Channel:*** {'*No AFK channel*' if not ctx.guild.afk_channel else ctx.guild.afk_channel.mention}
        ***AFK-Timeout:*** {ctx.guild.afk_timeout}
        """.replace("\t", "")
        if ctx.guild.icon:
            simbed.set_thumbnail(url=ctx.guild.icon.url)
        else: simbed.description += "__**Icon:**__ Server doesn't have a icon"
        if ctx.guild.banner:
            simbed.set_image(url=ctx.guild.banner.url)
        else: simbed.description += "__**Banner:**__ Server doesn't have a banner"
        simbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=simbed)

    # Spotify
    @commands.command(name="spotify", help="Will show your or the given member's spotify activity if possible", usage="[member]")
    async def spotify(self, ctx:commands.Context, member:discord.Member = None):
        member = ctx.author if not member else member
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                finspotifymbed = discord.Embed(
                    colour=activity.colour,
                    url=activity.track_url,
                    title=activity.title,
                    timestamp=ctx.message.created_at
                )
                finspotifymbed.description = F"""
                **Artists:** {', '.join(artist for artist in activity.artists)}
                **Album:** {activity.album}
                **Duration:** {time.strftime("%H:%M:%S", time.gmtime(activity.duration.total_seconds()))}
                **Track-ID:** {activity.track_id}
                **Party-ID:** {activity.party_id}
                **Listening-Since:** {discord.utils.format_dt(activity.created_at, style='f')} ({discord.utils.format_dt(activity.created_at, style='R')})
                """.replace("\t", "")
                finspotifymbed.set_author(name=member, icon_url=member.display_avatar.url)
                finspotifymbed.set_image(url=activity.album_cover_url)
                finspotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
                await ctx.send(embed=finspotifymbed)
                break
        else:
            badspotifymbed = discord.Embed(
                colour=self.bot.colour,
                title=F"{member} is not listenning to Spotify",
                timestamp=ctx.message.created_at
            )
            badspotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            await ctx.send(embed=badspotifymbed)

    # Say
    @commands.command(name="say", help="Will say your message", usage="<text>")
    async def say(self, ctx:commands.Context, *, say):
        await ctx.send(F"{say} | {ctx.author.mention}")

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
    @commands.command(name="source", aliases=["src"], help="Will show the bots source", usage="[command]")
    async def source(self, ctx:commands.Context, *, command: str = None):
        source_url = "https://github.com/lvlahraam/Mei-Bot"
        branch = "main"
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
            source_url = "https://github.com/lvlahraam/Mei-Bot"
            branch = "main"

        final_url = F"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        await ctx.send(final_url)

    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    @commands.guild_only()
    @commands.has_guild_permissions(change_nickname=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def afk(self, ctx:commands.Context):
        unafkmbed = discord.Embed(
            colour=self.bot.colour,
            title="Your name has been changed to it's original",
            timestamp=ctx.message.created_at
        )
        unafkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        doafkmbed = discord.Embed(
            colour=self.bot.colour,
            title="Doing AFK",
            description="Your name has been now changed to `AFK`",
            timestamp=ctx.message.created_at
        )
        doafkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if ctx.author.nick == "AFK":
            await ctx.author.edit(nick=None)
            return await ctx.send(embed=unafkmbed)
        await ctx.author.edit(nick="AFK")
        await ctx.send(embed=doafkmbed)
        if ctx.author.voice:
            doafkmbed.description += "\nNow moving you to AFK voice channel"
            await ctx.author.move_to(ctx.guild.afk_channel)

def setup(bot):
    bot.add_cog(Utility(bot))
