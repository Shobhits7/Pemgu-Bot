import discord
from discord.ext import commands

class Todo(commands.Cog, description="If you are so lazy to do stuff, use these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="todo", help="Will show your list of tasks, consider using subcommands", invoke_without_command=True)
    async def todo(self, ctx:commands.Context):
        todos = await self.bot.postgres.fetch("SELECT * FROM todos WHERE user_id=$1", ctx.author.id)
        tasks = []
        counter = 1
        if not todos: return await ctx.send("You currently don't have any tasks")
        for stuff in todos:
            tasks.append(F"{counter} - {stuff['task']}\n")
            counter += 1
        todombed = discord.Embed(
            colour=self.bot.colour,
            title="Your current tasks:",
            description="".join(task for task in tasks),
            timestamp=ctx.message.created_at
        )
        todombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=todombed)

    @todo.command(name="add", help="Will add the given task to your tasks")
    async def add(self, ctx:commands.Context, *, task:str):
        await self.bot.postgres.execute("INSERT INTO todos(user_name,user_id,task) VALUES($1,$2,$3)", ctx.author.name, ctx.author.id, task)
        addmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully added,",
            description=F"> {task}\n**To your tasks**",
            timestamp=ctx.message.created_at
        )
        addmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=addmbed)

def setup(bot):
    bot.add_cog(Todo(bot))