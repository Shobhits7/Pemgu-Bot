import discord
from discord.ext import commands
import os
import asyncpg
from config.utils.json import read_json, write_json

async def get_prefix_postgresql(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(bot.default_prefix)(bot, message)
    try:
        return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)
    except KeyError:
        prefix = await bot.db.fetchval("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
        if prefix:
            bot.prefixes[message.guild.id] = prefix
            return commands.when_mentioned_or(bot.prefix[message.guild.id])(bot, message)
        else:
            await bot.db.execute("INSERT INTO prefixes (guild_d,prefix) VALUES ($1,$2) ON CONFLICT (guild_id) DO UPDATE SET prefix = $2", message.guild.id, bot.default_prefix)
            bot.prefixes[message.guild.id] = bot.default_prefix
            return commands.when_mentioned_or(bot.prefixes[message.guild.id])(bot, message)

bot = commands.Bot(command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, owner_ids={798928603201929306, 494496285676535811}, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="@Brevity for prefix | ~b help for help | Made by lvlahraam"))

bot.prefixes = {}
bot.default_prefix = "~b"

async def create_db_pool():
    await bot.wait_until_ready()
    bot.db = await asyncpg.create_pool(dsn=os.getenv("POSTGRESQL"))
    print("Connection to Postgres was successful")

bot.blacklisted = []

@bot.check
async def blacklisted(ctx):
    if ctx.author.id in bot.blacklisted:
        return False
    return True 

for file in sorted(os.listdir("./config/core/")):
    if file.endswith(".py"):
        bot.load_extension(F"config.core.{file[:-3]}")

bot.load_extension('jishaku')
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.run(os.getenv("TOKEN"))
bot.loop.create_task(bot.create_db_pool())
