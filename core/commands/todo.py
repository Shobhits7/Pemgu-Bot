import discord
from discord.ext import commands

class Todo(commands.Cog, description="If you are so lazy to do stuff, use these"):
    def __init__(self, bot):
        self.bot = bot

    # Todo
    @commands.group(name="todo", help="Consider using subcommands", invoke_without_command=True)
    async def todo(self, ctx:commands.Context):
        await ctx.send_help("Todo")

    # List
    @todo.command(name="list", help="Will show your or another user's tasks list")
    async def list(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        listmbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        listmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        todos = await self.bot.postgres.fetch("SELECT * FROM todos WHERE user_id=$1", user.id)
        if not todos: 
            listmbed.title = F"{user} doesn't have any tasks"
            return await ctx.send(embed=listmbed)
        tasks = []
        counter = 0
        for stuff in todos:
            tasks.append(F"{counter} - {stuff['task']}\n")
            counter += 1
        listmbed.title=F"{user}'s tasks:"
        listmbed.description="".join(task for task in tasks)
        await ctx.send(embed=listmbed)

    # Add
    @todo.command(name="add", help="Will add the given task to your tasks")
    async def add(self, ctx:commands.Context, *, task:str):
        await self.bot.postgres.execute("INSERT INTO todos(user_name,user_id,task) VALUES($1,$2,$3)", ctx.author.name, ctx.author.id, task)
        addmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully added:",
            description=F"> {task}\n**To your tasks**",
            timestamp=ctx.message.created_at
        )
        addmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=addmbed)

    # Remove
    @todo.command(name="remove", help="Will remove the given task from your tasks")
    async def remove(self, ctx:commands.Context, *, task:int):
        removembed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        removembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        todos = await self.bot.postgres.fetch("SELECT * FROM todos WHERE user_id=$1", ctx.author.id)
        tasks = []
        if not todos:
            removembed.title = "You don't have any tasks"
            return await ctx.send(embed=removembed)
        for stuff in todos:
            tasks.append(stuff["task"])
        todo = await self.bot.postgres.fetchval("SELECT task FROM todos WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[task])
        if not todo:
            removembed.title = "Is not in your tasks:"
            removembed.description = F"> {tasks[task]}"
            return await ctx.send(embed=removembed)
        removembed.title = "Successfully removed:"
        removembed.description = F"> {tasks[task]}\n**From your tasks**"
        await self.bot.postgres.execute("DELETE FROM todos WHERE user_id=$1 AND task=$2", ctx.author.id, tasks[task])
        await ctx.send(embed=removembed)

def setup(bot):
    bot.add_cog(Todo(bot))