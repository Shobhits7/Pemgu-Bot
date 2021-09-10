import discord
from discord.ext import commands
from config.utils.aiohttp import session_json

class Anime(commands.Cog, description="SFW Waifu's and Husbando's chamber"):
    def __init__(self, bot):
        self.bot = bot
    
    # SFW
    @commands.command(name="sfw", help="Will send an random sfw waifu or husbando image if not specified")
    async def sfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.hori.ovh/sfw/all/")
        sfwmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW Image",
            timestamp=ctx.message.created_at
        )
        sfwmbed.set_image(url=session["url"])
        sfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sfwmbed)

    # Waifu
    @commands.command(name="waifu", aliases=["wa"], help="Will send an random sfw waifu image")
    async def waifu_sfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.hori.ovh/sfw/waifu/")
        wambed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW Waifu Image",
            timestamp=ctx.message.created_at
        )
        wambed.set_image(url=session["url"])
        wambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=wambed)

    # NSFW
    @commands.command(name="nsfw", help="Will send an random nsfw waifu or husbando image if nor specified")
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.hori.ovh/nsfw/ero/")
        nsfwmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Image",
            timestamp=ctx.message.created_at
        )
        nsfwmbed.set_image(url=session["url"])
        nsfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=nsfwmbed)

def setup(bot):
    bot.add_cog(Anime(bot))