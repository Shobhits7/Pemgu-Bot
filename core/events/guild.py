import discord
from discord.ext import commands

class OnGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild:discord.Guild):
        prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", guild.id)
        if prefix:
            await self.bot.postgres.execute("DELETE FROM prefixes WHERE guild_id=$1", guild.id)

def setup(bot):
    bot.add_cog(OnGuild(bot))