import nextcord
from nextcord.ext import commands

class Setup(commands.Cog, description="For setting up the bot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.group(name="prefix", aliases=["pf"], help="Will tell you the prefix for this guild", invoke_without_command=True)
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx):
        await ctx.trigger_typing()
        prefix = await self.bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", ctx.guild.id)
        if len(prefix) == 0:
            prefix = "~b"
        else:
            prefix = prefix[0].get("prefix")
        pfmbed = nextcord.Embed(
            colour=0x525BC2,
            title=F"My Prefix here is `{prefix}`",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=pfmbed)
    # Prefix Change
    @prefix.command(name="change", aliases=["pfc"], help="Will change the prefix for this guild", usage="<prefix>")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix_change(self, ctx, prefix):
        await ctx.trigger_typing()
        await self.bot.db.execute("INSERT INTO prefixes(guild_id, prefix) VALUES ($1, $2)", ctx.guild.id, prefix)
        pfcmbed = nextcord.Embed(
            colour=0x525BC2,
            title=F"Changed my prefix to `{prefix}`",
            timestamp=ctx.message.created_at
        )
        pfcmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=pfcmbed)
    # Prefix Reset
    @prefix.command(name="reset", aliases=["pfr"], help="Will reset the prefix for this guild")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix_reset(self, ctx):
        await ctx.trigger_typing()
        await self.bot.db.execute("UPDATE prefixes SET prefix = $1 WHERE guild_id = $2",self.bot.prefix, ctx.guild.id)
        pfrmbed = nextcord.Embed(
            colour=0x525BC2,
            title=F"The prefix has been resetted  to `{self.bot.prefix}`",
            timestamp=ctx.message.created_at
        )
        pfrmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=pfrmbed)

def setup(bot):
    bot.add_cog(Setup(bot))
