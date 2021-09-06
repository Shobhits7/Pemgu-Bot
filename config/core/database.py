import discord
from discord.ext import commands

class Database(commands.Cog, description="Monotoring database with these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="delete", aliases=["dlt"], help="Will delete a row from db")
    @commands.is_owner()
    async def delete(self, ctx, *, table):
        await ctx.trigger_typing()
        dltmbed = discord.Embed(
            colour=0x525BC1,
            title=F"Deleted from {table}",
            timestamp=ctx.message.created_at
        )
        dltmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await self.bot.db.execute(F"DELETE FROM {table} WHERE guild_id = $1", ctx.guild.id)
        await ctx.send(embed=dltmbed)

def setup(bot):
    bot.add_cog(Database(bot))