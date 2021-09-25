import discord
from discord.ext import commands

class Setup(commands.Cog, description="For setting up the bot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.command(name="prefix", aliases=["pf"], help="Will tell you the prefix for this guild", invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx:commands.Context):
        pfmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"My Prefix here is `{self.bot.prefix}`",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pfmbed)

def setup(bot):
    bot.add_cog(Setup(bot))
