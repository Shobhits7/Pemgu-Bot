import discord, aiohttp, asyncpg, os
from discord.ext import commands
from config.utils import help, options

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def close(self):
        if not self.session.closed:
            await self.session.close()

prefix = ",m"
bot = Bot(
    command_prefix=prefix,
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.PaginateHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

bot.prefix = prefix
bot.colour = 0x2F3136

for folder in sorted(os.listdir("./config/")):
    if folder in ("commands", "events"):
        for cog in sorted(os.listdir(F"./config/{folder}/")):
            if cog.endswith(".py"):
                bot.load_extension(F"config.{folder}.{cog[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.create_task(aiohttpsession())
bot.run(os.getenv("TOKEN"))
