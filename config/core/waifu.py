import discord
from discord.ext import commands
from config.utils.aiohttp import session_json

class Anime(commands.Cog, description="SFW Waifu's and Husbando's chamber"):
    def __init__(self, bot):
        self.bot = bot
    
    # SFW
    @commands.group(name="sfw", help="Will send an random sfw waifu or husbando image if not specified", usage="[waifu|wa|husbando|ha]", invoke_without_command=True)
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
    # SFW Waifu
    @sfw.command(name="waifu", aliases=["wa"], help="Will send an random waifu image")
    async def waifu_sfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.hori.ovh/sfw/waifu/")
        sfwwambed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW Waifu Image",
            timestamp=ctx.message.created_at
        )
        sfwwambed.set_image(url=session["url"])
        sfwwambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sfwwambed)

    # NSFW
    @commands.group(name="nsfw", help="Will send an random nsfw waifu or husbando image if nor specified", usage="[ass|ecchi|ero|hentai|maid|milf|oppai|oral|paizuri|selfies|uniform]", invoke_without_command=True)
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