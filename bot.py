import discord, aiohttp, asyncpg, motor.motor_asyncio, os
from discord.ext import commands
from config.utils import errors, help, options

async def create_postgresql_pool():
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

async def connect_mongodb_cluster():
    bot.cluster = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB"))
    print("Connection to MongoDB was successful")

async def get_prefix_mongodb(bot, message):
    if not message.guild:
        return ""

    prefixes = bot.cluster["Mei-DB"]['prefixes']
    if (await prefixes.count_documents({}) == 0):
        prefix = bot.prefix
    else:
        prefix = await prefixes.find_one({'_id': str(message.guild.id)})
    return commands.when_mentioned_or(prefix)(bot, message)

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def on_connect(self):
        print(F"---------------------------------------------------\nLogged in as: {self.user} - {self.user.id}\nMain prefix is: {self.prefix}\nGuilds bot is in: {len(self.guilds)}\nThe Bot is online now\n---------------------------------------------------")
        await self.change_presence(activity=discord.Game(name=F"@{self.user.name} for prefix | {self.prefix} help for help"))

    async def on_message(self, message):
        if message.author.bot: return
        if F"<@!{self.user.id}>" == message.content or F"<@{self.user.id}>" == message.content:
            prefix = await self.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
            if len(prefix) == 0:
                prefix = self.prefix
            else:
                prefix = prefix[0].get("prefix")
            ompmbed = discord.Embed(
                colour=self.colour,
                title=F"My Prefix here is `{prefix}`",
                timestamp=message.created_at
            )
            ompmbed.set_footer(text=message.author, icon_url=message.author.avatar.url)
            return await message.channel.send(embed=ompmbed)
        else:
            await self.process_commands(message)

    async def on_message_edit(self, old, new):
        await self.process_commands(new)

    async def on_command_error(self, ctx, error):
        await errors.handler(bot=self, ctx=ctx, error=error)

    async def close(self):
        if not self.session.closed:
            await self.session.close()

bot = Bot(slash_commands=True, slash_command_guilds=[804380398296498256], command_prefix=get_prefix_mongodb, strip_after_prefix=True, case_insensitive=True, help_command=help.CustomHelp(), intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(users=False, everyone=False, roles=False, replied_user=False))

bot.prefix = ".m"
bot.colour = 0x2F3136

for cog in sorted(os.listdir("./config/core/")):
    if cog.endswith(".py"):
        bot.load_extension(F"config.core.{cog[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_postgresql_pool())
bot.loop.run_until_complete(connect_mongodb_cluster())
bot.loop.create_task(aiohttpsession())
bot.run(os.getenv("TOKEN"))
