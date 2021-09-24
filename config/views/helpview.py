import discord

class SelectUI(discord.ui.Select):
    def __init__(self, view):
        self.help = view.help
        self.mapping = view.mapping
        self.homepage = view.homepage
        options = []
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category..."
            if not name.startswith("On") and name != "Jishaku":
                option = discord.SelectOption(emoji=self.help.emojis.get(name) if self.help.emojis.get(name) else '❓', label=F"{name} Category [{len(commands)}]", description=description, value=name)
                options.append(option)
        super().__init__(placeholder="Where do you want to go...", min_values=2, max_values=6, options=options)
    async def callback(self, interaction:discord.Interaction):
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.values[0] == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category [{len(commands)}]",
                    description=F"{description}\n\n",
                    timestamp=self.help.context.message.created_at
                )
                for command in cmds:
                    mbed.description += F"• **{self.help.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=mbed)

class SelectView(discord.ui.View):
    def __init__(self, help, mapping, homepage):
        super().__init__(timeout=10)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.add_item(SelectUI(self))
        self.add_item(discord.ui.Button(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(discord.ui.Button(emoji="🍩", label="Support Guild", url="https://discord.gg/bWnjkjyFRz"))

    @discord.ui.button(emoji="🏠", label="Home", style=discord.ButtonStyle.green)
    async def home(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.homepage)

    @discord.ui.button(emoji="💣", label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

    async def on_timeout(self):
        try:
            for items in self.children:
                if isinstance(items, discord.ui.Select):
                    items.placeholder = "Disabled due to timeout..."
                items.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            return

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.help.context.author.id:
            return True
        icheckmbed = discord.Embed(
            colour=self.help.context.bot.colour,
            title="You can't use this",
            description=F"<@{interaction.user.id}> - Only <@{self.help.context.author.id}> can use that\nCause they did the command\nIf you wanted to use the command, do what they did",
            timestamp=self.help.context.message.created_at
        )
        icheckmbed.set_thumbnail(url=self.help.context.me.avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False

class ButtonsUI(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.help = view.help
        self.mapping = view.mapping
        self.homepage = view.homepage

    async def callback(self, interaction:discord.Interaction):
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.custom_id == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category [{len(commands)}]",
                    description=F"{description}\n\n",
                    timestamp=self.help.context.message.created_at
                )
                for command in cmds:
                    mbed.description += F"• **{self.help.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=mbed)
        if self.custom_id == "Home":
            await interaction.response.edit_message(embed=self.homepage)
        if self.custom_id == "Delete":
            await interaction.message.delete()


class ButtonsView(discord.ui.View):
    def __init__(self, help, mapping, homepage):
        super().__init__(timeout=10)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.add_item(item=ButtonsUI(emoji="🏠", label="Home", style=discord.ButtonStyle.green, custom_id="Home", view=self))
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            if not name.startswith("On") and name != "Jishaku":
                self.add_item(item=ButtonsUI(emoji=self.help.emojis.get(name), label=F"{name} [{len(commands)}]", style=discord.ButtonStyle.blurple, custom_id=name, view=self))
        self.add_item(item=ButtonsUI(emoji="💣",label="Delete", style=discord.ButtonStyle.red, custom_id="Delete", view=self))
        self.add_item(item=ButtonsUI(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True)), view=self))
        self.add_item(item=ButtonsUI(emoji="🍩", label="Support Guild", url="https://discord.gg/bWnjkjyFRz", view=self))

    async def on_timeout(self):
        try:
            for items in self.children:
                self.clear_items()
                self.add_item(discord.ui.Button(emoji="❌", label="Disabled due to timeout...", style=discord.ButtonStyle.red, disabled=True))
            await self.message.edit(view=self)
        except discord.NotFound:
            return

    async def interaction_check(self, interaction:discord.Interaction):
        if interaction.user.id == self.help.context.author.id:
            return True
        icheckmbed = discord.Embed(
            colour=self.help.context.bot.colour,
            title="You can't use this",
            description=F"<@{interaction.user.id}> - Only <@{self.help.context.author.id}> can use that\nCause they did the command\nIf you wanted to use the command, do what they did",
            timestamp=self.help.context.message.created_at
        )
        icheckmbed.set_thumbnail(url=self.help.context.me.avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False
