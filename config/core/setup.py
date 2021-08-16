import discord
from discord.ext import commands
from config.utils.json import read_json, write_json

class Setup(commands.Cog, description="For setting up the bot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.command(name="prefix", aliases=["pf"], help="Will change the prefix", usage="<prefix>")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx, *, pre="~b"):
        pfmbed = discord.Embed(
            colour=self.bot.color,
            title="Prefix",
            description=F"The guild prefix has been changed to `{pre}`",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if not pre:
            pass
        elif pre:
            data = read_json("prefixes")
            data[str(ctx.guild.id)] = pre
            write_json(data, "prefixes")
            await ctx.reply(embed=pfmbed)

def setup(bot):
    bot.add_cog(Setup(bot))
