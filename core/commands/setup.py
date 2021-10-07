import discord
from discord.ext import commands

class Setup(commands.Cog, description="For setting up the bot"):
    def __init__(self, bot):
        self.bot = bot

    # Prefix
    @commands.group(name="prefix", aliases=["pf"], help="Will tell you the prefix for this guild", invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx:commands.Context):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        pfmbed = discord.Embed(
            colour=self.bot.colour,
            title=F"My Prefix here is:",
            description=F"> {self.bot.prefix if not prefix else prefix}",
            timestamp=ctx.message.created_at
        )
        pfmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfmbed)

    # Prefix-Change
    @prefix.command(name="change", aliases=["ch"], help="Will change the prefix to the new given prefix")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def prefix_change(self, ctx:commands.Context, *, text:str):
        if text == self.bot.prefix: await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        else: prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        if not prefix: await self.bot.postgres.execute("INSERT INTO prefixes(guild_name,guild_id,prefix) VALUES ($1,$2,$3)", ctx.guild.name, ctx.guild.id, text)
        else: await self.bot.postgres.execute("UPDATE prefixes SET prefix=$1 WHERE guild_name=$2 AND guild_id=$3", text, ctx.guild.name, ctx.guild.id)
        pfchmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully changed prefix to:",
            description=F"> {text}",
            timestamp=ctx.message.created_at
        )
        pfchmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfchmbed)

    # Prefix-Reset
    @prefix.command(name="reset", aliases=["rs"], help="Will reset the prefix")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def prefix_reset(self, ctx:commands.Context):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        if prefix: await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", ctx.guild.id)
        pfrsmbed = discord.Embed(
            colour=self.bot.colour,
            title="Successfully resetted to:",
            description=F"> {self.bot.prefix}",
            timestamp=ctx.message.created_at
        )
        pfrsmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=pfrsmbed)

def setup(bot):
    bot.add_cog(Setup(bot))