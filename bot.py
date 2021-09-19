import discord, aiohttp, asyncpg, os
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
        prefix = bot.prefix
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_connect(self):
        print(F"---------------------------------------------------\nLogged in as: {self.user} - {self.user.id}\nMain prefix is: {self.prefix}\nGuilds bot is in: {len(self.guilds)}\nThe Bot is online now\n---------------------------------------------------")

    # async def on_message(self, message):
    #     if message.author.bot: return
    #     if F"<@!{self.user.id}>" == message.content or F"<@{self.user.id}>" == message.content:
    #         prefix = await self.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    #         if len(prefix) == 0:
    #             prefix = self.prefix
    #         else:
    #             prefix = prefix[0].get("prefix")
    #         ompmbed = discord.Embed(
    #             colour=self.color,
    #             title=F"My Prefix here is `{prefix}`",
    #             timestamp=message.created_at
    #         )
    #         ompmbed.set_footer(text=message.author, icon_url=message.author.avatar.url)
    #         return await message.channel.send(embed=ompmbed)

    # async def on_message_edit(self, old, new):
    #     await self.process_commands(new)

    async def close(self):
        if not self.session.closed:
            await self.session.close()

bot = Bot(slash_commands=True, slash_command_guilds=[804380398296498256], command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, help_command=MyHelp(), intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False))

bot.prefix = ";w"
bot.color = 0x2F3136

async def httpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

for cog in sorted(os.listdir("./config/core/")):
    if cog.endswith(".py"):
        bot.load_extension(F"config.core.{cog[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_db_poll())
bot.loop.create_task(httpsession())
bot.run(os.getenv("TOKEN"))
