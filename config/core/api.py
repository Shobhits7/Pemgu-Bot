import discord, os, io
from discord.ext import commands

class API(commands.Cog, description="Some cool commands that uses internet"):
    def __init__(self, bot):
        self.bot = bot
        headers=self.dagpi_headers = {
            "Authorization": os.getenv("DAGPI")
        }

    # Roast
    @commands.command(name="roast", aliases=["rst"], help="Will roast you or the given user")
    async def roast(self, ctx, user:commands.UserConverter = None):
        user = user or ctx.author
        session = await self.bot.session.get("https://api.dagpi.xyz/data/roast", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        rstmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Roasting {user}",
            description=response['roast'],
            timestamp=ctx.message.created_at
        )
        rstmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=rstmbed)

    # Joke
    @commands.command(name="joke", aliases=["jk"], help="Will tell you a random joke")
    async def joke(self, ctx):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/joke", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        jkmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is a random joke",
            description=response["joke"],
            timestamp=ctx.message.created_at
        )
        jkmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=jkmbed)

    # 8Ball
    @commands.command(name="8ball", aliases=["8b"], help="Will give you a random answer", usage="<question>")
    async def _8ball(self, ctx, *, question):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/8ball", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        _8bmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is your answer",
            timestamp=ctx.message.created_at
        )
        _8bmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        _8bmbed.add_field(name="Your Question:", value=question)
        _8bmbed.add_field(name="Your Answer:", value=response["response"])
        await ctx.send(embed=_8bmbed)

    # Pixel
    @commands.command(name="pixel", aliases=["pxl"], help="Will make the given image pixelated", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def pixel(self, ctx, user:commands.UserConverter = None):
        user = user or ctx.author
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/pixel/?url={user.avatar.with_static_format('png').with_size(1024)}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        pxlmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} 's pixelated image",
            timestamp=ctx.message.created_at
        )
        pxlmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        pxlmbed.set_image(url="attachment://pixel.png")
        await ctx.send(file=discord.File(response, filename="pixel.png"), embed=pxlmbed)

    # Colors
    @commands.command(name="colors", aliases=["clrs"], help="Will give you the colors from the given image", usage="[user]")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def colors(self, ctx, user:commands.UserConverter = None):
        user = user or ctx.author
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/colors/?url={user.avatar.with_static_format('png').with_size(1024)}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        clrsmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} 's image colors",
            timestamp=ctx.message.created_at
        )
        clrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        clrsmbed.set_image(url="attachment://colors.png")
        await ctx.send(file=discord.File(response, filename="colors.png"), embed=clrsmbed)

    # Tweet
    @commands.command(name="tweet", aliases=["tw"], help="Will preview your tweet", usage="<username> <text>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def tweet(self, ctx, *, text, user:commands.UserConverter = None):
        user = user or ctx.author
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/tweet/?url={user.avatar.with_static_format('png').with_size(1024)}&username={ctx.author.name}&text={text}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        twmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"{user} 's tweet",
            timestamp=ctx.message.created_at
        )
        twmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        twmbed.set_image(url="attachment://tweet.png")
        await ctx.send(file=discord.File(response, filename="tweet.png"), embed=twmbed)

    # Screenshot
    @commands.command(name="screenshot", aliases=["ss"], help="Will give you a preview from the given website", usage="<website>")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def screenshot(self, ctx, *, website):
        session = await self.bot.session.get(F"https://api.screenshotmachine.com?key=a95edd&url={website}&dimension=1024x768")
        response = io.BytesIO(await session.read())
        session.close()
        ssmbed = discord.Embed(
            colour=self.bot.colour,
            title="Here is your screenshot",
            timestamp=ctx.message.created_at
        )
        ssmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        ssmbed.set_image(url="attachment://screenshot.png")
        await ctx.send(file=discord.File(response, filename="screenshot.png"), embed=ssmbed)

    # Pypi
    @commands.command(name="pypi", help="Will give information about the given lib in pypi")
    async def pypi(self, ctx, *, lib):
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
            **License:** {response['info']['license']}""", inline=False)
        pypimbed.add_field(name="Classifiers:", value=",\n    ".join(classifier for classifier in response['info']['classifiers']), inline=False)
        pypimbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/873478114183880704/887470965188091944/pypilogo.png")
        pypimbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pypimbed)

    @commands.group(name="rickandmorty", aliases=["ram"], help="Some Rick and Morty commands, use subcommands", invoke_without_command=True)
    async def rickandmorty(self, ctx):
        await ctx.send_help(ctx.command.cog)
    
    # Character
    @rickandmorty.command(name="character", aliases=["char"], help="Will show information about the given character", usage="<character's name>")
    async def character(self, ctx, *, character: str):
        session = await self.bot.session.get(F"https://rickandmortyapi.com/api/character/?name={character}")
        response = await session.json()
        ramchmbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at,
        )
        for x in response['results'][0]:
            ramchmbed.title= F"{x['name']} 's Information"
            ramchmbed.set_image(url=x['image'])
            ramchmbed.add_field(name="Stauts:", value=x['status'])
            ramchmbed.add_field(name="Species:", value=x['species'])
            ramchmbed.add_field(name="Type:", value="Unknown" if not x['type'] else x['type'])
            ramchmbed.add_field(name="Gender:", value=x['gender'])
            ramchmbed.add_field(name="Origin:", value='\n'.join([origin.name for origin in x['origin']]))
            ramchmbed.add_field(name="Location:", value='\n'.join([location.name for location in x['location']]))
            ramchmbed.add_field(name="Created:", value=x['created'])
            ramchmbed.add_field(name="URL:", value=x['url'])

    # Location
    @rickandmorty.command(name="location", aliases=["loc"], help="Will show information about the given location", usage="<location's name>")
    async def location(self, ctx, *, location: str):
        session = await self.bot.session.get("...")
        response = await session.json()

    # Episode
    @rickandmorty.command(name="episode", aliases=["ep"], help="Will show information about the given episode", usage="<episode's number>")
    async def episode(self, ctx, *, episode: int):
        session = await self.bot.session.get("...")
        response = await session.json()

def setup(bot):
    bot.add_cog(API(bot))
