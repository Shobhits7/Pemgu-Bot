import discord, aiohttp, asyncpg, os, random
from discord.ext import commands
from config.utils import help

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class MeiBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = os.getenv("TOKEN")
        self.prefix = ";m"
        self.colour = 0x2F3136

    @property
    def color(self):
        colours = [
            discord.Colour.default(),
            discord.Colour.teal(),
            discord.Colour.dark_teal(),
            discord.Colour.green(),
            discord.Colour.dark_green(),
            discord.Colour.blue(),
            discord.Colour.dark_blue(),
            discord.Colour.blurple(),
            discord.Colour.purple(),
            discord.Colour.dark_purple(),
            discord.Colour.magenta(),
            discord.Colour.dark_magenta(),
            discord.Colour.gold(),
            discord.Colour.dark_gold(),
            discord.Colour.orange(),
            discord.Colour.dark_orange(),
            discord.Colour.red(),
            discord.Colour.dark_red(),
            discord.Colour.greyple(),
            discord.Colour.light_grey(),
            discord.Colour.lighter_grey(),
            discord.Colour.dark_grey(),
            discord.Colour.darker_grey(),
        ]
        colour = random.choice(colours)
        return colour

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
