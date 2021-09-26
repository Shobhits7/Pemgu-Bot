import discord, contextlib
from discord.ext import commands
from discord.ext.commands import Paginator
import config.views.helpview as hv

class MinimalHelp(commands.MinimalHelpCommand):
    def __init__(self):
        self.emojis = {
            "Anime": "🍘",
            "API": "🌎",
            "Game": "🎮",
            "Moderation": "🎩",
            "Music": "🎼",
            "Owner": "👑",
            "Setup": "🔧",
            "Utility": "🧰",
            "Jishaku": "👀",
            "No": "❓"
        }
        super().__init__(
            command_attrs={
                "help": "The help command for this bot",
                "aliases": ["h", "commands"]
            }
        )
    async def send_pages(self):
        mhmbed = discord.Embed(
            colour=self.context.bot.colour,
            title=F"{self.context.me.name}'s Help",
            timestamp=self.context.message.created_at
        )
        mhmbed.set_thumbnail(url=self.context.me.avatar.url)
        mhmbed.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        mhmbed.set_footer(text="[] means the argument is optional. | <> means the argument is required.")
        for page in self.paginator.pages:
            mhmbed.description = page
            await self.context.send(embed=mhmbed)

class PaginateHelp(commands.HelpCommand):
    def __init__(self):
        self.emojis = {
            "Anime": "🍘",
            "API": "🌎",
            "Game": "🎮",
            "Moderation": "🎩",
            "Music": "🎼",
            "Owner": "👑",
            "Setup": "🔧",
            "Utility": "🧰",
            "Jishaku": "👀",
            "No": "❓"
        }
        super().__init__(
            command_attrs={
                "help": "The help command for this bot",
                "aliases": ["h", "commands"]
            }
        )

    async def send_bot_help(self, mapping):
        paginator = Paginator(",m", "~m", max_size=2000, linesep="\n")
        embeds = []
        for cog, commands in mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            embed = discord.Embed(title=name, description=description)
            embeds.append(embed)
        for mbed in embeds:
            paginator.add_line(mbed)
            for page in paginator.pages:
                await self.context.send(mbed, page)

class CustomHelp(commands.HelpCommand):
    def __init__(self):
        self.emojis = {
            "Anime": "🍘",
            "API": "🌎",
            "Game": "🎮",
            "Moderation": "🎩",
            "Music": "🎼",
            "Owner": "👑",
            "Setup": "🔧",
            "Utility": "🧰",
            "Jishaku": "👀",
            "No": "❓"
        }
        super().__init__(
            command_attrs={
                "help": "The help command for this bot",
                "aliases": ["h", "commands"]
            }
        )

    # Help Main
    async def send_bot_help(self, mapping):
        homepage = discord.Embed(
            colour=self.context.bot.colour,
            title=F"{self.context.me.name}'s Help",
            description=F"This is a list of all modules in the bot.\nSelect a module for more information.",
            timestamp=self.context.message.created_at
        )
        homepage.set_thumbnail(url=self.context.me.avatar.url)
        homepage.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        usable = 0
        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands, sort=True):
                usable += len(filtered_commands)
        homepage.add_field(name="Prefix:", value=self.context.prefix or "In DM you don't need to use prefix", inline=False)
        homepage.add_field(name="Usable:", value=usable, inline=False)
        homepage.add_field(name="Arguments:", value="[] means the argument is optional.\n<> means the argument is required.\n***DO NOT USE THESE WHEN DOING A COMMAND***", inline=False)
        view = hv.SelectView(self, mapping, homepage)
        view.message = await self.context.send(embed=homepage, view=view)
        return

    # Help Cog
    async def send_cog_help(self, cog):
        name = cog.qualified_name if cog else "No"
        description = cog.description if cog else "Commands without category"
        hcogmbed = discord.Embed(
            colour=self.context.bot.colour,
            title=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} Category [{len(cog.get_commands())}]",
            description=F"{description}\n\n",
            timestamp=self.context.message.created_at
        )
        for command in cog.walk_commands():
            hcogmbed.description += F"• **{self.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
        hcogmbed.set_thumbnail(url=self.context.me.avatar.url)
        hcogmbed.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        await self.context.send(embed=hcogmbed)
        return

    # Help Command
    async def send_command_help(self, command):
        hcmdmbed = discord.Embed(
            colour=self.context.bot.colour,
            title=self.get_command_signature(command),
            description=command.help or "No help found...",
            timestamp=self.context.message.created_at
        )
        hcmdmbed.set_thumbnail(url=self.context.me.avatar.url)
        hcmdmbed.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        if cog := command.cog:
            hcmdmbed.add_field(name="Category:", value=F"{self.emojis.get(cog.qualified_name) if self.emojis.get(cog.qualified_name) else '❓'} {cog.qualified_name}")
        can_run = "No"
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"  
        hcmdmbed.add_field(name="Usable", value=can_run)
        if command._buckets and (cooldown := command._buckets._cooldown):
            hcmdmbed.add_field(name="Cooldown", value=F"{cooldown.rate} per {cooldown.per:.0f} seconds")
        await self.context.send(embed=hcmdmbed)
        return

    # Help Group
    async def send_group_help(self, group):
        can_run = "No"
        hgroupmbed = discord.Embed(
            colour=self.context.bot.colour,
            title=self.get_command_signature(group),
            description=F"{group.help or 'No help found...'}\n\n",
            timestamp=self.context.message.created_at
        )
        hgroupmbed.set_thumbnail(url=self.context.me.avatar.url)
        hgroupmbed.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        for command in group.commands:
            hgroupmbed.description += F"• **{self.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
        if cog := command.cog:
            hgroupmbed.add_field(name="Category", value=F"{self.emojis.get(cog.qualified_name) if self.emojis.get(cog.qualified_name) else '❓'} {cog.qualified_name}")
            with contextlib.suppress(commands.CommandError):
                if await command.can_run(self.context):
                    can_run = "Yes"
            hgroupmbed.add_field(name="Usable", value=can_run)
        if command._buckets and (cooldown := command._buckets._cooldown):
            hgroupmbed.add_field(name="Cooldown", value=F"{cooldown.rate} per {cooldown.per:.0f} seconds")
        await self.context.send(embed=hgroupmbed)
        return

    # Help Error
    async def send_error_message(self, error):
        herrormbed = discord.Embed(
            colour=self.context.bot.colour,
            title="Help Error",
            description=error,
            timestamp=self.context.message.created_at
        )
        herrormbed.set_thumbnail(url=self.context.me.avatar.url)
        herrormbed.set_author(name=self.context.author, icon_url=self.context.author.avatar.url)
        await self.context.send(embed=herrormbed)
        return
