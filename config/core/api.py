import discord
from discord.ext import commands
from config.utils.aiohttp import session_json, session_text, session_bytes
import os
import datetime

class API(commands.Cog, name="API 🌐", description="Some cool API commands"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {
            "Authorization": os.getenv("DAGPI")
        }

# Dagpi
    # Data
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
        jkmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=jkmbed)

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
        _8bmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        _8bmbed.add_field(name="Your Question:", value=question)
        _8bmbed.add_field(name="Your Answer:", value=session["response"])
        await ctx.reply(embed=_8bmbed)

    # Image
        # Pixel
    @commands.command(name="pixel", aliases=["pxl"], help="Will make the given image pixelated", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def pixel(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/pixel/?url={user.avatar_url_as(static_format='png', size=1024)}", self.dagpi_headers)
        pxlmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is the pixelated for the image",
            timestamp=ctx.message.created_at
        )
        pxlmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        pxlmbed.set_image(url="attachment://pixel.png")
        await ctx.reply(file=discord.File(session, filename="pixel.png"), embed=pxlmbed)
    
        # Mirror
    @commands.command(name="mirror", aliases=["mr"], help="Will make the given picture mirrored", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def mirror(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/mirror/?url={user.avatar_url_as(static_format='png', size=1024)}", self.dagpi_headers)
        mrmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is mirrored for the image",
            timestamp=ctx.message.created_at
        )
        mrmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        mrmbed.set_image(url="attachment://mirror.png")
        await ctx.reply(file=discord.File(session, filename="mirror.png"), embed=mrmbed)

        # Flip
    @commands.command(name="flip", aliases=["fi"], help="Will make the given picture flipped", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def flip(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/flip/?url={user.avatar_url_as(static_format='png', size=1024)}", self.dagpi_headers)
        fimbed = discord.Embed(
            colour=self.bot.color,
            title="Here is flipped for the image",
            timestamp=ctx.message.created_at
        )
        fimbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        fimbed.set_image(url="attachment://flip.png")
        await ctx.reply(file=discord.File(session, filename="flip.png"), embed=fimbed)

        # Colors
    @commands.command(name="colors", aliases=["clrs"], help="Will give you the colors from the given image", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def colors(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/colors/?url={user.avatar_url_as(static_format='png', size=1024)}", self.dagpi_headers)
        clrsmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is the colors for the image",
            timestamp=ctx.message.created_at
        )
        clrsmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        clrsmbed.set_image(url="attachment://colors.png")
        await ctx.reply(file=discord.File(session, filename="colors.png"), embed=clrsmbed)

        # RGB
    @commands.command(name="rgb", help="Will give you rgb information about the given image", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def rbg(self, ctx, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/rgb/?url={user.avatar_url_as(static_format='png', size=1024)}", self.dagpi_headers)
        rgbmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is the rgb info for the image",
            timestamp=ctx.message.created_at
        )
        rgbmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        rgbmbed.set_image(url="attachment://rgb.png")
        await ctx.reply(file=discord.File(session, filename="rgb.png"), embed=rgbmbed)

        # Tweet
    @commands.command(name="tweet", aliases=["tw"], help="Will preview your tweet", usage="<username> <text>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def tweet(self, ctx, *, text, user:commands.UserConverter = None):
        await ctx.trigger_typing()
        user = user or ctx.author
        session = await session_bytes(F"https://api.dagpi.xyz/image/tweet/?url={user.avatar_url_as(static_format='png', size=1024)}&username={ctx.author.name}&text={text}", self.dagpi_headers)
        twmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your tweet's preview",
            timestamp=ctx.message.created_at
        )
        twmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        twmbed.set_image(url="attachment://tweet.png")
        await ctx.reply(file=discord.File(session, filename="tweet.png"), embed=twmbed)

# Other
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
        ssmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        ssmbed.set_image(url="attachment://screenshot.png")
        await ctx.reply(file=discord.File(session, filename="screenshot.png"), embed=ssmbed)
    
    # Code
    @commands.command(name="code", aliases=["cd"], help="Will give you a preview from your code", usage="<code>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def code(self, ctx, *code):
        await ctx.trigger_typing()
        session = await session_bytes(F"https://carbonnowsh.herokuapp.com/?code={code}&paddingVertical=56px&paddingHorizontal=56px&backgroundImage=none&backgroundImageSelection=none&backgroundMode=color&backgroundColor=rgba(88, 89, 185, 100)&dropShadow=true&dropShadowOffsetY=20px&dropShadowBlurRadius=68px&theme=seti&windowTheme=none&language=auto&fontFamily=Hack&fontSize=16px&lineHeight=133%&windowControls=true&widthAdjustment=true&lineNumbers=true&firstLineNumber=0&exportSize=2x&watermark=false&squaredImage=false&hiddenCharacters=false&name=Hello World&width=680")
        cdmbed = discord.Embed(
            colour=self.bot.color,
            title="Here is your preview for the code",
            timestamp=ctx.message.created_at
        )
        cdmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        cdmbed.set_image(url="attachment://code.png")
        await ctx.reply(file=discord.File(session, filename="code.png"), embed=cdmbed)

# Dinosaur API
    # Chat
    @commands.command(name="chat", aliases=["ct"], help="Will say something depend on your message", usage="<text>")
    async def chat(self, ctx, *, text):
        await ctx.trigger_typing()
        session = await session_text(F"https://dinosaur.ml/misc/chatbot/?msg={text}")
        if not session["msg"]:
            pass
        await ctx.reply(session["msg"])
    
    # Sarcasm
    @commands.command(name="sarcasm", aliases=["sc"], help="Will make your message sarcasm", usage="<text>")
    async def sarcasm(self, ctx, *, text):
        await ctx.trigger_typing()
        session = await session_text(F"https://dinosaur.ml/misc/sarcastic/?text={text}")
        await ctx.reply(session["message"])        

    # Coinflip
    @commands.command(name="coinflip", aliases=["cf"], help="Will do a coinflip")
    async def coinFlip(self, ctx):
        await ctx.trigger_typing()
        session = await session_text("https://dinosaur.ml/random/coinflip/")
        cfmbed = discord.Embed(
            colour=self.bot.color,
            title=F"You got {session['side']}",
            timestamp=ctx.message.created_at
        )
        cfmbed.set_image(url=session['image'])
        cfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=cfmbed)

    # Bitcoin
    @commands.command(name="bitcoin", aliases=["bc"], help="Will show the current worth of Bitcoin")
    async def bitcoin(self, ctx):
        await ctx.trigger_typing()
        session = await session_text("https://dinosaur.ml/cryptocurrency/bitcoin/")
        bcmbed = discord.Embed(
            colour=self.bot.color,
            title="Bitcoin Information",
            timestamp=ctx.message.created_at
        )
        bcmbed.add_field(name="Coin type:", value=F"{session['coin']}", inline=False)
        bcmbed.add_field(name="Updated at:", value=F"{session['updated_at']}\uFEFF", inline=False)
        bcmbed.add_field(name="USD:", value=F"{session['USD']}", inline=False)
        bcmbed.add_field(name="GBP:", value=F"{session['GBP']}", inline=False)
        bcmbed.add_field(name="EUR:", value=F"{session['EUR']}", inline=False)
        bcmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=bcmbed)


    # Color
    @commands.command(name="color", aliases=["clr"], help="Will send the preview for the given color", usage="<hex>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def color(self, ctx, *, hex):
        await ctx.trigger_typing()
        if "#" in hex:
            hex = hex[1:]
        session = await session_bytes(F"https://dinosaur.ml/misc/colorviewer/?hex={hex}")
        clrmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Here is the color for {hex}",
            timestamp=ctx.message.created_at
        )
        clrmbed.set_image(url="attachment://colors.png")
        clrmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.reply(file=discord.File(session, filename="colors.png"), embed=clrmbed)

def setup(bot):
    bot.add_cog(API(bot))