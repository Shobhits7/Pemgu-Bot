import discord
from discord.ext import commands

class Setup(commands.Cog, description="For setting up the bot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.group(name="prefix", aliases=["pf"], help="Will tell you the prefix for this guild", invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx:commands.Context):
        prefix = await self.bot.postgresql.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", ctx:commands.Context.guild.id)
        if len(prefix) == 0:
            prefix = self.bot.prefix
        else:
            prefix = prefix[0].get("prefix")
        pfmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"My Prefix here is `{prefix}`",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pfmbed)
    # Prefix Change
    @prefix.command(name="change", aliases=["pfc"], help="Will change the prefix for this guild", usage="<prefix>")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix_change(self, ctx:commands.Context, prefix):
        row = await self.bot.postgresql.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", ctx:commands.Context.guild.id)
        if len(row) == 0:
            await self.bot.postgresql.execute("INSERT INTO prefixes(guild_id, prefix) VALUES ($1, $2)", ctx:commands.Context.guild.id, prefix)
        else:
            await self.bot.postgresql.execute("UPDATE prefixes SET prefix = $2 WHERE guild_id = $1", ctx:commands.Context.guild.id, prefix)
        pfcmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"Changed my prefix to `{prefix}`",
            timestamp=ctx.message.created_at
        )
        pfcmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pfcmbed)
    # Prefix Reset
    @prefix.command(name="reset", aliases=["pfr"], help="Will reset the prefix for this guild")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix_reset(self, ctx:commands.Context):
        await self.bot.postgresql.execute("UPDATE prefixes SET prefix = $1 WHERE guild_id = $2",self.bot.prefix, ctx:commands.Context.guild.id)
        pfrmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"The prefix has been resetted  to `{self.bot.prefix}`",
            timestamp=ctx.message.created_at
        )
        pfrmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=pfrmbed)

def setup(bot):
    bot.add_cog(Setup(bot))
