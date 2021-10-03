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
        self._commands = []
        for command in sorted(os.listdir("./config/commands/")):
            if command.endswith(".py"):
                self.load_extension(F"config.commands.{command[:-3]}")
                self._commands.append(command[:-3])
        self._events = []
        for event in sorted(os.listdir("./config/events/")):
            if event.endswith(".py"):
                self.load_extension(F"config.events.{event[:-3]}")
                self._events.append(event[:-3])
        self.load_extension("jishaku")
        os.environ["JISHAKU_UNDERSCORE"] = "True"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

    async def close(self):
        if not self.session.closed:
            await self.session.close()
        await super().close()

    @classmethod
    def paginator(self, embeds):
        return page.Paginator(self, embeds)

bot = JakeTheDogBase(
    command_prefix=commands.when_mentioned_or(".j"),
    strip_after_prefix=True,
    case_insensitive=True,
    help_command=help.CustomHelp(),
    intents=discord.Intents.all(),
    allowed_mentions=discord.AllowedMentions.none()
)

blacklisted_people = [412734157819609090]
@bot.check
async def blacklisted(ctx:commands.Context):
    if ctx.author.id in blacklisted_people: raise commands.CheckFailure
    return True

bot.loop.create_task(aiohttpsession())
bot.run(bot.token)