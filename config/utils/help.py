import discord, contextlib
from discord.ext import commands
from config.views import helpmenu

class MyHelp(commands.HelpCommand):
    def __init__(self):
        self.emojis = {
            "Anime": "🍙",
            "API": "🌎",
            "Fun": "🤣",
            "Game": "🎮",
            "Moderation": "🎩",
            "Owner": "👑",
            "Setup": "🔮",
            "Utility": "🧰",
            "Waifu": "🍘",
            "Jishaku": "👀",
            "No": "❓"
        }
        super().__init__(
            command_attrs={
                "help": "The help command for the bot",
                "aliases": ["h", "commands"]
            }
        )

    # Help Main
    async def send_bot_help(self, mapping):
        ctx = self.context
        homepage = discord.Embed(
            colour=ctx.bot.color,
            title=F"{ctx.me.display_name} Help",
            description=F"This is a list of all modules in the bot.\nSelect a module for more information.",
            timestamp=ctx.message.created_at
        )
        homepage.set_thumbnail(url=ctx.me.avatar.url)
        homepage.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        usable = 0
        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands, sort=True):
                usable += len(filtered_commands)
        homepage.add_field(name="Prefix:", value=ctx.clean_prefix or "In DM you don't need to use prefix", inline=False)
        homepage.add_field(name="Usable:", value=usable, inline=False)
        homepage.add_field(name="Arguments:", value="[] means the argument is optional.\n<> means the argument is required.\n***DO NOT USE THESE WHEN DOING A COMMAND***", inline=False)
        view = helpmenu.HelpView(self, mapping, homepage, self.emojis)
        view.message = await ctx.send(embed=homepage, view=view)
        return

    # Help Cog
    async def send_cog_help(self, cog):
        ctx = self.context
        name = cog.qualified_name if cog else "No"
        description = cog.description if cog else "Commands without category"
        hcogmbed = discord.Embed(
            colour=ctx.bot.color,
            title=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} Category [{len(cog.get_commands())}]",
            description=F"{description}\n\n",
            timestamp=ctx.message.created_at
        )
        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                hcogmbed.description += F"**{self.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
        hcogmbed.set_thumbnail(url=ctx.me.avatar.url)
        hcogmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=hcogmbed)
        return

    # Help Command
    async def send_command_help(self, command):
        ctx = self.context
        hcmdmbed = discord.Embed(
            colour=ctx.bot.color,
            title=F"**{self.get_command_signature(command)}**",
            description=command.help or "No help found...",
            timestamp=ctx.message.created_at
        )
        hcmdmbed.set_thumbnail(url=ctx.me.avatar.url)
        hcmdmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        if cog := command.cog:
            hcmdmbed.add_field(name="Category:", value=F"{self.emojis.get(cog.qualified_name) if self.emojis.get(cog.qualified_name) else '❓'} {cog.qualified_name}")
        can_run = "No"
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"  
        hcmdmbed.add_field(name="Usable", value=can_run)
        if command._buckets and (cooldown := command._buckets._cooldown):
            hcmdmbed.add_field(name="Cooldown", value=F"{cooldown.rate} per {cooldown.per:.0f} seconds")
        await ctx.send(embed=hcmdmbed)
        return

    # Help Group
    async def send_group_help(self, group):
        ctx = self.context
        can_run = "No"
        hgroupmbed = discord.Embed(
            colour=ctx.bot.color,
            title=F"**{self.get_command_signature(group)}**",
            description=F"{group.help or 'No help found...'}\n\n",
            timestamp=ctx.message.created_at
        )
        hgroupmbed.set_thumbnail(url=ctx.me.avatar.url)
        hgroupmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        for command in group.commands:
            hgroupmbed.description += F"**{self.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
        if cog := command.cog:
            hgroupmbed.add_field(name="Category", value=F"{self.emojis.get(cog.qualified_name) if self.emojis.get(cog.qualified_name) else '❓'} {cog.qualified_name}")
            with contextlib.suppress(commands.CommandError):
                if await command.can_run(self.context):
                    can_run = "Yes"
            hgroupmbed.add_field(name="Usable", value=can_run)
        if command._buckets and (cooldown := command._buckets._cooldown):
            hgroupmbed.add_field(name="Cooldown", value=F"{cooldown.rate} per {cooldown.per:.0f} seconds")
        await ctx.send(embed=hgroupmbed)
        return

    # Help SubCommand Error
    async def subcommand_not_found(self, command, string):
        ctx = self.context
        hscmdmbed = discord.Embed(
            colour=ctx.bot.color,
            title="Sub Command Not Found",
            description=F"{command} - {string}",
            timestamp=ctx.message.created_at
        )
        hscmdmbed.set_thumbnail(url=ctx.me.avatar.url)
        hscmdmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=hscmdmbed)
        return

    # Help Error
    async def send_error_message(self, error):
        if error == None:
            return
        ctx = self.context
        herrormbed = discord.Embed(
            colour=ctx.bot.color,
            title="Help Error",
            description=error,
            timestamp=ctx.message.created_at
        )
        herrormbed.set_thumbnail(url=ctx.me.avatar.url)
        herrormbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=herrormbed)
        return
