import nextcord
from nextcord.ext import commands
import datetime
import contextlib

class HelpMenu(nextcord.ui.Select):
    def __init__(self, help, mapping, homepage, emojis):
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
        options = [
            nextcord.SelectOption(label="Home", description="The main page of this menu", value="Home", emoji=":bot:878221621687640074")
        ]
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if not name.startswith("On"):
                option = nextcord.SelectOption(label=F"{name} Category [{len(commands)}]", description=description, value=name, emoji=self.emojis.get(name) if self.emojis.get(name) else '⛔')
                options.append(option)
        super().__init__(placeholder="Choose the module you want to checkout: ", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.help.context.author.id:
            await interaction.response.send_message(F"<@{interaction.user.id}> - Only <@{self.help.context.author.id}> can use that.", ephemeral=True)
            return
        if self.values[0] == self.options[0]:
            await interaction.response.send_message(F"<@{interaction.user.id}> - The options is already {self.values[0]} try something else.", ephemeral=True)
            return
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if self.values[0] == name:
                mbed = nextcord.Embed(
                    colour=0x525BC2,
                    title=F"{self.emojis.get(name) if self.emojis.get(name) else '⛔'} {name} Category [{len(commands)}]",
                    description=description,
                    timestamp=datetime.datetime.now()
                )
                for command in commands:
                    mbed.add_field(name=self.help.get_command_signature(command), value=command.help or "No help")
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=mbed)
            elif self.values[0] == "Home":
                try:
                    await interaction.response.edit_message(embed=self.homepage)
                except nextcord.InteractionResponded:
                    pass

class HelpView(nextcord.ui.View):
    def __init__(self, help, mapping, homepage, emojis):
        super().__init__()
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
        self.add_item(HelpMenu(self.help, self.mapping, self.homepage, self.emojis))
        
    async def on_timeout(self):
        await self.message.edit(view=self)

class MyHelp(commands.HelpCommand):
    def __init__(self):
        self.emojis = {
            "API": "🌐",
            "Database": "📝",
            "Fun": "🤣",
            "Moderation": "⚔",
            "Owner": "👑",
            "Setup": "❓",
            "Utility": "⚙",
            "Jishaku": "👀",
            "No": "⛔"
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
        homepage = nextcord.Embed(
            colour=0x525BC2,
            title=F"{ctx.me.display_name} <:bot:878221621687640074> Help",
            description="""```py
This is a list of all modules in the bot.
Select a module for more information.
[] means the argument is optional.
<> means the argument is required.```""",
            timestamp = ctx.message.created_at
        )
        homepage.set_thumbnail(url=ctx.me.avatar.url)
        homepage.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        usable = 0
        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands, sort=True):
                amount_commands = len(filtered_commands)
                usable += amount_commands
                name = cog.qualified_name if cog else "No"
                description = cog.description if cog else "Commands without category"
                homepage.add_field(name=F"{self.emojis.get(name) if self.emojis.get(name) else '⛔'} {name} Category [{len(commands)}]", value=description)
        view = HelpView(self, mapping, homepage, self.emojis)
        view.message = await ctx.reply(embed=homepage, view=view)
        return

    # Help Command
    async def send_command_help(self, command):
        ctx = self.context
        signature = self.get_command_signature(command)
        hcmdmbed = nextcord.Embed(
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
        await ctx.reply(embed=hcmdmbed)
        return

    # Help SubCommand Error
    async def subcommand_not_found(self, command, string):
        ctx = self.context
        hscmdmbed = nextcord.Embed(
            colour=0x525BC2,
            title="Sub Command Not Found",
            description=F"{command} - {string}",
            timestamp=ctx.message.created_at
        )
        hscmdmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        hscmdmbed.set_thumbnail(url=ctx.me.avatar.url)
        await ctx.reply(embed=hscmdmbed)
        return

    # Help Cog
    async def send_cog_help(self, cog):
        ctx = self.context
        title = F"{self.emojis.get(cog.qualified_name) if self.emojis.get(cog.qualified_name) else ''} {cog.qualified_name}" or "No"
        hcogmbed = nextcord.Embed(
            colour=0x525BC2,
            title=title,
            description=cog.description or "No help found...",
            timestamp=ctx.message.created_at
        )
        hcogmbed.set_thumbnail(url=ctx.me.avatar.url)
        hcogmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        for command in cog.get_commands():
            hcogmbed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
        await ctx.reply(embed=hcogmbed)
        return

    # Help Group
    async def send_group_help(self, group):
        ctx = self.context
        title = self.get_command_signature(group)
        hgroupmbed = nextcord.Embed(
            colour=0x525BC2,
            title=title,
            description=group.help or "No help found...",
            timestamp=ctx.message.created_at
        )
        hgroupmbed.set_thumbnail(url=ctx.me.avatar.url)
        hgroupmbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        for command in group.commands:
            hgroupmbed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
        await ctx.reply(embed=hgroupmbed)
        return

    # Help Error
    async def send_error_message(self, error):
        if error == None:
            return
        ctx = self.context
        herrormbed = nextcord.Embed(
            colour=0x525BC2,
            title="Help Error",
            description=error,
            timestamp=ctx.message.created_at
        )
        herrormbed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        herrormbed.set_thumbnail(url=ctx.me.avatar.url)
        await ctx.reply(embed=herrormbed)
        return

