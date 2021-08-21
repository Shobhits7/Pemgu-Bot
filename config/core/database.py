import discord
from discord.ext import commands

class Database(commands.Cog, description="Database command line"):
    def __init__(self, bot):
        self.bot = bot
    
    # Delete
    @commands.command(name="delete", aliases=["dlt"], help="Will delete a row", usage="<table> <guild_id>")
    @commands.is_owner()
    async def delete(self, ctx, *, table, guild_id: int):
        await ctx.trigger_typing()
        await self.bot.db.execute(F"DELETE FROM  {table} WHERE guild_id = $1", guild_id)
        dltmbed = discord.Embed(
            colour=0x2F3136,
            title=F"Deleted the row for {guild_id}",
            timestamp=ctx.message.created_at
        )
        dltmbed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=dltmbed)

def setup(bot):
    bot.add_cog(Database(bot))