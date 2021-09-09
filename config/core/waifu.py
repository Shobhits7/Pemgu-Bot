import discord
from discord.ext import commands
from config.utils.aiohttp import session_json

class Anime(commands.Cog, description="SFW Waifu's and Husbando's chamber"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(name="sfw", help="Will send an random waifu or husbando image if not specified", invoke_without_command=True)
    async def sfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.hori.ovh/sfw/all/")
        sfwmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW All Image",
            timestamp=ctx.message.created_at
        )
        sfwmbed.set_image(url=session["url"])
        sfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sfwmbed)

def setup(bot):
    bot.add_cog(Anime(bot))