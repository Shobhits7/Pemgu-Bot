import discord
from discord.ext import commands

class Rick_and_Morty(commands.Cog, name="Rick and Morty", description="Wubba Lubba Dub Dub"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="rickandmorty", aliases=["ram"], help="Some Rick and Morty commands, use subcommands", invoke_without_command=True)
    async def rickandmorty(self, ctx):
        await ctx.send_help(ctx.command.cog)
    
    # Character
    @rickandmorty.command(name="character", aliases=["char"], help="Will show information about the given character", usage="<character's name>")
    async def character(self, ctx, *, character: str):
        pass

    # Location
    @rickandmorty.command(name="location", aliases=["loc"], help="Will show information about the given location", usage="<location's name>")
    async def location(self, ctx, *, location: str):
        pass

    # Episode
    @rickandmorty.command(name="episode", aliases=["ep"], help="Will show information about the given episode", usage="<episode's number>")
    async def episode(self, ctx, *, episode: int):
        pass

def setup(bot):
    bot.add_cog(Rick_and_Morty(bot))