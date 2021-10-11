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
        badtodombed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} currently doesn't have any tasks",
            timestamp=ctx.message.created_at
        )
        badtodombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        todos = await self.bot.postgres.fetch("SELECT * FROM todos WHERE user_id=$1", user.id)
        if not todos: return await ctx.send(embed=badtodombed)
        tasks = []
        counter = 1
        for stuff in todos:
            tasks.append(F"{counter} - {stuff['task']}\n")
            counter += 1
        fintodombed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user}'s current tasks:",
            description="".join(task for task in tasks),
            timestamp=ctx.message.created_at
        )
        fintodombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=fintodombed)

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
    async def remove(self, ctx:commands.Context, *, task:str):
        badremovembed = discord.Embed(
            colour=self.bot.colour,
            title=F"> {task}",
            description="Is not in your tasks",
            timestamp=ctx.message.created_at
        )
        badremovembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        finremovedmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully removed:",
            description=F"> {task}\n**From your tasks**",
            timestamp=ctx.message.created_at
        )
        finremovedmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        tasks = await self.bot.postgres.fetch("SELECT task FROM todos WHERE user_id=$1 AND task=$2", ctx.author.id, task)
        if not tasks: return await ctx.send(embed=badremovembed)
        await self.bot.postgres.execute("DELETE FROM todos WHERE user_id=$1 AND task=$2", ctx.author.id, task)
        await ctx.send(embed=finremovedmbed)

def setup(bot):
    bot.add_cog(Todo(bot))