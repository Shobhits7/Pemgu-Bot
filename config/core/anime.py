import discord
from discord.ext import commands
from ..utils.aiohttp import session_json

class Anime(commands.Cog, description="Some Weeb shit stuff"):
    def __init__(self, bot):
        self.bot = bot
    
    # Quote
    @commands.command(name="quote", help="Will send an anime quote")
    async def quote(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://animechan.vercel.app/api/random/", headers=None)
        quotembed = discord.Embed(
            colour=self.bot.color,
            title="Here is your quoute",
            timestamp=ctx.message.created_at
        )
        quotembed.add_field(name="Quote:", value=session["quote"])
        quotembed.add_field(name="Character:", value=session["character"])
        quotembed.add_field(name="Series:", value=session["anime"])
        quotembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=quotembed)

def setup(bot):
    bot.add_cog(Anime(bot))