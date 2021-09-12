import discord, asyncpg, os
from discord.ext import commands
from config.utils.help import MyHelp

bot = commands.Bot(slash_commands=True, slash_command_guilds=[804380398296498256], command_prefix=".poke", strip_after_prefix=True, case_insensitive=True, allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False), help_command=MyHelp(), intents=discord.Intents.all())

bot.prefix = ".poke"
bot.color = 0x0x2F3136 

bot.activity = discord.Game(name=F"@Poke.net for prefix | {bot.prefix} help for help | Made by lvlahraam#8435")

bot.status = discord.Status.online

for file in sorted(os.listdir("./config/core/")):
    if file.endswith(".py"):
        bot.load_extension(F"config.core.{file[:-3]}")

bot.load_extension("jishaku")

bot.run(os.getenv("TOKEN"))
