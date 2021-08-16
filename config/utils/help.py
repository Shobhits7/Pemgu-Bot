import discord
from discord.ext import commands
import datetime
import contextlib

class HelpEmbed(discord.Embed): 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = 0x5258B9
        self.timestamp = datetime.datetime.utcnow()
        self.text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
        self.set_footer(text=self.text)

class MyHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.user),
                "aliases": ["h", "commands"]
            }
        )
    
    # Help Main
    async def send_bot_help(self, mapping):
        ctx = self.context
        hmainmbed = HelpEmbed(
            title=F"{ctx.me.display_name} Help",
        )
        hmainmbed.set_thumbnail(url=ctx.me.avatar_url)
        hmainmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        usable = 0 
        for cog, commands in mapping.items(): 
            if filtered_commands := await self.filter_commands(commands, sort=True):
                amount_commands = len(filtered_commands)
                usable += amount_commands
                if cog:
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No Category"
                    description = "Commands with no category"
                hmainmbed.add_field(name=F"{name} Category [{amount_commands}]", value=description)
        hmainmbed.description = F"{len(self.context.bot.commands)} commands | {usable} usable" 
        await ctx.reply(embed=hmainmbed)

    # Help Command
    async def send_command_help(self, command):
        ctx = self.context
        signature = self.get_command_signature(command)
        hcmdmbed = HelpEmbed(
            title=signature,
            description=command.help or "No help found...",
        )
        hcmdmbed.set_thumbnail(url=ctx.me.avatar_url)
        hcmdmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        if cog := command.cog:
            hcmdmbed.add_field(name="Category", value=cog.qualified_name)
        can_run = "No"
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"  
        hcmdmbed.add_field(name="Usable", value=can_run)
        if command._buckets and (cooldown := command._buckets._cooldown):
            hcmdmbed.add_field(name="Cooldown", value=F"{cooldown.rate} per {cooldown.per:.0f} seconds")
        await ctx.reply(embed=hcmdmbed)

    # Help Cog
    async def send_cog_help(self, cog):
        ctx = self.context
        title = cog.qualified_name or "No"
        hcogmbed = HelpEmbed(
            title=title,
            description=cog.description or "No help found..."
        )
        hcogmbed.set_thumbnail(url=ctx.me.avatar_url)
        hcogmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        for commands in cog.get_commands():
            hcogmbed.add_field(name=self.get_command_signature(commands), value=commands.help or "No help found...")
        await ctx.reply(embed=hcogmbed)

    # Help Group
    async def send_group_help(self, group):
        ctx= self.context
        title = self.get_command_signature(group)
        hgroupmbed = HelpEmbed(
            title=title,
            description=group.help or "No help found..."
        )
        hgroupmbed.set_thumbnail(url=ctx.me.avatar_url)
        hgroupmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        for commands in group.commands:
            hgroupmbed.add_field(name=self.get_command_signature(commands), value=commands.help or "No help found...")
        await ctx.reply(embed=hgroupmbed)

    # Help Error
    async def send_error_message(self, error):
        ctx = self.context
        herrormbed = HelpEmbed(
            title="Help Error",
            description=error
        )
        herrormbed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        herrormbed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.reply(embed=herrormbed)
