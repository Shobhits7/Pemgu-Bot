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
    @commands.command(name="sfw", help="Will send and random SFW Waifu Image")
    async def sfw(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/sfw/waifu/")
        response = await session.json()
        session.close()
        sfwmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your SFW Image",
            timestamp=ctx.message.created_at
        )
        sfwmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        sfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=sfwmbed)
    
    # NSFW
    @commands.group(name="nsfw", help="Will send and random NSFW Waifu Image")
    @commands.is_nsfw()
    async def nsfw(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.waifu.im/nsfw/ero/")
        response = await session.json()
        session.close()
        nsfwmbed = discord.Embed(
            color=self.bot.color,
            url=F"https://waifu.im/preview/?image={response.get('tags')[0].get('images')[0].get('file')}",
            title="Here is your NSFW Image",
            timestamp=ctx.message.created_at
        )
        nsfwmbed.set_image(url=response.get('tags')[0].get('images')[0].get('url'))
        nsfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=nsfwmbed)

def setup(bot):
    bot.add_cog(Anime(bot))