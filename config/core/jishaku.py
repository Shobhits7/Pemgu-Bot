import discord
from discord.ext import commands
from jishaku.cog import STANDARD_FEATURES

class CustomDebugCog(*STANDARD_FEATURES,  name="Jishaku :eyes:", description="Jishaku commands are hidden in here"):
    pass

def setup(bot: commands.Bot):
    bot.add_cog(CustomDebugCog(bot=bot))
