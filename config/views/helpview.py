import discord

class PaginatorView(discord.ui.View):
    def __init__(self, help, mapping):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = discord.Embed(
            colour=self.help.context.bot.colour,
            title=F"{self.help.context.me.name}'s Help",
            description="For more help or information use the buttons to change pages.",
            timestamp=self.help.context.message.created_at
        )
        self.page = 0
        self.mbeds = [self.homepage]
        self.add_item(item=discord.ui.Button(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(item=discord.ui.Button(emoji="🍩", label="Support Server", url="https://discord.gg/bWnjkjyFRz"))
        def gts(command):
            return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}\n"
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if not name.startswith("On"):
                mbed = discord.Embed(
                        colour=self.help.context.bot.colour,
                        title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                        description=F"{description}\n\n{''.join(gts(command) for command in commands)}",
                        timestamp=self.help.context.message.created_at
                )
                mbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
                mbed.set_author(name=self.help.context.author, icon_url=self.help.context.author.display_avatar.url)
                mbed.set_footer(text=F"<> is required | [] is optional | Page: {len(self.mbeds)}")
                self.mbeds.append(mbed)
        print(len(self.mbeds))

    @discord.ui.button(emoji="⏯", style=discord.ButtonStyle.green)
    async def home(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.homepage)

    @discord.ui.button(emoji="⏮", style=discord.ButtonStyle.blurple, disabled=True)
    async def previous(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.page -= 1
        if self.page != 0: button.disabled = False
        await interaction.response.edit_message(embed=self.mbeds[self.page], view=button.view)
    
    @discord.ui.button(emoji="⏹", style=discord.ButtonStyle.red)
    async def delete(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

    @discord.ui.button(emoji="⏭", style=discord.ButtonStyle.blurple)
    async def next(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.page += 1
        if self.page == 10: button.disabled = True
        await interaction.response.edit_message(embed=self.mbeds[self.page], view=button.view)

    async def on_timeout(self):
        try:
            await self.message.edit(view=None)
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
        icheckmbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False

class SelectUI(discord.ui.Select):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.help = view.help
        self.mapping = view.mapping
        self.homepage = view.homepage

    async def callback(self, interaction:discord.Interaction):
        def gts(command):
            return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}\n"
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.values[0] == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                    description=F"{description}\n\n{''.join(gts(command) for command in cmds)}",
                    timestamp=self.help.context.message.created_at
                )
                mbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                mbed.set_footer(text="<> is required | [] is optional")
                await interaction.response.edit_message(embed=mbed)
        if self.values[0] == "Home":
            await interaction.response.edit_message(embed=self.homepage)

class SelectView(discord.ui.View):
    def __init__(self, help, mapping):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = discord.Embed(
            colour=self.help.context.bot.colour,
            title=F"{self.help.context.me.name}'s Help",
            description="For more help or information use the menu.",
            timestamp=self.help.context.message.created_at
        )
        options = []
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category..."
            if not name.startswith("On"):
                option = discord.SelectOption(emoji=self.help.emojis.get(name) if self.help.emojis.get(name) else '❓', label=name, description=description, value=name)
                options.append(option)
        self.add_item(item=SelectUI(placeholder="Where do you want to go...", options=options, min_values=1, max_values=1, view=self))
        self.add_item(item=discord.ui.Button(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(item=discord.ui.Button(emoji="🍩", label="Support Server", url="https://discord.gg/bWnjkjyFRz"))

    @discord.ui.button(emoji="🏠", label=F"Home", style=discord.ButtonStyle.green)
    async def home(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.homepage)

    @discord.ui.button(emoji="💣", label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

    async def on_timeout(self):
        try:
            for item in self.children:
                if isinstance(item, discord.ui.Select):
                    item.placeholder = "Disabled due to being timed out..."
                item.disabled = True
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
        icheckmbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False

class ButtonsUI(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.help = view.help
        self.mapping = view.mapping
        self.homepage = view.homepage

    async def callback(self, interaction:discord.Interaction):
        def gts(command):
            return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}\n"
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.custom_id == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                    description=F"{description}\n\n{''.join(gts(command) for command in cmds)}",
                    timestamp=self.help.context.message.created_at
                )
                mbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                mbed.set_footer(text="<> is required | [] is optional")
                await interaction.response.edit_message(embed=mbed)
        if self.custom_id == "Home":
            await interaction.response.edit_message(embed=self.homepage)
        if self.custom_id == "Delete":
            await interaction.message.delete()

class ButtonsView(discord.ui.View):
    def __init__(self, help, mapping):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = discord.Embed(
            colour=self.help.context.bot.colour,
            title=F"{self.help.context.me.name}'s Help",
            description="For more help or information use and click on the buttons.",
            timestamp=self.help.context.message.created_at
        )
        self.add_item(item=ButtonsUI(emoji="🏠", label="Home", style=discord.ButtonStyle.green, custom_id="Home", view=self))
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            if not name.startswith("On"):
                self.add_item(item=ButtonsUI(emoji=self.help.emojis.get(name), label=name, style=discord.ButtonStyle.blurple, custom_id=name, view=self))
        self.add_item(item=ButtonsUI(emoji="💣", label="Delete", style=discord.ButtonStyle.red, custom_id="Delete", view=self))
        self.add_item(item=discord.ui.Button(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(item=discord.ui.Button(emoji="🍩", label="Support Server", url="https://discord.gg/bWnjkjyFRz"))

    async def on_timeout(self):
        try:
            self.clear_items()
            self.add_item(item=discord.ui.Button(emoji="❌", label="Disabled due to timeout...", style=discord.ButtonStyle.red, disabled=True))
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
        icheckmbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False
