import discord
from discord.ext import commands
from core.utils.pagination import Paginator

class Anime(commands.Cog, description="Some Weeb shit?!"):
    def __init__(self, bot):
        self.bot = bot
    
    # Quote
    @commands.command(name="quote", help="Will send a anime quote")
    async def quote(self, ctx:commands.Context):
        embeds = []
        for _ in range(0, 6):
            session = await self.bot.session.get("https://animechan.vercel.app/api/random/")
            response = await session.json()
            session.close()
            quotembed = discord.Embed(
                color=self.bot.color,
                title="Here is your quote",
                timestamp=ctx.message.created_at
            )
            quotembed.add_field(name="Quote:", value=response["quote"])
            quotembed.add_field(name="Character:", value=response["character"])
            quotembed.add_field(name="Series:", value=response["anime"])
            quotembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            embeds.append(quotembed)
        view = Paginator(ctx, embeds)
        view.message = await ctx.send(content="Use the buttons for changing the page", embed=embeds[0], view=view)

    # SFW
    @commands.group(name="sfw", help="Consider using subcommands", invoke_without_command=True)
    async def sfw(self, ctx:commands.Context):
        await ctx.send_help("sfw")

    # SFW-Waifu
    @sfw.command(name="waifu", help="Will send a random sfw waifu image")
    async def waifu(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/sfw/waifu/")
        response = await session.json()
        session.close()
        wambed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your SFW Waifu Image",
            timestamp=ctx.message.created_at
        )
        wambed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        wambed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=wambed)
    
    # SFW-Maid
    @sfw.command(name="maid", help="Will send a random sfw maid image")
    async def smaid(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/sfw/maid/")
        response = await session.json()
        session.close()
        smaidmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your SFW Maid Image",
            timestamp=ctx.message.created_at
        )
        smaidmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        smaidmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=smaidmbed)
    
    # NSFW
    @commands.group(name="nsfw", help="Consider using subcommands", invoke_without_command=True)
    @commands.is_nsfw()
    async def nsfw(self, ctx:commands.Context):
        await ctx.send_help("nsfw")

    # NSFW-Ass
    @nsfw.command(name="ass", help="Will send a random nsfw thicc image")
    @commands.is_nsfw()
    async def ass(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/ass/")
        response = await session.json()
        session.close()
        assmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Ass Image",
            timestamp=ctx.message.created_at
        )
        assmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        assmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=assmbed)

    # NSFW-Ecchi
    @nsfw.command(name="ecchi", help="Will send a random nsfw ecchi image")
    @commands.is_nsfw()
    async def ecchi(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/ecchi/")
        response = await session.json()
        session.close()
        ecchimbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Ecchi Image",
            timestamp=ctx.message.created_at
        )
        ecchimbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        ecchimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=ecchimbed)

    # NSFW-Ero
    @nsfw.command(name="ero", help="Will send a random nsfw ero image")
    @commands.is_nsfw()
    async def ero(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/ero/")
        response = await session.json()
        session.close()
        erombed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Ero Image",
            timestamp=ctx.message.created_at
        )
        erombed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        erombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=erombed)

    # NSFW-Hentai
    @nsfw.command(name="hentai", help="Will send a random nsfw hentai image")
    @commands.is_nsfw()
    async def hentai(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/hentai/")
        response = await session.json()
        session.close()
        hentaimbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Hentai Image",
            timestamp=ctx.message.created_at
        )
        hentaimbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        hentaimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=hentaimbed)

    # NSFW-Maid
    @nsfw.command(name="maid", help="Will send a random nsfw maid image")
    @commands.is_nsfw()
    async def nmaid(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/maid/")
        response = await session.json()
        session.close()
        nmaidmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Maid Image",
            timestamp=ctx.message.created_at
        )
        nmaidmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        nmaidmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=nmaidmbed)

    # NSFW-Milf
    @nsfw.command(name="milf", help="Will send a random nsfw milf image")
    @commands.is_nsfw()
    async def milf(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/milf/")
        response = await session.json()
        session.close()
        milfmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Milf Image",
            timestamp=ctx.message.created_at
        )
        milfmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        milfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=milfmbed)

    # NSFW-Oppai
    @nsfw.command(name="oppai", help="Will send a random nsfw oppai image")
    @commands.is_nsfw()
    async def oppai(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/ero/")
        response = await session.json()
        session.close()
        oppaimbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Oppai Image",
            timestamp=ctx.message.created_at
        )
        oppaimbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        oppaimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=oppaimbed)

    # NSFW-Oral
    @nsfw.command(name="oral", help="Will send a random nsfw oral image")
    @commands.is_nsfw()
    async def oral(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/oral/")
        response = await session.json()
        session.close()
        oralmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Oral Image",
            timestamp=ctx.message.created_at
        )
        oralmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        oralmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=oralmbed)

    # NSFW-Paizuri
    @nsfw.command(name="paizuri", help="Will send a random nsfw paizuri image")
    @commands.is_nsfw()
    async def paizuri(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/paizuri/")
        response = await session.json()
        session.close()
        paizurimbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Paizuri Image",
            timestamp=ctx.message.created_at
        )
        paizurimbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        paizurimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=paizurimbed)

    # NSFW-Selfies
    @nsfw.command(name="selfies", help="Will send a random nsfw selfies image")
    @commands.is_nsfw()
    async def selfies(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/selfies/")
        response = await session.json()
        session.close()
        selfiesmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Selfies Image",
            timestamp=ctx.message.created_at
        )
        selfiesmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        selfiesmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=selfiesmbed)

    # NSFW-Uniform
    @nsfw.command(name="uniform", help="Will send a random nsfw uniform image")
    @commands.is_nsfw()
    async def uniform(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/uniform/")
        response = await session.json()
        session.close()
        uniformmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Uniform Image",
            timestamp=ctx.message.created_at
        )
        uniformmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        uniformmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=uniformmbed)

def setup(bot):
    bot.add_cog(Anime(bot))