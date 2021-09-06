import discord
from discord.ext import commands
import datetime
import contextlib

class HelpMenu(discord.ui.Select):
    def __init__(self, help, mapping, homepage, emojis):
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
        options = [
            discord.SelectOption(label="Home", description="The homepage of this menu", value="Home", emoji=":botbrevity:878221621687640074")
        ]
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if not name.startswith("On"):
                option = discord.SelectOption(label=F"{name} Category [{len(commands)}]", description=description, value=name, emoji=self.emojis.get(name) if self.emojis.get(name) else '❓')
                options.append(option)
        super().__init__(placeholder="Choose the module you want to checkout: ", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if self.values[0] == name:
                mbed = discord.Embed(
                    colour=0x525BC2,
                    title=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} Category [{len(commands)}]",
                    description=description,
                    timestamp=self.help.context.message.created_at
                )
                for command in commands:
                    mbed.add_field(name=self.help.get_command_signature(command), value=command.help or "No help")
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=mbed)
            elif self.values[0] == "Home":
                try:
                    await interaction.response.edit_message(embed=self.homepage)
                except discord.InteractionResponded:
                    pass

class HelpView(discord.ui.View):
    def __init__(self, help, mapping, homepage, emojis):
        super().__init__()
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
        self.add_item(HelpMenu(self.help, self.mapping, self.homepage, self.emojis))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.help.context.author.id:
            return True

        await interaction.response.send_message(F"<@{interaction.user.id}> - Only <@{self.help.context.author.id}> can use that.", ephemeral=True)

class MyHelp(commands.HelpCommand):
    def __init__(self):
        self.emojis = {
            "API": "🌎",
            "Database": "📝",
            "Fun": "🤣",
            "Moderation": "💀",
            "Owner": "👑",
            "Setup": "🔮",
            "Utility": "🧰",
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
            colour=0x525BC2,
            title=F"{ctx.me.display_name} <:botbrevity:878221621687640074> Help",
            description=F"My prefix here is `{ctx.clean_prefix}`!\nThis is a list of all modules in the bot.\nSelect a module for more information.",
            timestamp=ctx.message.created_at
        )
        homepage.set_thumbnail(url=ctx.me.avatar.url)
        homepage.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        usable = 0
        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands, sort=True):
                usable += len(filtered_commands)
        homepage.add_field(name="Usable:", value=usable)
        homepage.add_field(name="Arguments:", value="[] means the argument is optional.\n<> means the argument is required.")
        view = HelpView(self, mapping, homepage, self.emojis)
        await ctx.send(embed=homepage, view=view)
        return

    # Help Cog
    async def send_cog_help(self, cog):
        ctx = self.context
        name = cog.qualified_name if cog else "No"
        description = cog.description if cog else "Commands without category"
        hcogmbed = discord.Embed(
            colour=0x525BC2,
            title=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} [{len(cog.get_commands())}]",
            description=description,
            timestamp=ctx.message.created_at
        )
        if filtered_commands := await self.filter_commands(cog.get_commands()):
            for command in filtered_commands:
                hcogmbed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
        hcogmbed.set_thumbnail(url=ctx.me.avatar.url)
        hcogmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=hcogmbed)
        return

    # Help Command
    async def send_command_help(self, command):
        ctx = self.context
        signature = self.get_command_signature(command)
        hcmdmbed = discord.Embed(
            colour=0x525BC2,
            title=signature,
            description=command.help or "No help found...",
            timestamp=ctx.message.created_at
        )
        hcmdmbed.set_thumbnail(url=ctx.me.avatar.url)
        hcmdmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        if cog := command.cog:
            hcmdmbed.add_field(name="Category", value=F"{self.emojis.get(cog.qualified_name) if self.emojis.get(cog.qualified_name) else ''} {cog.qualified_name}")
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
            colour=0x525BC2,
            title=self.get_command_signature(group),
            description=group.help or "No help found...",
            timestamp=ctx.message.created_at
        )
        hgroupmbed.set_thumbnail(url=ctx.me.avatar.url)
        hgroupmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        for command in group.commands:
            hgroupmbed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
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
            colour=0x525BC2,
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
            colour=0x525BC2,
            title="Help Error",
            description=error,
            timestamp=ctx.message.created_at
        )
        herrormbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        herrormbed.set_thumbnail(url=ctx.me.avatar.url)
        await ctx.send(embed=herrormbed)
        return

