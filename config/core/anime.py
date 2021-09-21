import discord
from discord.ext import commands

class Anime(commands.Cog, description="Some Weeb shit"):
    def __init__(self, bot):
        self.bot = bot
    
    # Quote
    @commands.command(name="quote", help="Will send a anime quote")
    async def quote(self, ctx):
        session = await self.bot.session.get("https://animechan.vercel.app/api/random/")
        response = await session.json()
        session.close()
        quotembed = discord.Embed(
            colour=self.bot.colour,
            title="Here is your quote",
            timestamp=ctx.message.created_at
        )
        quotembed.add_field(name="Quote:", value=response["quote"])
        quotembed.add_field(name="Character:", value=response["character"])
        quotembed.add_field(name="Series:", value=response["anime"])
        quotembed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=quotembed)

    # SFW
    @commands.group(name="sfw", help="Will send a random sfw waifu or husbando image if not specified", invoke_without_command=True)
    async def sfw(self, ctx):
        session = await self.bot.session.get("https://api.waifu.im/sfw/all/")
        response = await session.json()
        session.close()
        sfwmbed = discord.Embed(
            colour=self.bot.colour,
            url=F"https://waifu.im/preview/?image={response['file']}",
            title="Here is your SFW Image",
            timestamp=ctx.message.created_at
        )
        sfwmbed.set_image(url=response["url"])
        sfwmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=sfwmbed)

    # Waifu
    @sfw.command(name="waifu", help="Will send a random sfw waifu image")
    async def waifu(self, ctx):
        session = await self.bot.session.get("https://api.waifu.im/sfw/waifu/")
        response = await session.json()
        session.close()
        wambed = discord.Embed(
            colour=self.bot.colour,
            url=F"https://waifu.im/preview/?image={response['file']}",
            title="Here is your SFW Waifu Image",
            timestamp=ctx.message.created_at
        )
        wambed.set_image(url=response["url"])
        wambed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=wambed)
    
    # SMaid
    @sfw.command(name="maid", help="Will send a random sfw maid image")
    async def smaid(self, ctx):
        session = await self.bot.session.get("https://api.waifu.im/sfw/maid/")
        response = await session.json()
        session.close()
        smaidmbed = discord.Embed(
            colour=self.bot.colour,
            url=F"https://waifu.im/preview/?image={response['file']}",
            title="Here is your SFW Maid Image",
            timestamp=ctx.message.created_at
        )
        smaidmbed.set_image(url=response["url"])
        smaidmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=smaidmbed)

def setup(bot):
    bot.add_cog(Anime(bot))