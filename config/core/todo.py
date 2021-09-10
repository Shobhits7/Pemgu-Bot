import discord
from discord.ext import commands

class Todo(commands.Cog, description="Lazy people use these"):
    def __init__(self, bot):
        self.bot = bot

    # Todo
    @commands.group(name="todo", help="Will tell you, your todo list", invoke_without_command=True)
    async def todo(self, ctx):
        await ctx.trigger_typing()
        await ctx.send("IN DEVELOPMENT")

def setup(bot):
    bot.add_cog(Todo(bot))