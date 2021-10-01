import discord, aiohttp, asyncpg, os, random, config.utils.help as help, config.utils.pagination as page
from discord.colour import Colour
from discord.ext import commands

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class MeiBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = os.getenv("TOKEN")
        self.prefix = ";m"

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

    @classmethod
    def paginator(self, ctx, embeds):
        return page.Paginator(ctx, embeds)

    @property
    def colour(self):
        colours = [
            discord.Colour.blue(),
            discord.Colour.blurple(),
            discord.Colour.brand_green(),
            discord.Colour.brand_red(),
            discord.Colour.dark_blue(),
            discord.Colour.dark_gold(),
            discord.Colour.dark_gray(),
            discord.Colour.dark_green(),
            discord.Colour.dark_grey(),
            discord.Colour.dark_magenta(),
            discord.Colour.dark_orange(),
            discord.Colour.dark_purple(),
            discord.Colour.dark_red(),
            discord.Colour.dark_teal(),
            discord.Colour.dark_theme(),
            discord.Colour.darker_gray(),
            discord.Colour.darker_grey(),
            discord.Colour.default(),
            discord.Colour.fuchsia(),
            discord.Colour.gold(),
            discord.Colour.green(),
            discord.Colour.greyple(),
            discord.Colour.light_gray(),
            discord.Colour.light_grey(),
            discord.Colour.lighter_gray(),
            discord.Colour.lighter_grey(),
            discord.Colour.magenta(),
            discord.Colour.og_blurple(),
            discord.Colour.orange(),
            discord.Colour.purple(),
            discord.Colour.random(),
            discord.Colour.red(),
            discord.Colour.teal(),
            discord.Colour.yellow()
        ]
        colour = random.choice(colours)
        return colour

bot = MeiBase(
    command_prefix=commands.when_mentioned_or(";m"),
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

for core in sorted(os.listdir("./config/core/")):
    if core.endswith(".py"):
        bot.load_extension(F"config.core.{core[:-3]}")

bot.load_extension("jishaku")
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

blacklisted_people = []
@bot.check
async def blacklisted(ctx:commands.Context):
    if ctx.author.id in blacklisted_people: raise commands.CheckFailure
    return True

bot.loop.create_task(aiohttpsession())
bot.run(bot.token)
