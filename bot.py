import discord, aiohttp, asyncpg, os
from discord.ext import commands
from discord.ext.commands.errors import CheckAnyFailure
from config.utils.help import MyHelp

async def create_db_poll():
    bot.db = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Connection to Postgres was successful")

async def get_prefix_postgresql(bot, message):
    if not message.guild:
        return ""
    prefix = await bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    if len(prefix) == 0:
        prefix = "[w]"
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)

bot = commands.Bot(slash_commands=True, slash_command_guilds=[804380398296498256], command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, help_command=MyHelp(), intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False))

async def aiohttp_session():
    bot.aiosession = aiohttp.ClientSession
    print("Making a ClientSession was successful")

bot.prefix = "[w]"
bot.color = 0x2F3136

bot.activity = discord.Game(name=F"@Whaffle for prefix | {bot.prefix} help for help | Made by lvlahraam#8435")

bot.status = discord.Status.online

for cog in sorted(os.listdir("./config/core/")):
    if cog.endswith(".py"):
        bot.load_extension(F"config.core.{cog[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_db_poll())
bot.loop.run_until_complete(aiohttp_session())
bot.run(os.getenv("TOKEN"))
