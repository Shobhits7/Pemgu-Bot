import discord, aiohttp, os, random
import config.utils.help as help, config.utils.pagination as page, config.utils.options as options
from discord.ext import commands

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class JakeTheDogBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.colour = 0xECA622
        self.prefix = ".j"
        self.token = os.getenv("TOKEN")
        self.modules = []
        for module in sorted(os.listdir("./config/modules/")):
            if module.endswith(".py"):
                self.load_extension(F"config.modules.{module[:-3]}")
                self.modules.append(module[:-3])
        self.load_extension("jishaku")
        os.environ["JISHAKU_UNDERSCORE"] = "True"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

    @classmethod
    def paginator(self, embeds):
        return page.Paginator(self.bot, embeds)

bot = JakeTheDogBase(
    command_prefix=commands.when_mentioned_or(".j"),
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

blacklisted_people = []
@bot.check
async def blacklisted(ctx:commands.Context):
    if ctx.author.id in blacklisted_people: raise commands.CheckFailure
    return True

bot.loop.create_task(aiohttpsession())
bot.run(bot.token)