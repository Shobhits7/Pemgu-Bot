import discord
from discord.ext import commands
from core.views.confirm import Confirm

class Utility(commands.Cog, description="Useful stuff that are open to everyone"):
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
        afkmbed  = discord.Embed(
            colour=self.bot.colour,
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
    @commands.group(name="notes", aliases=["note"], help="Will show all of your or the given user's notes", invoke_without_command=True)
    async def notes(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        notembed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        notembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", user.id)
        if not notes: 
            notembed.title = F"{user} doesn't have any tasks"
            return await ctx.send(embed=notembed)
        tasks = []
        counter = 0
        for stuff in notes:
            tasks.append(F"{counter}. {stuff['task']}\n")
            counter += 1
        notembed.title=F"{user}'s tasks:"
        notembed.description="".join(task for task in tasks)
        await ctx.send(embed=notembed)

    # Add
    @notes.command(name="add", aliases=["+"], help="Will add the given task to your notes")
    async def notes_add(self, ctx:commands.Context, *, task:str):
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
    @notes.command(name="remove", aliases=["-"], help="Will remove the given task from your notes")
    async def notes_remove(self, ctx:commands.Context, *, number:int):
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

    # Clear
    @notes.command(name="clear", aliases=["="], help="Will clear your notes")
    async def notes_clear(self, ctx:commands.Context):
        clearmbed = discord.Embed(
            colour=self.bot.colour,
            title="Choose your option:",
            timestamp=ctx.message.created_at
        )
        clearmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        view = Confirm(ctx)
        if not view.value:
            return await ctx.send(embed=clearmbed, view=view)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", ctx.author.id)
        if not notes:
            clearmbed.title = "You don't have any tasks"
            return await ctx.send(embed=clearmbed)
        tasks = []
        for stuff in notes:
            tasks.append(stuff["task"])
        for task in tasks:
            await self.bot.postgres.execute("DELETE FROM notes WHERE task=$1 AND user_id=$2", task, ctx.author.id)
        clearmbed.title = "Successfully removed:"
        clearmbed.description = "**Every Task**"
        await ctx.send(embed=clearmbed, view=view)

def setup(bot):
    bot.add_cog(Utility(bot))