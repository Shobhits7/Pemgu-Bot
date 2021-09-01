import nextcord
from nextcord.ext import commands
import time

class Utility(commands.Cog, description="Useful commands are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # About
    @commands.command(name="about", aliases=["ab"], help="Will show the bot's information")
    async def about(self, ctx):
        await ctx.trigger_typing()
        abmbed = nextcord.Embed(
            colour=0x2F3136,
            title="About Bot",
            timestamp=ctx.message.created_at
        )
        abmbed.description += "[Click here for Commands](https://lvlahraam.gitbook.io/brevity-bot/commands)"
        abmbed.description += "\n[Click here for FAQ](https://lvlahraam.gitbook.io/brevity-bot)\n"
        abmbed.description += F"[Click here for Invite]({nextcord.utils.oauth_url(client_id=844226171972616205, permissions=nextcord.Permissions(administrator=True))})"
        abmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=abmbed)

    # Info
    @commands.command(name="info", aliases=["io"], help="Will show member info", usage="[user]")
    @commands.guild_only()
    async def info(self, ctx, *, member:commands.MemberConverter = None):
        await ctx.trigger_typing()
        user = member or ctx.author
        iombed = nextcord.Embed(
            colour=0x2F3136,
            title=F"{user.display_name} Information",
            timestamp=ctx.message.created_at
        )
        iombed.add_field(name="Joined Date", value=F"{user.mention} joined the server on\n{user.joined_at}")
        iombed.add_field(name="Roles", value=F"User has {len(user.roles)-1} roles")
        iombed.set_thumbnail(url=user.avatar.url)
        iombed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=iombed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another member avatar", usage="[user]")
    async def avatar(self, ctx, *, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        avmbed = nextcord.Embed(
            colour=0x2F3136,
            title="User's Avatar",
            timestamp=ctx.message.created_at
        )
        avmbed.set_image(url=user.avatar.url)
        avmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=avmbed)

    # Icon
    @commands.command(name="icon", aliases=["ic"], help="Will show the guild's icon")
    @commands.guild_only()
    async def icon(self, ctx):
        await ctx.trigger_typing()
        icmbed = nextcord.Embed(
            colour=0x2F3136,
            title="Server's Icon",
            timestamp=ctx.message.created_at
        )
        icmbed.set_image(url=ctx.guild.icon_url)
        icmbed.set_image(url=ctx.guild.icon_url)
        icmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=icmbed)

    # Stats
    @commands.command(name="stats", aliases=["sa"], help="Will show the stats of this server")
    @commands.guild_only()
    async def stats(self, ctx):
        await ctx.trigger_typing()
        sambed = nextcord.Embed(
            colour=0x2F3136,
            title="Stats for this server",
            timestamp=ctx.message.created_at
        )
        sambed.add_field(name="Members", value=F"{len(ctx.guild.members)} members are in this guild")
        sambed.add_field(name="Channels", value=F"{len(ctx.guild.channels)} channels are in this guild")
        sambed.set_thumbnail(url=ctx.guild.icon_url)
        sambed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sambed)

    # Echo
    @commands.command(name="echo", aliases=["eo"], help="Will echo your message", usage="<text>")
    async def echo(self, ctx, *, echo):
        await ctx.trigger_typing()
        badeombed = nextcord.Embed(
            colour=0x2F3136,
            title="Don't even think of using that",
            timestamp=ctx.message.created_at
        )
        badeombed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        if "@everyone" in ctx.message.content or "@here" in ctx.message.content:
            if ctx.author.guild_permissions.mention_everyone:
                return await ctx.send(echo)
            return await ctx.send(embed=badeombed)
        else:
            await ctx.send(echo)

    # Ping
    @commands.command(name="ping", aliases=["pi"], help="Will show your latency")
    async def ping(self, ctx):
        await ctx.trigger_typing()
        start = time.perf_counter()
        unpimbed = nextcord.Embed(
            colour=0x2F3136,
            title="🎾 Pinging...",
            timestamp=ctx.message.created_at
        )
        unpimbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        unpimsg = await ctx.send(embed=unpimbed)
        end = time.perf_counter()
        dopimbed = nextcord.Embed(
            colour=0x2F3136,
            title="🏓 Pong:",
            description=F"Ping! {(end - start) * 1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await unpimsg.edit(embed=dopimbed)

    # Invite
    @commands.command(name="invite", aliases=["ie"], help="Will make a send the link for adding  the bot")
    async def invite(self, ctx):
        await ctx.trigger_typing()
        iembed = nextcord.Embed(
            colour=0x2F3136,
            title="Here is the invite link for adding the bot 👈",
            url=nextcord.utils.oauth_url(client_id=844226171972616205, permissions=nextcord.Permissions(administrator=True)),
            timestamp=ctx.message.created_at
        )
        iembed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=iembed)

    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    @commands.guild_only()
    @commands.has_guild_permissions(change_nickname=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def afk(self, ctx):
        await ctx.trigger_typing()
        unafkmbed = nextcord.Embed(
            colour=0x2F3136,
            title="Your name has been changed to it's original",
            timestamp=ctx.message.created_at
        )
        unafkmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        doafkmbed = nextcord.Embed(
            colour=0x2F3136,
            title="Doing AFK",
            description="Your name has been now changed to `AFK`\nAnd now moving you to the afk voice",
            timestamp=ctx.message.created_at
        )
        doafkmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        if ctx.author.nick == "AFK":
            await ctx.author.edit(nick=None)
            return await ctx.send(embed=unafkmbed)
        await ctx.author.edit(nick="AFK")
        await ctx.send(embed=doafkmbed)
        await ctx.author.move_to(ctx.guild.afk_channel)
    
def setup(bot):
    bot.add_cog(Utility(bot))