import nextcord
from nextcord.ext import commands

class OnGuild(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.bot.db.execute("DELETE FROM prefixes WHERE guild_id = $1", guild.id)

def setup(bot):
    bot.add_cog(OnGuild(bot))