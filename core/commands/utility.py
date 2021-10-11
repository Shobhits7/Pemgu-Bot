import discord
from discord.ext import commands

class Utility(commands.Cog, description="Useful commands that are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # Cleanup
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    async def cleanup(self, ctx:commands.Context, *, amount:int):
        cumbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Cleaned-up {amount} of bot messages",
        )
        cumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.channel.purge(limit=amount+1, check=lambda m: m.author.id == self.bot.user.id, bulk=False)
        await ctx.send(embed=cumbed, delete_after=5)

    # Note
    @commands.group(name="note", help="Consider using subcommands", invoke_without_command=True)
    async def note(self, ctx:commands.Context):
        await ctx.send_help("note")

    # List
    @note.command(name="list", help="Will show your or another user's notes")
    async def list(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        listmbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        listmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", user.id)
        if not notes: 
            listmbed.title = F"{user} doesn't have any tasks"
            return await ctx.send(embed=listmbed)
        tasks = []
        counter = 0
        for stuff in notes:
            tasks.append(F"{counter} - {stuff['task']}\n")
            counter += 1
        listmbed.title=F"{user}'s tasks:"
        listmbed.description="".join(task for task in tasks)
        await ctx.send(embed=listmbed)

    # Add
    @note.command(name="add", help="Will add the given task to your notes")
    async def add(self, ctx:commands.Context, *, task:str):
        await self.bot.postgres.execute("INSERT INTO notes(user_name,user_id,task) VALUES($1,$2,$3)", ctx.author.name, ctx.author.id, task)
        addmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully added:",
            description=F"> {task}\n**To your notes**",
            timestamp=ctx.message.created_at
        )
        addmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=addmbed)

    # Remove
    @note.command(name="remove", help="Will remove the given task from your notes")
    async def remove(self, ctx:commands.Context, *, number:int):
        removembed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        removembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", ctx.author.id)
        tasks = []
        if not notes:
            removembed.title = "You don't have any tasks"
            return await ctx.send(embed=removembed)
        for stuff in notes:
            tasks.append(stuff["task"])
        note = await self.bot.postgres.fetchval("SELECT task FROM notes WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[number])
        if not note:
            removembed.title = "Is not in your tasks:"
            removembed.description = F"> {number}\n**Check your tasks.**"
            return await ctx.send(embed=removembed)
        removembed.title = "Successfully removed:"
        removembed.description = F"> {tasks[number]}\n**From your tasks**"
        await self.bot.postgres.execute("DELETE FROM notes WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[number])
        await ctx.send(embed=removembed)

    # PYPI
    @commands.command(name="pypi", help="Will give information about the given library in PYPI")
    async def pypi(self, ctx:commands.Context, *, library:str):
        pypimbed = discord.Embed(
            colour=self.bot.colour,
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