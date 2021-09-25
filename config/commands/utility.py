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
            description=F"[Click here for Adding Bot]({discord.utils.oauth_url(client_id=self.bot.user.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))})\n[Click here for Joining Support](https://discord.gg/bWnjkjyFRz)\nIn {len(self.bot.guilds)} Guilds\nHas {len(self.bot.commands)} Commands\nOwner is lvlahraam#8435",
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=abmbed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another user's avatar", usage="[user]")
    async def avatar(self, ctx:commands.Context, user:commands.UserConverter = None):
        user = user or ctx.author
        avmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} Avatar",
            timestamp=ctx.message.created_at
        )
        avmbed.set_image(url=user.avatar.url)
        avmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=avmbed)

    # Banner
    @commands.command(name="banner", aliases=["br"], help="Will show your or another user's banner", usage="[user]")
    async def banner(self, ctx:commands.Context, user:commands.UserConverter = None):
        user = user or ctx.author
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
        brmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=brmbed)

    # UserInfo
    @commands.command(name="userinfo", aliases=["ui"], help="Will show User info", usage="[user]")
    @commands.guild_only()
    async def userinfo(self, ctx:commands.Context, *, member:commands.MemberConverter = None):
        member = member or ctx.author
        image = await self.bot.fetch_user(member.id)
        uimbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{member} Information",
            description="`Global-Information` is for the member in discord\n`Guild-Information` for the member in this guild",
            timestamp=ctx.message.created_at
        )
        uimbed.add_field(name="__Global-Information:__", value=F"""
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
        ***Registered:*** {discord.utils.format_dt(member.created_at, style="F")} ({discord.utils.format_dt(member.created_at, style="R")})""", inline=False)
        uimbed.add_field(name="__Guild-Information:__", value=F"""
        ***Joined:*** {discord.utils.format_dt(member.joined_at, style="F")} ({discord.utils.format_dt(member.joined_at, style="R")})
        ***Roles [{len(member.roles)}]:*** {', '.join(role.mention for role in member.roles)}
        ***Top-Role:*** {member.top_role.mention}
        ***Boosting:*** {'True' if member in ctx.guild.premium_subscribers else 'False'}
        ***Nickname:*** {member.nick}
        ***Voice:*** {member.voice}
        ***Guild-Permissions:*** {', '.join([perm.replace("_", " ").title() for perm, enabled in member.guild_permissions if enabled])}""", inline=False)
        uimbed.set_thumbnail(url=member.avatar.url)
        if image.banner and image.banner.url:
            uimbed.set_image(url=image.banner.url)
        else:
            uimbed.description += "\n**Banner:** member doesn't have banner"
        uimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=uimbed)

    # GuildInfo
    @commands.command(name="guildinfo", aliases=["gi"], help="Will show the guild's info")
    @commands.guild_only()
    async def guildinfo(self, ctx:commands.Context):
        guildctx = ctx.guild
        gimbed = discord.Embed(
            colour=self.bot.colour,
            title="Stats for this Guild",
            timestamp=ctx.message.created_at
        )
        gimbed.add_field(name="Members", value=F"{len(ctx.guild.members)}")
        gimbed.add_field(name="Channels", value=F"{len(ctx.guild.channels)}")
        if ctx.guild.icon and ctx.guild.icon.url:
            gimbed.add_field(name="Icon:", value=F"True")
            gimbed.set_thumbnail(url=ctx.guild.icon.url)
        else:
            gimbed.add_field(name="Icon:", value=F"False")
        if ctx.guild.banner and ctx.guild.banner.url:
            gimbed.add_field(name="Banner:", value=F"True")
            gimbed.set_image(url=ctx.guild.banner.url)
        else:
            gimbed.add_field(name="Banner:", value=F"False")
        gimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=gimbed)

    # Spotify
    @commands.command(name="spotify", help="Will show your or the given member's spotify activity if possible", usage="[member]")
    async def spotify(self, ctx:commands.Context, member:discord.Member = None):
        member = member or ctx.author
        for activity in member.activities:
            if isinstance(activity, discord.Spotify):
                finspotifymbed = discord.Embed(
                    colour=activity.colour,
                    url=activity.track_url,
                    title=activity.title,
                    timestamp=ctx.message.created_at
                )
                finspotifymbed.set_author(name=member, icon_url=member.avatar.url)
                finspotifymbed.add_field(name="Artists:", value=", ".join(artist for artist in activity.artists), inline=False)
                finspotifymbed.add_field(name="Album", value=activity.album, inline=False)
                finspotifymbed.add_field(name="Duration:", value=time.strftime("%H:%M:%S", time.gmtime(activity.duration.total_seconds())), inline=False)
                finspotifymbed.add_field(name="Listening-Since:", value=F"{discord.utils.format_dt(activity.created_at, style='f')} ({discord.utils.format_dt(activity.created_at, style='R')})", inline=False)
                finspotifymbed.add_field(name="Track-ID", value=activity.track_id, inline=False)
                finspotifymbed.add_field(name="Party-ID", value=activity.party_id, inline=False)
                finspotifymbed.set_image(url=activity.album_cover_url)
                finspotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=finspotifymbed)
                break
        else:
            badspotifymbed = discord.Embed(
                colour=self.bot.colour,
                title=F"{member} is not listenning to Spotify"
            )
            badspotifymbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=badspotifymbed)

    # Echo
    @commands.command(name="echo", aliases=["eo"], help="Will echo your message", usage="<text>")
    async def echo(self, ctx:commands.Context, *, echo):
        await ctx.send(F"{echo} | {ctx.author.mention}")

    # Ping
    @commands.command(name="ping", aliases=["pi"], help="Will show bot's ping")
    async def ping(self, ctx:commands.Context):
        unpimbed = discord.Embed(
            colour=self.bot.colour,
            title="🎾 Pinging...",
            timestamp=ctx.message.created_at
        )
        unpimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        start = time.perf_counter()
        unpimsg = await ctx.send(embed=unpimbed)
        end = time.perf_counter()
        dpb = time.time()
        await self.bot.postgresql.fetch("SELECT 1")
        dopimbed = discord.Embed(
            colour=self.bot.colour,
            title="🏓 Pong:",
            description=F"Websocket: {self.bot.latency * 1000}ms\nTyping: {(end - start) * 1000}ms\nDatabase: {(time.time() - dpb) * 1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
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
        iembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
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
        unafkmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        doafkmbed = discord.Embed(
            colour=self.bot.colour,
            title="Doing AFK",
            description="Your name has been now changed to `AFK`",
            timestamp=ctx.message.created_at
        )
        doafkmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
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
