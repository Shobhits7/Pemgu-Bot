import discord, aiohttp, asyncpg, os
from discord.ext import commands
from config.utils import help, colours

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefix = ",m"
        self.colour = 0x2F3136

    async def close(self):
        if not self.session.closed:
            await self.session.close()

bot = Bot(
    command_prefix=",m",
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

for cog in sorted("./config/core/"):
    if cog.endswith(".py"):
        bot.load_extension(F"config.core.{cog[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.create_task(aiohttpsession())
bot.run(os.getenv("TOKEN"))
