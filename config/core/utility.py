import discord
from discord.ext import commands
from config.utils.help import MyHelp
import time

class Utility(commands.Cog, name="Utility ⚙", aliases=["utility", "Utility"], description="Useful commands are open to everyone"):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = MyHelp()
        self.bot.help_command.cog = self

    # About
    @commands.command(name="about", aliases=["ab"], help="Will show the bot's information")
    async def about(self, ctx):
        await ctx.trigger_typing()
        abmbed = discord.Embed(
            colour=self.bot.color,
            title="About Bot",
            timestamp=ctx.message.created_at
        )
        abmbed.set_image(url="https://imgur.com/YTmL4GG.png")
        abmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=abmbed)

    # Info
    @commands.command(name="info", aliases=["io"], help="Will show member info", usage="[user]")
    @commands.guild_only()
    async def info(self, ctx, *, member:commands.MemberConverter = None):
        await ctx.trigger_typing()
        user = member or ctx.author
        iombed = discord.Embed(
            colour=self.bot.color,
            title=F"{user.display_name} Information",
            timestamp=ctx.message.created_at
        )
        iombed.add_field(name="Joined Date", value=F"{user.mention} joined the server on\n{user.joined_at}")
        iombed.add_field(name="Roles", value=F"User has {len(user.roles)-1} roles")
        iombed.set_thumbnail(url=user.avatar_url)
        iombed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=iombed)

    # Stats
    @commands.command(name="stats", aliases=["sa"], help="Will show the stats of this server")
    @commands.guild_only()
    async def stats(self, ctx):
        await ctx.trigger_typing()
        sambed = discord.Embed(
            colour=self.bot.color,
            title="Stats for this server",
            timestamp=ctx.message.created_at
        )
        sambed.add_field(name="Members", value=F"{len(ctx.guild.members)} members are in this guild")
        sambed.add_field(name="Channels", value=F"{len(ctx.guild.channels)} channels are in this guild")
        sambed.set_thumbnail(url=ctx.guild.icon_url)
        sambed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=sambed)

    # Avatar
    @commands.command(name="avatar", aliases=["av"], help="Will show your or another member avatar", usage="[user]")
    async def avatar(self, ctx, *, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        avmbed = discord.Embed(
            colour=self.bot.color,
            title="User's Avatar",
            timestamp=ctx.message.created_at
        )
        avmbed.set_image(url=user.avatar_url)
        avmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=avmbed)

    # Icon
    @commands.command(name="icon", aliases=["ic"], help="Will show the guild's icon")
    @commands.guild_only()
    async def icon(self, ctx):
        await ctx.trigger_typing()
        icmbed = discord.Embed(
            colour=self.bot.color,
            title="Server's Icon",
            timestamp=ctx.message.created_at
        )
        icmbed.set_image(url=ctx.guild.icon_url)
        icmbed.set_image(url=ctx.guild.icon_url)
        icmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=icmbed)

    # Ping
    @commands.command(name="ping", aliases=["pi"], help="Will show your latency")
    async def ping(self, ctx):
        await ctx.trigger_typing()
        start = time.perf_counter()
        unpimbed = discord.Embed(
            colour=self.bot.color,
            title="🎾 Pinging...",
            timestamp=ctx.message.created_at
        )
        unpimbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        unpimsg = await ctx.reply(embed=unpimbed)
        end = time.perf_counter()
        dopimbed = discord.Embed(
            colour=self.bot.color,
            title="🏓 Pong:",
            description=F"Ping! {(end - start) * 1000}ms",
            timestamp=ctx.message.created_at
        )
        dopimbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await unpimsg.edit(embed=dopimbed)

    # Invite
    @commands.command(name="invite", aliases=["ie"], help="Will make a send the link for adding  the bot")
    async def invite(self, ctx):
        await ctx.trigger_typing()
        iembed = discord.Embed(
            colour=self.bot.color,
            title="Here is the invite link for adding the bot 👈",
            url=discord.utils.oauth_url(client_id=844226171972616205, permissions=discord.Permissions(administrator=True)),
            timestamp=ctx.message.created_at
        )
        iembed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=iembed)
    
    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    @commands.guild_only()
    @commands.has_guild_permissions(change_nickname=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def afk(self, ctx):
        await ctx.trigger_typing()
        unafkmbed = discord.Embed(
            colour=self.bot.color,
            title="Your name has been changed to it's original",
            timestamp=ctx.message.created_at
        )
        unafkmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        doafkmbed = discord.Embed(
            colour=self.bot.color,
            title="Doing AFK",
            description="Your name has been now changed to `AFK`\nAnd now moving you to the afk voice",
            timestamp=ctx.message.created_at
        )
        doafkmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if ctx.author.nick == "AFK":
            await ctx.author.edit(nick=None)
            return await ctx.reply(embed=unafkmbed)
        await ctx.author.edit(nick="AFK")
        await ctx.reply(embed=doafkmbed)
        await ctx.author.move_to(ctx.guild.afk_channel)
    
def setup(bot):
    bot.add_cog(Utility(bot))
    