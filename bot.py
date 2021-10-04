import discord, aiohttp, os, asyncpg
import core.utils.help as help, core.utils.pagination as page, core.utils.options as options
from discord.ext import commands

async def connect_pool_postgres():
    bot.postgres = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Successfully created to the Postgres Pool")

async def get_prefix(bot, message:discord.Message):
    if not message.guild:
        return ""
    prefix = await bot.postgres.fetch("SELECT prefix FROM prefixes WHERE guild_id=$1", message.guild.id)
    return commands.when_mentioned_or(".j") if len(prefix) == 0 else  commands.when_mentioned_or(prefix)

async def created_session_aiohttp():
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
    def paginator(self, embeds):
        return page.Paginator(self, embeds)

bot = JakeTheDogBase(
    command_prefix=get_prefix,
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

bot.colour = 0xECA622
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
os.environ["JISHAKU_UNDERSCORE"] = "FALSE"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

blacklisted_people = [412734157819609090, 718622831788949575]
@bot.check
async def blacklisted(ctx:commands.Context):
    if ctx.author.id in blacklisted_people: raise commands.CheckFailure
    return True

bot.loop.run_until_complete(connect_pool_postgres())
bot.loop.create_task(created_session_aiohttp())
bot.run(os.getenv("TOKEN"))