import discord
from discord.ext import commands
from config.utils.aiohttp import session_json

class Anime(commands.Cog, description="Some Weeb shit stuff"):
    def __init__(self, bot):
        self.bot = bot
    
    # Quote
    @commands.command(name="quote", help="Will send a anime quote")
    async def quote(self, ctx):
        await ctx.trigger_typing()
        async with self.bot.session as session:
            async with session.get("https://animechan.vercel.app/api/random/") as r:
                r.json()
        quotembed = discord.Embed(
            colour=self.bot.color,
            title="Here is your quote",
            timestamp=ctx.message.created_at
        )
        quotembed.add_field(name="Quote:", value=r["quote"])
        quotembed.add_field(name="Character:", value=r["character"])
        quotembed.add_field(name="Series:", value=r["anime"])
        quotembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=quotembed)

    # SFW
    @commands.command(name="sfw", help="Will send a random sfw waifu or husbando image if not specified")
    async def sfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/sfw/all/")
        sfwmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW Image",
            timestamp=ctx.message.created_at
        )
        sfwmbed.set_image(url=session["url"])
        sfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sfwmbed)

    # Waifu
    @commands.command(name="waifu", help="Will send a random sfw waifu image")
    async def waifu(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/sfw/waifu/")
        wambed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW Waifu Image",
            timestamp=ctx.message.created_at
        )
        wambed.set_image(url=session["url"])
        wambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=wambed)
    
    # SMaid
    @commands.command(name="smaid", help="Will send a random sfw maid image")
    async def smaid(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/sfw/maid/")
        smaidmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your SFW Maid Image",
            timestamp=ctx.message.created_at
        )
        smaidmbed.set_image(url=session["url"])
        smaidmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=smaidmbed)

    # NSFW
    @commands.command(name="nsfw", help="Will send a random nsfw waifu image")
    @commands.is_nsfw()
    async def nsfw(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/ero/")
        nsfwmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Image",
            timestamp=ctx.message.created_at
        )
        nsfwmbed.set_image(url=session["url"])
        nsfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=nsfwmbed)

    # Ass
    @commands.command(name="ass", help="Will send a random nsfw ass image")
    @commands.is_nsfw()
    async def ass(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/ass/")
        assmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Ass Image",
            timestamp=ctx.message.created_at
        )
        assmbed.set_image(url=session["url"])
        assmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=assmbed)

    # Ecchi
    @commands.command(name="ecchi", help="Will send a random nsfw ecchi image")
    @commands.is_nsfw()
    async def ecchi(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/ecchi/")
        ecchimbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Ecchi Image",
            timestamp=ctx.message.created_at
        )
        ecchimbed.set_image(url=session["url"])
        ecchimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=ecchimbed)

    # Ero
    @commands.command(name="ero", help="Will send a random nsfw ero image")
    @commands.is_nsfw()
    async def ero(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/ero/")
        erombed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Ero Image",
            timestamp=ctx.message.created_at
        )
        erombed.set_image(url=session["url"])
        erombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=erombed)

    # Hentai
    @commands.command(name="hentai", help="Will send a random nsfw hentai image")
    @commands.is_nsfw()
    async def hentai(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/hentai/")
        hentaimbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Hentai Image",
            timestamp=ctx.message.created_at
        )
        hentaimbed.set_image(url=session["url"])
        hentaimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=hentaimbed)

    # NMaid
    @commands.command(name="nmaid", help="Will send a random nsfw maid image")
    @commands.is_nsfw()
    async def nmaid(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/maid/")
        nmaidmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Maid Image",
            timestamp=ctx.message.created_at
        )
        nmaidmbed.set_image(url=session["url"])
        nmaidmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=nmaidmbed)

    # Milf
    @commands.command(name="milf", help="Will send a random nsfw milf image")
    @commands.is_nsfw()
    async def milf(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/milf/")
        milfmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Milf Image",
            timestamp=ctx.message.created_at
        )
        milfmbed.set_image(url=session["url"])
        milfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=milfmbed)

    # Oppai
    @commands.command(name="oppai", help="Will send a random nsfw oppai image")
    @commands.is_nsfw()
    async def oppai(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/oppai/")
        oppaimbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Oppai Image",
            timestamp=ctx.message.created_at
        )
        oppaimbed.set_image(url=session["url"])
        oppaimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=oppaimbed)

    # Oral
    @commands.command(name="oral", help="Will send a random nsfw oral image")
    @commands.is_nsfw()
    async def oral(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/oral/")
        oralmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Oral Image",
            timestamp=ctx.message.created_at
        )
        oralmbed.set_image(url=session["url"])
        oralmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=oralmbed)

    # Paizuri
    @commands.command(name="paizuri", help="Will send a random nsfw paizuri image")
    @commands.is_nsfw()
    async def paizuri(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/paizuri/")
        paizurimbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Paizuri Image",
            timestamp=ctx.message.created_at
        )
        paizurimbed.set_image(url=session["url"])
        paizurimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=paizurimbed)

    # Selfies
    @commands.command(name="selfies", help="Will send a random nsfw selfies image")
    @commands.is_nsfw()
    async def selfies(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/selfies/")
        selfiesmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Selfies Image",
            timestamp=ctx.message.created_at
        )
        selfiesmbed.set_image(url=session["url"])
        selfiesmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=selfiesmbed)

    # Uniform
    @commands.command(name="uniform", help="Will send a random nsfw uniform image")
    @commands.is_nsfw()
    async def uniform(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.waifu.im/nsfw/uniform/")
        uniformmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your NSFW Uniform Image",
            timestamp=ctx.message.created_at
        )
        uniformmbed.set_image(url=session["url"])
        uniformmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=uniformmbed)

def setup(bot):
    bot.add_cog(Anime(bot))