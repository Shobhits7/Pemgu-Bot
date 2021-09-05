import discord
from discord.ext import commands
from config.utils.help import MyHelp
import time

class Utility(commands.Cog, description="Useful commands are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # About
    @commands.command(name="about", aliases=["ab"], help="Will show the bot's information")
    async def about(self, ctx):
        await ctx.trigger_typing()
        abmbed = discord.Embed(
            colour=0x525BC2,
            title="About Bot",
            description=F"[Click here for Commands](https://lvlahraam.gitbook.io/brevity-bot/commands)\n[Click here for FAQ](https://lvlahraam.gitbook.io/brevity-bot)\n[Click here for Adding Bot](https://dsc.gg/brevity-bot)\n[Click here for Joining Support](https://dsc.gg/brevity-support)",
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=abmbed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another user's avatar", usage="[user]")
    async def avatar(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        avmbed = discord.Embed(
            colour=0x525BC2,
            title=F"{user} Avatar",
            timestamp=ctx.message.created_at
        )
        avmbed.set_image(url=user.avatar.url)
        avmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=avmbed)

    # Banner
    @commands.command(name="banner", aliases=["br"], help="Will show your or another user's banner", usage="[user]")
    async def banner(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        image = await self.bot.fetch_user(user.id)
        brmbed = discord.Embed(
            colour=0x525BC2,
            title=F"{user} Banner",
            timestamp=ctx.message.created_at
        )
        if image.banner and image.banner.url:
            brmbed.set_image(url=image.banner.url)
        else:
            brmbed.description = "*This user doesn't have any banner*"
        brmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=brmbed)

    # Info
    @commands.command(name="info", aliases=["io"], help="Will show member info", usage="[user]")
    @commands.guild_only()
    async def info(self, ctx, *, member:commands.MemberConverter = None):
        await ctx.trigger_typing()
        user = member or ctx.author
        image = await self.bot.fetch_user(user.id)
        iombed = discord.Embed(
            colour=0x525BC2,
            title=F"{user} Information",
            timestamp=ctx.message.created_at
        )
        iombed.add_field(name="Joined Date", value=F"{user.mention} joined the server on\n{user.joined_at}")
        iombed.add_field(name="Roles", value=F"User has {len(user.roles)-1} roles")
        iombed.set_thumbnail(url=user.avatar.url)
        if image.banner and image.banner.url:
            iombed.set_image(url=image.banner.url)
        else:
            iombed.description = "*This user doesn't have any banner*"
        iombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=iombed)

    # Stats
    @commands.command(name="stats", aliases=["sa"], help="Will show the stats of this server")
    @commands.guild_only()
    async def stats(self, ctx):
        await ctx.trigger_typing()
        sambed = discord.Embed(
            colour=0x525BC2,
            title="Stats for this server",
            timestamp=ctx.message.created_at
        )
        sambed.add_field(name="Members", value=F"{len(ctx.guild.members)} members are in this guild")
        sambed.add_field(name="Channels", value=F"{len(ctx.guild.channels)} channels are in this guild")
        sambed.set_thumbnail(url=ctx.guild.icon.url)
        if ctx.guild.banner and ctx.guild.banner.url:
            sambed.set_image(url=ctx.guild.banner.url)
        else:
            sambed.description = "*This guild doesn't have any banner*"
        sambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sambed)

    # Echo
    @commands.command(name="echo", aliases=["eo"], help="Will echo your message", usage="<text>")
    async def echo(self, ctx, *, echo):
        await ctx.trigger_typing()
        await ctx.send(echo)

    # Ping
    @commands.command(name="ping", aliases=["pi"], help="Will show bot's ping")
    async def ping(self, ctx):
        await ctx.trigger_typing()
        unpimbed = discord.Embed(
            colour=0x525BC2,
            title="🎾 Pinging...",
            timestamp=ctx.message.created_at
        )
        unpimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        start = time.perf_counter()
        unpimsg = await ctx.send(embed=unpimbed)
        end = time.perf_counter()
        dopimbed = discord.Embed(
            colour=0x525BC2,
            title="🏓 Pong:",
            description=F"Ping! {(end - start) * 1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await unpimsg.edit(embed=dopimbed)

    # Invite
    @commands.command(name="invite", aliases=["ie"], help="Will make a send the link for adding  the bot")
    async def invite(self, ctx):
        await ctx.trigger_typing()
        iembed = discord.Embed(
            colour=0x525BC2,
            title="Here is the invite link for adding the bot 👈",
            url=discord.utils.oauth_url(client_id=844226171972616205, permissions=discord.Permissions(administrator=True)),
            timestamp=ctx.message.created_at
        )
        iembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=iembed)

    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    @commands.guild_only()
    @commands.has_guild_permissions(change_nickname=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def afk(self, ctx):
        await ctx.trigger_typing()
        unafkmbed = discord.Embed(
            colour=0x525BC2,
            title="Your name has been changed to it's original",
            timestamp=ctx.message.created_at
        )
        unafkmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        doafkmbed = discord.Embed(
            colour=0x525BC2,
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
