import discord, aiohttp, os, io
import core.utils.help as help, core.utils.pagination as page, core.utils.options as options
from discord.ext import commands
from PIL import Image, ImageFilter

async def aiohttpsession():
    bot.session = aiohttp.ClientSession()
    print("Making a Session was successful")

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
    command_prefix=commands.when_mentioned_or(".j"),
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

@bot.command(name="wanted")
async def wanted(ctx:commands.Context, user:discord.User=None):
    user = ctx.author if not user else user
    wanted = Image.open("./core/images/wanted.jpg")
    asset = user.avatar.with_size(128)
    buffer = io.BytesIO(await asset.read())
    pfp = Image.open(buffer)
    pfp = pfp.resize((177, 177))
    wanted.paste(pfp, (390, 299))
    buffer2 = io.BytesIO()
    wanted.save(buffer2, 'jpg')
    buffer2.seek(0)
    await ctx.send(file=discord.File(fp=buffer2, filename= "wanted.jpg"))

bot.loop.create_task(aiohttpsession())
bot.run(os.getenv("TOKEN"))