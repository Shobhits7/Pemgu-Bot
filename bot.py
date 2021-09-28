import discord, aiohttp, asyncpg, os
from discord.ext import commands
from config.utils import help, colours

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = os.getenv("TOKEN")
        self.prefix = ",m"
        self.colour = 0x2F3136

    async def close(self):
        for cog in self.cogs:
            self.unload_extension(cog)
        if not self.session.closed:
            await self.session.close()
        await super().close()

bot = Bot(
    command_prefix=commands.when_mentioned_or(",m"),
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

for core in sorted(os.listdir("./config/core/")):
    if core.endswith(".py"):
        bot.load_extension(F"config.core.{core[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.create_task(aiohttpsession())
bot.run(bot.token)
