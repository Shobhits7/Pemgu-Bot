import discord, aiohttp, asyncpg, asyncio, os
from discord.ext import commands
from config.utils.help import MyHelp

async def create_db_poll():
    bot.db = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Connection to Postgres was successful")

async def get_prefix_postgresql(bot, message):
    if not message.guild:
        return ""
    prefix = await bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    if len(prefix) == 0:
        prefix = ";w"
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    async def close(self):
        if not self.session.closed:
            await self.session.close()

bot = Bot(slash_commands=True, slash_command_guilds=[804380398296498256], command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, help_command=MyHelp(), intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False))

bot.prefix = ";w"
bot.color = 0x2F3136

async def httpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

for folder in sorted(os.listdir("./config/")):
    if folder in ("commands", "events"):
        for cog in sorted(os.listdir(F"./config/{folder}/")):
            if cog.endswith(".py"):
                bot.load_extension(F"config.{folder}.{cog[:-3]}")

bot.load_extension("dismusic")
bot.lava_nodes = [
    {
        "host": "lava.link",
        "password": "whaffle-node",
        "port": 80,
        "identifier": "WHAFFLE",
        "region": "germany"
    }
]

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_db_poll())
bot.loop.create_task(httpsession())
bot.run(os.getenv("TOKEN"))
