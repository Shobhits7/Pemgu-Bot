import discord
from discord import activity
from discord.ext import commands
from config.utils.help import MyHelp
import os
import asyncpg

async def create_db_pool():
    bot.db = await asyncpg.create_pool(dsn=os.getenv("POSTGRESQL"))
    print("Connection to Postgres was successful")

async def get_prefix_postgresql(bot, message):
    if not message.guild:
        return ""
    prefix = await bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    if len(prefix) == 0:
        prefix = "~b"
    else:
        prefix = prefix[0].get("prefix")
    return prefix

bot = commands.Bot(slash_command_guilds=[804380398296498256], command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False), help_command=MyHelp(), owner_ids={798928603201929306, 494496285676535811}, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="@Brevity for prefix | ~b help for help | Made by lvlahraam"))

bot.activity = discord.Game(name="@Brevity for prefix | ~b help for help | Made by lvlahraam")
bot.status = discord.Status.online

bot.prefix = "~b"

bot.blacklisted = []

@bot.check
async def blacklisted(ctx):
    if ctx.author.id in bot.blacklisted:
        return False
    return True 

for file in sorted(os.listdir("./config/core/")):
    if file.endswith(".py"):
        bot.load_extension(F"config.core.{file[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_db_pool())
bot.run(os.getenv("TOKEN"))
