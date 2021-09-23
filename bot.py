import discord, aiohttp, asyncpg, motor.motor_asyncio, os
from discord.ext import commands
from config.utils import help, options

async def create_postgresl_pool():
    bot.postgresql = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Creating pool to Postgres was successful")

async def get_prefix_postgres(bot, message):
    if not message.guild:
        return ""
    prefix = await bot.postgresql.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    if len(prefix) == 0:
        prefix = bot.prefix
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        self.slash_commands=True
        self.slash_command_guilds=[804380398296498256]
        self.command_prefix=get_prefix_postgres
        self.strip_after_prefix=True
        self.case_insensitive=True
        self._help_command=help.CustomHelp()
        self.intents=discord.Intents.all()
        self.allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False)
        super().__init__(**kwargs)

    async def close(self):
        if not self.session.closed:
            await self.session.close()

bot = Bot()

bot.prefix = ".m"
bot.colour = 0x2F3136


for folder in sorted(os.listdir("./config/")):
    if folder in ("commands", "events"):
        for cog in folder:
            if cog.endswith(".py"):
                bot.load_extension(F"config.core.{cog[:-3]}")
        else: pass
else: pass

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_postgresl_pool())
bot.loop.create_task(aiohttpsession())
bot.run(os.getenv("TOKEN"))
