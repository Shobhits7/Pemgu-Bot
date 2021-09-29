import discord, aiohttp, asyncpg, os, config.utils.help as help, config.utils.options as opt
from discord.ext import commands

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class MeiBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = opt.Colour.invis
        self.token = os.getenv("TOKEN")
        self.prefix = ";m"

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

bot = MeiBase(
    command_prefix=commands.when_mentioned_or(";m"),
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
