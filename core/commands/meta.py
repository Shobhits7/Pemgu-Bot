import discord, time, os, inspect
from discord.ext import commands

class Meta(commands.Cog, description="Control the bot with this like a real robot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.group(name="prefix", aliases=["pf"], help="Will tell you the prefix for this guild", invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx:commands.Context):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        pfmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"My Prefix here is:",
            description=F"> {self.bot.prefix if not prefix else prefix}",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfmbed)

    # Prefix-Change
    @prefix.command(name="change", aliases=["ch"], help="Will change the prefix to the new given prefix")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def prefix_change(self, ctx:commands.Context, *, text:str):
        if text == self.bot.prefix: await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        else: prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        if not prefix: await self.bot.postgres.execute("INSERT INTO prefixes(guild_name,guild_id,prefix) VALUES ($1,$2,$3)", ctx.guild.name, ctx.guild.id, text)
        else: await self.bot.postgres.execute("UPDATE prefixes SET prefix=$1 WHERE guild_name=$2 AND guild_id=$3", text, ctx.guild.name, ctx.guild.id)
        pfchmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully changed prefix to:",
            description=F"> {text}",
            timestamp=ctx.message.created_at
        )
        pfchmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfchmbed)

    # Prefix-Reset
    @prefix.command(name="reset", aliases=["rs"], help="Will reset the prefix")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def prefix_reset(self, ctx:commands.Context):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        if prefix: await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        pfrsmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully resetted to:",
            description=F"> {self.bot.prefix}",
            timestamp=ctx.message.created_at
        )
        pfrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfrsmbed)

    # Cleanup
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    async def cleanup(self, ctx:commands.Context, *, amount:int):
        cumbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Cleaned-up {amount} of bot messages",
        )
        cumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.channel.purge(limit=amount+1, check=lambda m: m.author.id == self.bot.user.id, bulk=False)
        await ctx.send(embed=cumbed, delete_after=2.5)

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
        allowed = []
        allowed_emote = "<:allow:896062865071566898>"
        denied = []
        denied_emote = "<:deny:896062993090084974>"
        for permission, value in ctx.me.guild_permissions:
            permission.replace("_", " ").title()
            if value:
                allowed.append(F"{allowed_emote} - {permission}\n")
            if not value:
                denied.append(F"{denied_emote} - {permission}\n")
        permsmbed = discord.Embed(colour=self.bot.colour, title=F"{ok_emote} Bot Permissions", timestamp=ctx.message.created_at)
        permsmbed.add_field(name="Allowed:", value="\n".join(allow for allow in allowed), inline=True)
        permsmbed.add_field(name="Denied:", value="\n".join(deny for deny in denied), inline=True)
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
        source_url = "https://github.com/lvlahraam/JakeTheDog-Bot"
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
            source_url = "https://github.com/lvlahraam/JakeTheDog-Bot"
        final_url = F"<{source_url}/blob/main/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        await ctx.send(final_url)

def setup(bot):
    bot.add_cog(Meta(bot))