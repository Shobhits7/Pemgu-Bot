import discord
from discord.ext import commands
import os
import asyncpg
from config.utils.json import read_json, write_json

async def get_prefix_postgresql(bot, message):
    if not message.guild:
        return "~b"
    prefix = await bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    if len(prefix) == 0:
        await bot.db.execute("INSERT INTO prefixes(guild_id, prefix) VALUES ($1, $2)", message.guild.id, "~b")
        prefix = "~b"
    else:
        prefix = prefix[0].get("prefix")
    return prefix

bot = commands.Bot(command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, owner_ids={798928603201929306, 494496285676535811}, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="@Brevity for prefix | ~b help for help | Made by lvlahraam"))

async def create_db_pool():
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

bot.loop.run_until_complete(create_db_pool())
bot.run(os.getenv("TOKEN"))
