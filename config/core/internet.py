import discord, os, io
from discord.ext import commands

class Internet(commands.Cog, description="Some cool commands that uses internet"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {
            "Authorization": os.getenv("DAGPI")
        }

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
    @commands.command(name="8ball", aliases=["8b"], help="Will give you a random answer", usage="<question>")
    async def _8ball(self, ctx:commands.Context, question:str):
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

    # Pixel
    @commands.command(name="pixel", aliases=["pxl"], help="Will make the given image pixelated", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def pixel(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/pixel/?url={user.avatar.with_format('png')}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        pxlmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} 's pixelated image",
            timestamp=ctx.message.created_at
        )
        pxlmbed.set_image(url="attachment://pixel.png")
        pxlmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(response, filename="pixel.png"), embed=pxlmbed)

    # Colours
    @commands.command(name="colours", aliases=["clrs"], help="Will give you the colours from the given image", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def colours(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/colors/?url={user.avatar.with_format('png')}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        clrsmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} 's image colours",
            timestamp=ctx.message.created_at
        )
        clrsmbed.set_image(url="attachment://colours.png")
        clrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(response, filename="colours.png"), embed=clrsmbed)

    # Tweet
    @commands.command(name="tweet", aliases=["tw"], help="Will preview your tweet", usage="<username> <text>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def tweet(self, ctx:commands.Context, text:str, user:discord.User=None):
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
        await ctx.send(file=discord.File(response, filename="tweet.png"), embed=twmbed)

    # Screenshot
    @commands.command(name="screenshot", aliases=["ss"], help="Will give you a preview from the given website", usage="<website>")
    @commands.is_owner()
    @commands.bot_has_guild_permissions(attach_files=True)
    async def screenshot(self, ctx:commands.Context, website:str):
        session = await self.bot.session.get(F"https://api.screenshotmachine.com?key=a95edd&url={website}&dimension=1024x768")
        response = io.BytesIO(await session.read())
        session.close()
        ssmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is your screenshot",
            timestamp=ctx.message.created_at
        )
        ssmbed.set_image(url="attachment://screenshot.png")
        ssmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(response, filename="screenshot.png"), embed=ssmbed)

    # Pypi
    @commands.command(name="pypi", help="Will give information about the given lib in pypi")
    async def pypi(self, ctx:commands.Context, lib:str):
        session = await self.bot.session.get(F"https://pypi.org/pypi/{lib}/json")
        if session.status != 200:
            await ctx.send("Couldn't find that library in PYPI")
            return
        response = await session.json()
        session.close()
        pypimbed = discord.Embed(
            colour=self.bot.colour,
            url=response['info']['package_url'],
            title=response['info']['name'],
            description=response['info']['summary'],
            timestamp=ctx.message.created_at
        )
        pypimbed.add_field(name="Author Info:", value=F"Name: {response['info']['author']}\nEmail:{response['info']['author_email']}", inline=False)
        pypimbed.add_field(name="Package Info:", value=F"""**Version:** {response['info']['version']}
            **Download URL:** {response['info']['download_url']}
            **Documentation URL:** {response['info']['docs_url']}
            **Home Page:** {response['info']['home_page']}
            **Yanked:** {response['info']['yanked']} - {response['info']['yanked_reason']}
            **Keywords:** {response['info']['keywords']}
            **License:** {response['info']['license']}""".replace("\t", ""), inline=False)
        pypimbed.add_field(name="Classifiers:", value=",\n    ".join(classifier for classifier in response['info']['classifiers']), inline=False)
        pypimbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/873478114183880704/887470965188091944/pypilogo.png")
        pypimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pypimbed)

    @commands.group(name="rickandmorty", aliases=["ram"], help="Some Rick and Morty commands, use subcommands", invoke_without_command=True)
    async def rickandmorty(self, ctx:commands.Context):
        await ctx.send_help(ctx.command.cog)

    # Character
    @rickandmorty.command(name="character", aliases=["char"], help="Will show information about the given character", usage="<character's name>")
    async def character(self, ctx:commands.Context, character:str):
        session = await self.bot.session.get(F"https://rickandmortyapi.com/api/character/?name={character}")
        if session.status != 200:
            await ctx.send("Couldn't find that character in Rick And Morty")
            return
        response = await session.json()
        session.close()
        ramchmbed = discord.Embed(
            colour=self.bot.colour,
            url=response['results'][0]['url'],
            title=F"{response['results'][0]['name']} 's Information",
            timestamp=ctx.message.created_at,
        )
        ramchmbed.description = F"""
        Stauts: {response['results'][0]['status']}
        Species: {response['results'][0]['species']}
        Type: {'Unknown' if not response['results'][0]['type'] else response['results'][0]['type']}
        Gender: {response['results'][0]['gender']}
        Origin: {response['results'][0]['origin']['name']}
        Location: {response['results'][0]['location']['name']}
        Created: {response['results'][0]['created']}
        """.replace("\t", "")
        ramchmbed.set_image(url=response['results'][0]['image'])
        await ctx.send(embed=ramchmbed)

    # Location
    @rickandmorty.command(name="location", aliases=["loc"], help="Will show information about the given location", usage="<location's name>")
    async def location(self, ctx:commands.Context, location:str):
        session = await self.bot.session.get("...")
        response = await session.json()

    # Episode
    @rickandmorty.command(name="episode", aliases=["ep"], help="Will show information about the given episode", usage="<episode's number>")
    async def episode(self, ctx:commands.Context, episode:int):
        session = await self.bot.session.get("...")
        response = await session.json()

def setup(bot):
    bot.add_cog(Internet(bot))
