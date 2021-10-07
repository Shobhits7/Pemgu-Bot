import discord

class PaginatorButtons(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.help = view.help
        self.mapping = view.mapping
        self.homepage = view.homepage
        self.page = view.page
        self.mbeds = view.mbeds

    async def callback(self, interaction:discord.Interaction):
        if self.emoji == "⏯":
            await interaction.response.edit_message(embed=self.homepage)
        if self.emoji == "⏮":
            self.page -= 1
            await interaction.response.edit_message(embed=self.mbeds[self.page], view=self.view)
        if self.emoji == "⏮" and self.page >= 0:
            self.disabled = False
            await interaction.response.edit_message(embed=self.mbeds[self.page], view=self.view)
        if self.emoji == "⏹":
            await interaction.message.delete()
        if self.emoji == "⏭":
            self.page += 1
            await interaction.response.edit_message(embed=self.mbeds[self.page], view=self.view)
        if self.emoji == "⏭" and self.page == 10:
            self.disabled = True
            await interaction.response.edit_message(embed=self.mbeds[self.page], view=self.view)

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
        self.add_item(item=PaginatorButtons(emoji="⏯", style=discord.ButtonStyle.green, view=self))
        self.add_item(item=PaginatorButtons(emoji="⏮", style=discord.ButtonStyle.blurple, disabled=True, view=self))
        self.add_item(item=PaginatorButtons(emoji="⏹", style=discord.ButtonStyle.red, view=self))
        self.add_item(item=PaginatorButtons(emoji="⏭", style=discord.ButtonStyle.blurple, view=self))
        self.add_item(item=discord.ui.Button(emoji="🧇", label="Invite", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(item=discord.ui.Button(emoji="🍩", label="Support", url="https://discord.gg/bWnjkjyFRz"))
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

    def gts(self, command):
        return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}\n"

    async def callback(self, interaction:discord.Interaction):
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.values[0] == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                    description=F"{description}\n\n{''.join(self.gts(command) for command in cmds)}",
                    timestamp=self.help.context.message.created_at
                )
                mbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                mbed.set_footer(text="<> is required | [] is optional")
                await interaction.response.edit_message(embed=mbed)

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
        self.add_item(item=discord.ui.Button(emoji="🧇", label="Invite", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(item=discord.ui.Button(emoji="🍩", label="Support", url="https://discord.gg/bWnjkjyFRz"))
        self.add_item(item=discord.ui.Button(emoji="👨‍💻", label="Github", url="https://github.com/lvlahraam/JakeTheDog-Bot"))

    @discord.ui.button(emoji="🏠", label="Home", style=discord.ButtonStyle.green)
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

    def gts(self, command):
        return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}\n"

    async def callback(self, interaction:discord.Interaction):
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.custom_id == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                    description=F"{description}\n\n{''.join(self.gts(command) for command in cmds)}",
                    timestamp=self.help.context.message.created_at
                )
                mbed.set_thumbnail(url=self.help.context.me.display_avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                mbed.set_footer(text="<> is required | [] is optional")
                await interaction.response.edit_message(embed=mbed)

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
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            if not name.startswith("On"):
                self.add_item(item=ButtonsUI(emoji=self.help.emojis.get(name), label=name, style=discord.ButtonStyle.blurple, custom_id=name, view=self))
        self.add_item(item=discord.ui.Button(emoji="🧇", label="Invite", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(item=discord.ui.Button(emoji="🍩", label="Support", url="https://discord.gg/bWnjkjyFRz"))
        self.add_item(item=discord.ui.Button(emoji="👨‍💻", label="Github", url="https://github.com/lvlahraam/JakeTheDog-Bot"))

    @discord.ui.button(emoji="🏠", label="Home", style=discord.ButtonStyle.green)
    async def home(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.homepage)

    @discord.ui.button(emoji="💣", label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

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