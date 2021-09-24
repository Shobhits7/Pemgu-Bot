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

# Info
@bot.user_command(name="Info")
async def info(ctx:commands.Context, user):
    member = user or ctx.author
    image = await bot.fetch_user(member.id)
    iombed = discord.Embed(
        colour=bot.colour,
        title=F"{member} Information",
        description="`Global-Information` is for the user in discord\n`Guild-Information` for the user in this guild",
        timestamp=ctx.message.created_at
    )
    iombed.add_field(name="Global-Information:", value=F"""
    ***Username:*** {member.name}
    ***Discriminator:*** {member.discriminator}
    ***ID:*** {member.id}
    ***Mention:*** {member.mention}
    ***Badges:*** {', '.join([flag.replace("_", " ").title() for flag, enabled in member.public_flags if enabled])}
    ***Activity:*** {'*Nothing*' if not member.activity else member.activity}
    ***Status:*** {member.status}
    ***Web-Status:*** {member.web_status}
    ***Desktop-Status:*** {member.desktop_status}
    ***Mobile-Status:*** {member.mobile_status}
    ***Registered:*** {discord.utils.format_dt(member.created_at, style="f")} ({discord.utils.format_dt(member.created_at, style="R")})""", inline=False)
    iombed.add_field(name="Guild-Information:", value=F"""
    ***Joined:*** {discord.utils.format_dt(member.joined_at, style="f")} ({discord.utils.format_dt(member.joined_at, style="R")})
    ***Roles [{len(member.roles)}]:*** {', '.join(role.mention for role in member.roles)}
    ***Top-Role:*** {member.top_role.mention}
    ***Boosting:*** {'True' if member in ctx.guild.premium_subscribers else 'False'}
    ***Nickname:*** {member.nick}
    ***Voice:*** {member.voice}
    ***Guild-Permissions:*** {', '.join([perm.replace("_", " ").title() for perm, enabled in member.guild_permissions if enabled])}""", inline=False)
    iombed.set_thumbnail(url=member.avatar.url)
    if image.banner and image.banner.url:
        iombed.set_image(url=image.banner.url)
    else:
        iombed.description += "\n**Banner:** Member doesn't have banner"
    iombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
    await ctx.send(embed=iombed)

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
