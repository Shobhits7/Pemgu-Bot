import discord, aiohttp, asyncpg, os
from discord.ext import commands
from config.utils import help, options

async def create_postgresl_pool():
    bot.postgresql = await asyncpg.create_pool(dsn=os.getenv("DATABASE_URL"))
    print("Creating pool to Postgres was successful")

async def get_prefix_postgresql(bot, message):
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
        super().__init__(**kwargs)

    async def close(self):
        if not self.session.closed:
            await self.session.close()

bot = Bot(
    slash_commands=True,
    slash_command_guilds=[804380398296498256],
    command_prefix=get_prefix_postgresql,
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False)
)

bot.prefix = ".m"
bot.colour = 0x2F3136


@bot.user_command(name="Avatar")
async def avatar(ctx:commands.Context, user:discord.Member):
    avatarMbed = discord.Embed(title=F"{user} 's Avatar")
    avatarMbed.set_image(url=user.avatar.url)
    await ctx.respond(content="Here is the avatar", embed=avatarMbed)

for folder in sorted(os.listdir("./config/")):
    if folder in ("commands", "events"):
        for cog in sorted(os.listdir(F"./config/{folder}/")):
            if cog.endswith(".py"):
                bot.load_extension(F"config.{folder}.{cog[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_postgresl_pool())
bot.loop.create_task(aiohttpsession())
bot.run(os.getenv("TOKEN"))
