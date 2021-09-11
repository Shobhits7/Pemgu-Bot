import discord
from discord.ext import commands

class Database(commands.Cog, description="Monotoring database with these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="delete_prefix", help="Will delete a row from db")
    @commands.is_owner()
    async def delete_prefix(self, ctx, *, guild):
        await ctx.trigger_typing()
        dltmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Deleted from prefixes",
            timestamp=ctx.message.created_at
        )
        dltmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await self.bot.db.execute(F"DELETE FROM preffixes WHERE guild_id = $1", guild)
        await ctx.send(embed=dltmbed)
    
    @commands.command(name="delete_todo", help="Will delete a row from db")
    @commands.is_owner()
    async def delete_todo(self, ctx, *, user):
        await ctx.trigger_typing()
        dltmbed = discord.Embed(
            colour=self.bot.color,
            title=F"Deleted from todo",
            timestamp=ctx.message.created_at
        )
        dltmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        await self.bot.db.execute(F"DELETE FROM todos WHERE user_id = $1", user)
        await ctx.send(embed=dltmbed)

def setup(bot):
    bot.add_cog(Database(bot))