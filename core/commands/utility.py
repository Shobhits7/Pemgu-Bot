import discord, time, inspect, os
from discord.ext import commands
import core.views.confirm as cum

class Utility(commands.Cog, description="Useful stuff that are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # Cleanup
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    async def cleanup(self, ctx:commands.Context, *, amount:int):
        cumbed = discord.Embed(
            color=self.bot.color,
            title=F"Cleaned-up {amount} of bot messages",
        )
        cumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.channel.purge(limit=amount, check=lambda m: m.author.id == self.bot.user.id)
        await ctx.send(embed=cumbed, delete_after=5)

    # Leave
    @commands.command(name="leave", aliases=["lae"], help="Will make the bot leave")
    @commands.has_guild_permissions(administrator=True)
    async def leave(self, ctx:commands.Context):
        laembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        laembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = cum.Confirm(ctx)
        view.message = await ctx.send(content="Are you sure you want the bot to leave:", view=view)
        await view.wait()
        if view.value:
            laembed.title = F"{self.bot.user} has successfully left"
            await ctx.send(embed=laembed)
            await ctx.me.guild.leave()

    # Invite
    @commands.command(name="invite", aliases=["ie"], help="Will make a send the link for adding the bot")
    async def invite(self, ctx:commands.Context):
        iembed = discord.Embed(
            color=self.bot.color,
            title="Here is the invite link for adding the bot",
            url=discord.utils.oauth_url(client_id=self.bot.user.id, scopes=("bot", "applications.commands"), permissions=discord.Permissions(administrator=True)),
            description="Thank you for adding and inviting me!",
            timestamp=ctx.message.created_at
        )
        iembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
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
            description=F"Websocket: {self.bot.latency * 1000}ms\nTyping: {(end - start) * 1000}ms",
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

    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    @commands.guild_only()
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def afk(self, ctx:commands.Context):
        afkmbed  = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        afkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if ctx.author.nick == "AFK":
            afkmbed.title = "Name has been changed to it's original"
            await ctx.author.edit(nick=None)
            return await ctx.send(embed=afkmbed)
        afkmbed.title = "Doing AFK"
        afkmbed.description = "Name has been now changed to AFK"
        await ctx.author.edit(nick="AFK")
        await ctx.send(embed=afkmbed)
        if ctx.author.voice:
            afkmbed.description += "\nNow moving you to AFK voice channel"
            await ctx.author.move_to(ctx.guild.afk_channel)

    # Notes
    @commands.group(name="notes", aliases=["note"], help="Consider using subcommands", invoke_without_command=True)
    async def notes(self, ctx:commands.Context):
        await ctx.send_help("notes")

    # Notes-List
    @notes.command(name="list", aliases=["="], help="Will show every of your or the given user's notes")
    async def notes_list(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        notelistmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        notelistmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT task FROM notes WHERE user_id=$1", user.id)
        if not notes: 
            notelistmbed.title = F"{user} doesn't have any note"
            return await ctx.send(embed=notelistmbed)
        tasks = []
        counter = 0
        for stuff in notes:
            tasks.append(F"{counter}. {stuff['task']}\n")
            counter += 1
        notelistmbed.title=F"{user}'s notes:"
        notelistmbed.description="".join(task for task in tasks)
        await ctx.send(embed=notelistmbed)

    # Notes-Add
    @notes.command(name="add", aliases=["+"], help="Will add the given task to your notes")
    async def notes_add(self, ctx:commands.Context, *, task:str):
        noteaddmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        noteaddmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        note = await self.bot.postgres.fetchval("SELECT task FROM notes WHERE task=$1 AND user_id=$2", task, ctx.author.id)
        if note:
            noteaddmbed.title = "Is already in your notes:"
            noteaddmbed.description = F"> {task}"
            return await ctx.send(embed=noteaddmbed)
        await self.bot.postgres.execute("INSERT INTO notes(user_name,user_id,task) VALUES($1,$2,$3)", ctx.author.name, ctx.author.id, task)
        noteaddmbed.title = "Successfully added:"
        noteaddmbed.description = F"> {task}\n**To your notes**"
        await ctx.send(embed=noteaddmbed)

    # Notes-Remove
    @notes.command(name="remove", aliases=["-"], help="Will remove the given task from your notes")
    async def notes_remove(self, ctx:commands.Context, *, number:int):
        noteremovembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        noteremovembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", ctx.author.id)
        if not notes:
            noteremovembed.title = "You don't have any note"
            return await ctx.send(embed=noteremovembed)
        tasks = []
        for stuff in notes:
            tasks.append(stuff["task"])
        if len(tasks) <= number:
            noteremovembed.title = "Is not in your notes:"
            noteremovembed.description = F"> {number}\n**Check your notes**"
            return await ctx.send(embed=noteremovembed)
        note = await self.bot.postgres.fetchval("SELECT task FROM notes WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[number])
        if not note:
            noteremovembed.title = "Is not in your notes:"
            noteremovembed.description = F"> {number}\n**Check your notes**"
            return await ctx.send(embed=noteremovembed)
        await self.bot.postgres.execute("DELETE FROM notes WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[number])
        noteremovembed.title = "Successfully removed:"
        noteremovembed.description = F"> {tasks[number]}\n**From your notes**"
        await ctx.send(embed=noteremovembed)

    # Notes-Clear
    @notes.command(name="clear", aliases=["*"], help="Will clear your notes")
    async def notes_clear(self, ctx:commands.Context):
        noteclearmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        noteclearmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT task FROM notes WHERE user_id=$1", ctx.author.id)
        if not notes:
            noteclearmbed.title = "You don't have any note"
            return await ctx.send(embed=noteclearmbed)
        view = cum.Confirm(ctx)
        view.message = await ctx.send(content="Are you sure if you want to clear everything:", view=view)
        await view.wait()
        if view.value:
            tasks = []
            for stuff in notes:
                tasks.append(stuff["task"])
            for task in tasks:
                await self.bot.postgres.execute("DELETE FROM notes WHERE task=$1 AND user_id=$2", task, ctx.author.id)
            noteclearmbed.title = "Successfully cleared:"
            noteclearmbed.description = "**Your notes**"
            await ctx.send(embed=noteclearmbed)

def setup(bot):
    bot.add_cog(Utility(bot))
