import discord
from discord.ext import commands
from config.utils.json import read_json, write_json

class Setup(commands.Cog, description="For setting up the bot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.group(name="prefix", aliases=["pf"], help="Will tell you the prefix for this guild", invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx):
        await ctx.trigger_typing()
        data = read_json("prefixes")
        if str(ctx.guild.id) in data:
            prefix = data[str(ctx.guild.id)]
        else:
            prefix = "~b"
        pfmbed = discord.Embed(
            colour=self.bot.color,
            title=F"My Prefix here is {prefix}",
            timestamp=ctx.created_at
        )
        pfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    # Prefix Change
    @prefix.command(name="prefixchange", aliases=["pfc"], help="Will change the prefix for this guild", usage="<prefix>")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix_change(self, ctx, prefix="~b"):
        await ctx.trigger_typing()
        pfcmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Changed my prefix to ",
            timestamp=ctx.created_at
        )
        pfcmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if not prefix:
            pass
        elif prefix:
            data = read_json("prefixes")
            data[str(ctx.guild.id)] = prefix
            write_json(data, "prefixes")
        pfcmbed.title += prefix
        await ctx.send(pfcmbed)

def setup(bot):
    bot.add_cog(Setup(bot))
