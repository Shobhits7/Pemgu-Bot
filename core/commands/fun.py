import discord
from discord.ext import commands
import core.views.funview as fv

class Fun(commands.Cog, description="You sad?. Use these to at least have a smile"):
    def __init__(self, bot):
        self.bot = bot

    # Say
    @commands.command(name="say", help="Will say your message")
    async def say(self, ctx:commands.Context, *, say:str):
        await ctx.send(F"{say} | {ctx.author.mention}")

    # Nitro
    @commands.command(name="nitro", help="Will gift free Nitro")
    async def nitro(self, ctx:commands.Context):
        bnitrombed = discord.Embed(
            colour=self.bot.colour,
            title="A WILD NITRO GIFT APPEARS?!",
            description="Expires in 48 hours\nClick the button for claiming Nitro:.",
            timestamp=ctx.message.created_at
        )
        bnitrombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = fv.NitroView(ctx)
        view.message = await ctx.send(embed=bnitrombed, view=view)

def setup(bot):
    bot.add_cog(Fun(bot))