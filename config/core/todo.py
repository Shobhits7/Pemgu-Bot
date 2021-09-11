import discord
from discord.ext import commands

class Todo(commands.Cog, description="Lazy people use these"):
    def __init__(self, bot):
        self.bot = bot

    # Todo
    @commands.group(name="todo", help="Will tell you, your todo list", invoke_without_command=True)
    async def todo(self, ctx):
        await ctx.trigger_typing()
        todo = await self.bot.db.fetch("SELECT task, position FROM todo WHERE user_id = $1", ctx.author.id)
        if len(todo) == 0:
            await ctx.send("You don't have a todo list\nTry to make one with `todo add` command")
        else:
            todombed = discord.Embed(
                title="Here is your todo list",
            )
            todombed.description = "\n".join("{position}: {task}".format(**_) for _ in todo)
            await ctx.send(embed=todombed)
    
    # Add
    @todo.command(name="add", help="Will add the given task", usage="<task>")
    async def add(self, ctx, *, task):
        await ctx.trigger_typing()
        await self.bot.db.execute("INSERT INTO todo(user_id, task) VALUES ($1, $2)", ctx.author.id, task)
        await ctx.send("Your task has been now added")

def setup(bot):
    bot.add_cog(Todo(bot))