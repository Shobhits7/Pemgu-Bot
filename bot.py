import discord, asyncpg, os, aiohttp, random
import core.utils.help as help
from discord.ext import commands

async def create_pool_postgres():
    bot.postgres = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Successfully created to the Postgres Pool")

async def get_prefix(bot, message:discord.Message):
    prefix = bot.prefixes.get(message.guild.id)
    if prefix:
        return commands.when_mentioned_or(prefix)(bot, message)
    postgres = await bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", message.guild.id)
    if postgres:
        prefix = bot.prefixes[message.guild.id] = postgres
    else:
        prefix = bot.prefixes[message.guild.id] = bot.default_prefix
    print(F"Cached {F'{prefix}/d' if not postgres else F'{postgres}/p'} | {message.guild.name} - {message.guild.id}")
    return commands.when_mentioned_or(prefix)(bot, message)

async def create_session_aiohttp():
    bot.session = aiohttp.ClientSession()
    print("Successfully created a AioHttp Session ")

class PemguBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefixes = {}
        self.default_prefix = ".m"
        self._commands = []
        for command in sorted(os.listdir("./core/commands/")):
            if command.endswith(".py"):
                self.load_extension(F"core.commands.{command[:-3]}")
                self._commands.append(command[:-3])
        self._events = []
        for event in sorted(os.listdir("./core/events/")):
            if event.endswith(".py"):
                self.load_extension(F"core.events.{event[:-3]}")
                self._events.append(event[:-3])
        self.load_extension("jishaku")
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
        self.afks = {}

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

    @property
    def color(self):
        colors = [
            0x224585, 0x1D4E9A, 0x4879CE, 0x142966, 0x093C84,
            discord.Color.blue(),
            discord.Color.blurple(),
            discord.Color.brand_green(),
            discord.Color.brand_red(),
            discord.Color.dark_blue(),
            discord.Color.dark_gold(),
            discord.Color.dark_gray(),
            discord.Color.dark_green(),
            discord.Color.dark_grey(),
            discord.Color.dark_magenta(),
            discord.Color.dark_orange(),
            discord.Color.dark_purple(),
            discord.Color.dark_red(),
            discord.Color.dark_teal(),
            discord.Color.dark_theme(),
            discord.Color.darker_gray(),
            discord.Color.darker_grey(),
            discord.Color.default(),
            discord.Color.fuchsia(),
            discord.Color.gold(),
            discord.Color.green(),
            discord.Color.greyple(),
            discord.Color.light_gray(),
            discord.Color.light_grey(),
            discord.Color.lighter_gray(),
            discord.Color.lighter_grey(),
            discord.Color.magenta(),
            discord.Color.og_blurple(),
            discord.Color.orange(),
            discord.Color.purple(),
            discord.Color.random(),
            discord.Color.red(),
            discord.Color.teal(),
            discord.Color.yellow()
        ]
        color = random.choice(colors)
        return color

    @classmethod
    def trim(self, text: str, limit: int):
        text = text.strip()
        if len(text) > limit: return text[:limit-3] + "..."
        return text

bot = PemguBase(
    slash_commands=True,
    command_prefix=get_prefix,
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

@bot.check
async def blacklisted(ctx:commands.Context):
    blacklist = await bot.postgres.fetchval("SELECT user_id FROM blacklist WHERE user_id=$1", ctx.author.id)
    if not blacklist: return True
    raise commands.CheckAnyFailure

bot.loop.run_until_complete(create_pool_postgres())
bot.loop.create_task(create_session_aiohttp())
bot.run(os.getenv("TOKEN"))
