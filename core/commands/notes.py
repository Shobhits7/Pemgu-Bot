import discord
from discord.ext import commands

class Notes(commands.Cog, description="Taking notes with these for lazy people!"):
    def __init__(self, bot):
        self.bot = bot

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
            timestamp=ctx.message.created_at
        )
        clearmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        notes = await self.bot.postgres.fetch("SELECT * FROM notes WHERE user_id=$1", ctx.author.id)
        tasks = []
        if not notes:
            clearmbed.title = "You don't have any tasks"
            return await ctx.send(embed=clearmbed)
        for stuff in notes:
            tasks.append(stuff["task"])
        for task in tasks:
            await self.bot.postgres.execute("DELETE FROM notes WHERE task=$1 AND user_id=$1", task, ctx.author.id)
        clearmbed.title = "Successfully removed:"
        clearmbed.description = "**Every Task**"
        await ctx.send(embed=clearmbed)

def setup(bot):
    bot.add_cog(Notes(bot))