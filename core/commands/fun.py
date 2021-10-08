import discord, os, io
from discord.ext import commands
import core.views.funview as fv

class Fun(commands.Cog, description="You sad?. Use these to at least have a smile"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {"Authorization": os.getenv("DAGPI")}

    # Roast
    @commands.command(name="roast", aliases=["rst"], help="Will roast you or the given user")
    async def roast(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get("https://api.dagpi.xyz/data/roast", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        rstmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Roasting {user}",
            description=response['roast'],
            timestamp=ctx.message.created_at
        )
        rstmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=rstmbed)

    # Joke
    @commands.command(name="joke", aliases=["jk"], help="Will tell you a random joke")
    async def joke(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/joke", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        jkmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is a random joke",
            description=response["joke"],
            timestamp=ctx.message.created_at
        )
        jkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=jkmbed)

    # 8Ball
    @commands.command(name="8ball", aliases=["8b"], help="Will give you a random answer")
    async def _8ball(self, ctx:commands.Context, *, question:str):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/8ball", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        _8bmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is your answer",
            timestamp=ctx.message.created_at
        )
        _8bmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        _8bmbed.add_field(name="Your Question:", value=question)
        _8bmbed.add_field(name="Your Answer:", value=response["response"])
        await ctx.send(embed=_8bmbed)

    # Tweet
    @commands.command(name="tweet", aliases=["tw"], help="Will preview your tweet")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def tweet(self, ctx:commands.Context, *, text:str, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/tweet/?url={user.avatar.with_format('png')}&username={user.name}&text={text}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        twmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} 's tweet",
            timestamp=ctx.message.created_at
        )
        twmbed.set_image(url="attachment://tweet.png")
        twmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(fp=response, filename="tweet.png"), embed=twmbed)
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