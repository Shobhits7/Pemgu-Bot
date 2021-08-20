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
            title=F"My Prefix here is `{prefix}`",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=pfmbed)
    # Prefix Change
    @prefix.command(name="change", aliases=["pfc"], help="Will change the prefix for this guild", usage="<prefix>")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def change(self, ctx, prefix):
        await ctx.trigger_typing()
        if not prefix:
            pass
        elif prefix:
            data = read_json("prefixes")
            data[str(ctx.guild.id)] = prefix
            write_json(data, "prefixes")
        pfcmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Changed my prefix to `{prefix}`",
            timestamp=ctx.message.created_at
        )
        pfcmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=pfcmbed)
    # Prefix Reset
    @prefix.command(name="reset", aliases=["pfr"], help="Will reset the prefix for this guild")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def reset(self, ctx):
        await ctx.trigger_typing()
        data = read_json("prefixes")
        data.pop(str(ctx.guild.id))
        pfrmbed = discord.Embed(
            colour=self.bot.color,
            title="The prefix has been reseted to `~b`",
            timestamp=ctx.message.created_at
        )
        pfrmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=pfrmbed)

def setup(bot):
    bot.add_cog(Setup(bot))
