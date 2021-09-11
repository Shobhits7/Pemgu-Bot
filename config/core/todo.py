import discord
from discord.ext import commands

class Todo(commands.Cog, description="Lazy people use these"):
    def __init__(self, bot):
        self.bot = bot

    # List
    @commands.command(name="todo list", help="Will tell you, your todo list")
    async def todo_list(self, ctx):
        await ctx.trigger_typing()
        tasks = await self.bot.db.fetch("SELECT task FROM todos WHERE user_id = $1", ctx.author.id)
        if len(tasks) == 0:
            await ctx.send("You don't have a todo list\nTry to make one with `todo add` command")
        else:
            todombed = discord.Embed(
                title="Here is your todo list",
            )
            todombed.description = "\n".join(f"{i+1} {task['task']}" for i, task in enumerate(tasks))
            await ctx.send(embed=todombed)
    
    # Add
    @commands.command(name="todo add", help="Will add the given task", usage="<task>")
    async def todo_add(self, ctx, *, task):
        await ctx.trigger_typing()
        await self.bot.db.execute("INSERT INTO todos(user_id, task) VALUES($1, $2)", ctx.author.id, task)
        await ctx.send("Your task has been now added")

    # Remove
    @commands.command(name="todo remove", help="Will remove the given task", usage="<task>")
    async def todo_remove(self, ctx, *, task):
        await ctx.trigger_typing()
        task = await self.bot.db.fetch(F"SELECT {task} FROM todos WHERE user_id = $1", ctx.author.id)
        if len(task) == 0:
            await ctx.send(F"You don't have {task} in your list")
        else:
            await self.bot.db.execute("DELETE FROM todos WHERE user_id = $1 AND task = $2", ctx.author.id, task)
            await ctx.send(F"{task} has been now removed from your list")

def setup(bot):
    bot.add_cog(Todo(bot))