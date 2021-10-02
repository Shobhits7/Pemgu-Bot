import discord, aiohttp, os, random, config.utils.help as help, config.utils.pagination as page, config.utils.options as options
from discord.ext import commands

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

class MeiBase(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefix = ";m"
        self.command_prefix=commands.when_mentioned_or(self.prefix)
        self.strip_after_prefix=True
        self.case_insensitive=True
        self.help_command=help.CustomHelp()
        self.intents=discord.Intents.all()
        self.allowed_mentions=discord.AllowedMentions.none()
        self.token = os.getenv("TOKEN")
        self.modules = []
        for module in sorted(os.listdir("./config/modules/")):
            if module.endswith(".py"):
                bot.load_extension(F"config.module.{module[:-3]}")
                self.modules.append(module[:-3])
        self.load_extension("jishaku")
        os.environ["JISHAKU_UNDERSCORE"] = "True"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

    @classmethod
    def paginator(self, ctx, embeds):
        return page.Paginator(ctx, embeds)

    @property
    def colour(self):
        colour = random.choice(options.colours)
        return colour

bot = MeiBase()

blacklisted_people = []
@bot.check
async def blacklisted(ctx:commands.Context):
    if ctx.author.id in blacklisted_people: raise commands.CheckFailure
    return True

bot.loop.create_task(aiohttpsession())
bot.run(bot.token)