import discord, os
from discord.ext import commands
from ..utils.aiohttp import session_json, session_text, session_bytes

class API(commands.Cog, description="Some cool API commands"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {
            "Authorization": os.getenv("DAGPI")
        }
    
    # Joke
    @commands.command(name="joke", aliases=["jk"], help="Will tell you a random joke")
    async def joke(self, ctx):
        await ctx.trigger_typing()
        session = await session_json("https://api.dagpi.xyz/data/joke", self.dagpi_headers)
        jkmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is a random joke",
            description=session["joke"],
            timestamp=ctx.message.created_at
        )
        jkmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=jkmbed)

    # 8Ball
    @commands.command(name="8ball", aliases=["8b"], help="Will give you a random answer", usage="<question>")
    async def _8ball(self, ctx, *, question):
        await ctx.trigger_typing()
        session = await session_json("https://api.dagpi.xyz/data/8ball", self.dagpi_headers)
        _8bmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your answer",
            timestamp=ctx.message.created_at
        )
        _8bmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        _8bmbed.add_field(name="Your Question:", value=question)
        _8bmbed.add_field(name="Your Answer:", value=session["response"])
        await ctx.send(embed=_8bmbed)

    # Pixel
    @commands.command(name="pixel", aliases=["pxl"], help="Will make the given image pixelated", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def pixel(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/pixel/?url={user.avatar.with_static_format('png').with_size(1024)}", self.dagpi_headers)
        pxlmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is the pixelated for the image",
            timestamp=ctx.message.created_at
        )
        pxlmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        pxlmbed.set_image(url="attachment://pixel.png")
        await ctx.send(file=discord.File(session, filename="pixel.png"), embed=pxlmbed)

    # Colors
    @commands.command(name="colors", aliases=["clrs"], help="Will give you the colors from the given image", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def colors(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/colors/?url={user.avatar.with_static_format('png').with_size(1024)}", self.dagpi_headers)
        clrsmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is the colors for the image",
            timestamp=ctx.message.created_at
        )
        clrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        clrsmbed.set_image(url="attachment://colors.png")
        await ctx.send(file=discord.File(session, filename="colors.png"), embed=clrsmbed)

    # Tweet
    @commands.command(name="tweet", aliases=["tw"], help="Will preview your tweet", usage="<username> <text>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def tweet(self, ctx, *, text, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/tweet/?url={user.avatar.with_static_format('png').with_size(1024)}&username={ctx.author.name}&text={text}", self.dagpi_headers)
        twmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your tweet's preview",
            timestamp=ctx.message.created_at
        )
        twmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        twmbed.set_image(url="attachment://tweet.png")
        await ctx.send(file=discord.File(session, filename="tweet.png"), embed=twmbed)

    # Screenshot
    @commands.command(name="screenshot", aliases=["ss"], help="Will give you a preview from the given website", usage="<website>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def screenshot(self, ctx, *, website):
        await ctx.trigger_typing()
        session = await session_bytes(F"https://api.screenshotmachine.com?key=a95edd&url={website}&dimension=1024x768")
        ssmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your screenshot",
            timestamp=ctx.message.created_at
        )
        ssmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        ssmbed.set_image(url="attachment://screenshot.png")
        await ctx.send(file=discord.File(session, filename="screenshot.png"), embed=ssmbed)

    # Pypi
    @commands.command(name="pypi", help="Will give information about the given lib in pypi")
    async def pypi(self, ctx, *, lib):
        await ctx.trigger_typing()
        session = await session_json(F"https://pypi.org/pypi/{lib}/json")
        pypimbed = discord.Embed(
            colour=self.bot.color,
            url=session['info']['package_url'],
            title=session['info']['name'],
            description=session['info']['summary']
        )
        pypimbed.add_field(name="Author Info:", value=F"Name: {session['info']['author']}\nEmail:{session['info']['author_email']}", inline=False)
        # pypimbed.add_field(name="Maintainer Info:", value=F"Name: {session['info']['maintainer']}\nEmail: {session['maintainer_email']}")
        pypimbed.add_field(name="Package Info:", value=F"""Version: {session['info']['version']}
Download URL: {session['info']['download_url']}
Documentation URL: {session['info']['docs_url']}
Home Page: {session['info']['home_page']}
Yanked: {session['info']['yanked']} - {session['info']['yanked_reason']}
Keywords: {session['info']['keywords']}
License: {session['info']['license']}
Classifiers: {', '.join(classifier for classifier in session['info']['classifiers'])}""", inline=False)
        pypimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pypimbed)

def setup(bot):
    bot.add_cog(API(bot))
