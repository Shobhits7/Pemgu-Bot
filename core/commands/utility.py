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
            title=F"{self.bot.user.name} About",
            description=F"[Click here for source code](https://github.com/lvlahraam/JakeTheDog-Bot)\n[Click here for Adding Bot]({discord.utils.oauth_url(client_id=self.bot.user.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))})\n[Click here for Joining Support](https://discord.gg/bWnjkjyFRz)\nIn {len(self.bot.guilds)} Servers\nHas {len(self.bot.commands)} Commands\nOwner is <@{self.bot.owner_id}>",
            timestamp=ctx.message.created_at
        )
        abmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=abmbed)

    # Say
    @commands.command(name="say", help="Will say your message")
    async def say(self, ctx:commands.Context, *, say:str):
        await ctx.send(F"{say} | {ctx.author.mention}")

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
        pmbed = discord.Embed(colour=self.bot.colour, title="<:greyTick:596576672900186113> Bot Permissions", description="", timestamp=ctx.message.created_at)
        for perm, val in ctx.guild.me.guild_permissions:
            if val:
                pmbed.description += F"<:greenTick:596576670815879169> - {perm.replace('_', ' ').title()}\n"
            if not val:
                pmbed.description += F"<:redTick:596576672149667840> - {perm.replace('_', ' ').title()}\n"
        pmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pmbed)

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