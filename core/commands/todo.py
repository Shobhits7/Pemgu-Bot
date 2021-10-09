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
        for task in todos:
            tasks.append(F"{counter} - {task}\n")
            counter += 1
        todombed = discord.Embed(
            colour=self.bot.colour,
            title="Your current tasks:",
            description="".join(task for task in tasks),
            timestamp=ctx.message.created_at
        )
        todombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar)
        await ctx.send(embed=todombed)

def setup(bot):
    bot.add_cog(Todo(bot))