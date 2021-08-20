import discord
from discord.ext import commands
import os
import datetime
from config.utils.json import read_json, write_json

def get_prefix(bot, message):
    data = read_json("prefixes")
    if message.guild:
        if not str(message.guild.id) in data:
            return "~b" or "~B"
        elif str(message.guild.id) in data:
            return data[str(message.guild.id)]
    else:
        return ""

bot = commands.Bot(command_prefix=get_prefix, strip_after_prefix=True, case_insensitive=True, owner_ids={798928603201929306, 494496285676535811}, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="@Brevity for prefix | ~b help for help | Made by lvlahraam"))

bot.colors = [
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
    discord.Colour.darker_grey()
]

bot.color = 0x2F3136
bot.time = datetime.datetime.utcnow()

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
