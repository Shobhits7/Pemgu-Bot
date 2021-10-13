import discord
from discord.ext import commands

class Utility(commands.Cog, description="Useful stuff that are open to everyone"):
    def __init__(self, bot):
        self.bot = bot

    # Cleanup
    @commands.command(name="cleanup", aliases=["cu"], help="Will delete bot's messagess")
    async def cleanup(self, ctx:commands.Context, *, amount:int):
        cumbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Cleaned-up {amount} of bot messages",
        )
        cumbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.channel.purge(limit=amount+1, check=lambda m: m.author.id == self.bot.user.id, bulk=False)
        await ctx.send(embed=cumbed, delete_after=5)

    # PYPI
    @commands.command(name="pypi", help="Will give information about the given library in PYPI")
    async def pypi(self, ctx:commands.Context, *, library:str):
        pypimbed = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        pypimbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        session = await self.bot.session.get(F"https://pypi.org/pypi/{library}/json")
        if session.status != 200:
            pypimbed.title = "Couldn't find that library in PYPI"
            return await ctx.send(embed=pypimbed)
        response = await session.json()
        session.close()
        pypimbed.url = response['info']['package_url'],
        pypimbed.title = response['info']['name'],
        pypimbed.description = response['info']['summary'],
        pi = [
            F"***Version:*** {response['info']['version']}",
            F"***Download URL:*** {response['info']['download_url']}",
            F"***Documentation URL:*** {response['info']['docs_url']}",
            F"***Home Page:*** {response['info']['home_page']}",
            F"***Yanked:*** {response['info']['yanked']} - {response['info']['yanked_reason']}",
            F"***Keywords:*** {response['info']['keywords']}",
            F"***License:*** {response['info']['license']}"
        ]
        pypimbed.add_field(name="Author Info:", value=F"Name: {response['info']['author']}\nEmail:{response['info']['author_email']}", inline=False)
        pypimbed.add_field(name="Package Info:", value="\n".join(p for p in pi), inline=False)
        pypimbed.add_field(name="Classifiers:", value=",\n    ".join(classifier for classifier in response['info']['classifiers']), inline=False)
        await ctx.send(embed=pypimbed)

    # AFK
    @commands.command(name="afk", help="Will make you AFK")
    @commands.guild_only()
    @commands.has_guild_permissions(change_nickname=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def afk(self, ctx:commands.Context):
        afkmbed  = discord.Embed(
            colour=self.bot.colour,
            timestamp=ctx.message.created_at
        )
        afkmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if ctx.author.nick == "AFK":
            afkmbed.title = "Name has been changed to it's original"
            await ctx.author.edit(nick=None)
            return await ctx.send(embed=afkmbed)
        afkmbed.title = "Doing AFK"
        afkmbed.description = "Name has been now changed to AFK"
        await ctx.author.edit(nick="AFK")
        await ctx.send(embed=afkmbed)
        if ctx.author.voice:
            afkmbed.description += "\nNow moving you to AFK voice channel"
            await ctx.author.move_to(ctx.guild.afk_channel)

def setup(bot):
    bot.add_cog(Utility(bot))