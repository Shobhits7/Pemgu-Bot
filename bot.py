import discord, asyncpg, os, aiohttp, inspect
import core.utils.help as help, core.utils.pagination as page, core.utils.options as options
from discord.ext import commands

async def create_pool_postgres():
    bot.postgres = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Successfully created to the Postgres Pool")

async def get_prefix(bot, message:discord.Message):
    if not message.guild:
        return ""
    prefix = await bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", message.guild.id)
    if not prefix: prefix = bot.prefix
    else: prefix = prefix
    return prefix

async def create_session_aiohttp():
    bot.session = aiohttp.ClientSession()
    print("Successfully created a AioHttp Session ")

class JakeTheDogBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

    @classmethod
    def embed(self, ctx:commands.Context, url, title, desc):
        jtd = discord.Embed()
        if url: jtd.url = url
        if title: jtd.title = title
        if desc: jtd.desc = desc
        jtd.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        return jtd

bot = JakeTheDogBase(
    slash_commands=True,
    slash_command_guilds=[804380398296498256, 896009160603357224],
    command_prefix=get_prefix,
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

bot.colour = 0x2F3136 or 0x36393E
bot.prefix = ".j"
bot._commands = []
for command in sorted(os.listdir("./core/commands/")):
    if command.endswith(".py"):
        bot.load_extension(F"core.commands.{command[:-3]}")
        bot._commands.append(command[:-3])
bot._events = []
for event in sorted(os.listdir("./core/events/")):
    if event.endswith(".py"):
        bot.load_extension(F"core.events.{event[:-3]}")
        bot._events.append(event[:-3])
bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

@bot.check
async def blacklisted(ctx:commands.Context):
    blacklist = await bot.postgres.fetchval("SELECT user_id FROM blacklist WHERE user_id=$1", ctx.author.id)
    if not blacklist: return True
    raise commands.CheckFailure

bot.loop.run_until_complete(create_pool_postgres())
bot.loop.create_task(create_session_aiohttp())
bot.run(os.getenv("TOKEN"))
