import discord, os, io, random, typing
from discord.ext import commands
import core.views.funview as fv
class Fun(commands.Cog, description="You sad? Use these to at least have a smile!"):
    def __init__(self, bot):
        self.bot = bot
        self.dagpi_headers = {"Authorization": os.getenv("DAGPI")}

    # Say
    @commands.command(name="say", help="Will say your text")
    async def say(self, ctx:commands.Context, *, text:str):
        await ctx.send(F"{text} | {ctx.author.mention}")

    # Sarcasm
    @commands.command(name="sarcasm", help="Will say your text in a sarcastic way")
    async def sarcasm(self, ctx:commands.Context, *, text:str):
        await ctx.send(F"{''.join(c.upper() if i % 2 == 0 else c for i, c in enumerate(text))} | {ctx.author.mention}")

    # PP
    @commands.command(name="pp", help="Will tell your or the given user's pp size")
    async def pp(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        ppmbed = discord.Embed(
            color=self.bot.color,
            title=F"{user}'s PP Size:",
            description=F"8{'='*random.randint(1, 69)}D",
            timestamp=ctx.message.created_at
        )
        ppmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=ppmbed)

    # Ship
    @commands.command(name="ship", aliases=["sp"], help="Will ship you or the given member with the other given member")
    async def ship(self, ctx:commands.Context, member1:discord.Member, member2:discord.Member=None):
        spmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        spmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if member2: spmbed.title = F"Shipping {member1} with {member2}"
        else: spmbed.title = F"Shipping {ctx.author} with {member1}"
        number = random.randint(1, 100)
        if number < 25:  spmbed.description = F"`{number}%` - Can't see any love 💔"
        elif number >= 25 and number < 50:  spmbed.description = F"`{number}%` - Can see a sparkle 💖"
        elif number >= 50 and number <= 75:  spmbed.description = F"`{number}%` - I can see pumping 💓"
        elif number > 75:  spmbed.description = F"`{number}%` - CanI can see a lot of love 💘"
        await ctx.send(embed=spmbed)

    # Snipe
    @commands.command(name="snipe", aliases=["se"], help="Will give you the last deleted message in this channel", hidden=True)
    @commands.guild_only()
    async def snipe(self, ctx:commands.Context, number:int=None):
        number = 0 if not number else number
        snipe = self.bot.dsnipe.get(str(ctx.channel.id))
        sembed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        sembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if snipe:
            msg = snipe[::-1][number].get("msg")
            sembed.set_author(name=F"{msg.author} ({msg.author.id}) said in {msg.channel}", icon_url=msg.author.display_avatar.url, url=msg.jump_url)
            sembed.description = "Message didn't have content..." if not msg.content else msg.content
            sembed.set_image(url=msg.attachments[0].url)
            es = [sembed]
            if msg.embed:
                es.append(msg.embed)
            return await ctx.send(embeds=es)
        sembed.title = "There is no deleted message in this channel"
        await ctx.send(embed=sembed)

    # Counter
    @commands.command(name="counter", aliases=["ctr"], help="Will start an counter")
    async def counter(self, ctx:commands.Context):
        ctrmbed = discord.Embed(
            color=self.bot.color,
            description="Click the button for counting",
            timestamp=ctx.message.created_at
        )
        ctrmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = fv.CounterView(ctx)
        view.message = await ctx.send(embed=ctrmbed, view=view)

    # Nitro
    @commands.command(name="nitro", help="Will gift free Nitro")
    async def nitro(self, ctx:commands.Context):
        bnitrombed = discord.Embed(
            color=self.bot.color,
            title="A WILD NITRO GIFT APPEARS?!",
            description="Expires in 48 hours\nClick the button for claiming Nitro:.",
            timestamp=ctx.message.created_at
        )
        bnitrombed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        view = fv.NitroView(ctx)
        view.message = await ctx.send(embed=bnitrombed, view=view)

    # Token
    @commands.command(name="token", aliases=["tn"], help="Will send an random token")
    async def token(self, ctx:commands.Context):
        session = await self.bot.session.get("https://some-random-api.ml/bottoken")
        response = await session.json()
        session.close()
        tnmbed = discord.Embed(
            color=self.bot.color,
            title="Here is your token",
            description=response['token'],
            timestamp=ctx.message.created_at
        )
        tnmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=tnmbed)

    # Meme
    @commands.command(name="meme", aliases=["me"], help="Will show a random meme")
    async def meme(self, ctx:commands.Context):
        session = await self.bot.session.get("https://some-random-api.ml/meme")
        response = await session.json()
        session.close()
        membed = discord.Embed(
            color=self.bot.color,
            title="Here is a random meme for you",
            description=F"{response['caption']} - {response['category'].title()}",
            timestamp=ctx.message.created_at
        )
        membed.set_image(url=response['image'])
        membed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=membed)

    # Joke
    @commands.command(name="joke", aliases=["jk"], help="Will tell you a random joke")
    async def joke(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/joke", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        jkmbed = discord.Embed(
            color=self.bot.color,
            title="Here is a random joke",
            description=response["joke"],
            timestamp=ctx.message.created_at
        )
        jkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=jkmbed)

    # Fact
    @commands.command(name="fact", aliases=["fc"], help="Will tell you a random fact")
    async def fact(self, ctx:commands.Context):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/fact", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        fcmbed = discord.Embed(
            color=self.bot.color,
            title="Here is a random fact",
            description=response["fact"],
            timestamp=ctx.message.created_at
        )
        fcmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=fcmbed)

    # 8Ball
    @commands.command(name="8ball", aliases=["8b"], help="Will give you a random answer")
    async def _8ball(self, ctx:commands.Context, *, question:str):
        session = await self.bot.session.get("https://api.dagpi.xyz/data/8ball", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        _8bmbed = discord.Embed(
            color=self.bot.color,
            title="Here is your answer",
            timestamp=ctx.message.created_at
        )
        _8bmbed.add_field(name="Your Question:", value=question)
        _8bmbed.add_field(name="Your Answer:", value=response["response"])
        _8bmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=_8bmbed)

    # Roast
    @commands.command(name="roast", aliases=["rt"], help="Will roast you or the given user")
    async def roast(self, ctx:commands.Context, user:discord.User=None):
        user = ctx.author if not user else user
        session = await self.bot.session.get("https://api.dagpi.xyz/data/roast", headers=self.dagpi_headers)
        response = await session.json()
        session.close()
        rtmbed = discord.Embed(
            color=self.bot.color,
            title=F"Roasting {user}",
            description=response['roast'],
            timestamp=ctx.message.created_at
        )
        rtmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=rtmbed)

    # Tweet
    @commands.command(name="tweet", aliases=["tw"], help="Will preview your tweet")
    @commands.bot_has_guild_permissions(attach_files=True)
    async def tweet(self, ctx:commands.Context, user:typing.Optional[discord.User]=None, *, text:str):
        user = ctx.author if not user else user
        session = await self.bot.session.get(F"https://api.dagpi.xyz/image/tweet/?url={user.avatar.with_format('png')}&username={user.name}&text={text}", headers=self.dagpi_headers)
        response = io.BytesIO(await session.read())
        session.close()
        twmbed = discord.Embed(
            color=self.bot.color,
            title=F"{user}'s tweet",
            timestamp=ctx.message.created_at
        )
        twmbed.set_image(url="attachment://tweet.png")
        twmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(fp=response, filename="tweet.png"), embed=twmbed)

def setup(bot):
    bot.add_cog(Fun(bot))