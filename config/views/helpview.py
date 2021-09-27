import discord

class PaginatorView(discord.ui.View):
    def __init__(self, help, mapping, homepage):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.embed = 0
        self.embeds = [self.homepage]
        def gts(command):
            return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}"
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            embed = discord.Embed(
                colour=self.context.bot.colour,
                title=name,
                description=", ".join(gts(cmd) for cmd in cmds),
                timestamp=self.context.message.created_at
            )
            self.embeds.append(embed)
        
    @discord.ui.button(emoji="⏮", style=discord.ButtonStyle.blurple)
    async def back(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.embed -= 1
        await interaction.response.edit_message(embed=self.embeds[self.embed])
    
    @discord.ui.button(emoji="⏹", style=discord.ButtonStyle.red)
    async def delete(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

    @discord.ui.button(emoji="⏯", style=discord.ButtonStyle.green)
    async def back(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.homepage)

    @discord.ui.button(emoji="⏭", style=discord.ButtonStyle.blurple)
    async def back(self, button:discord.ui.Button, interaction:discord.Interaction):
        self.embed += 1
        await interaction.response.edit_message(embed=self.embeds[self.embed])

    async def on_timeout(self):
        try:
            for item in self.children:
                if isinstance(item, discord.ui.Select):
                    item.placeholder = "Disabled due to timeout..."
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
        icheckmbed.set_thumbnail(url=self.help.context.me.avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
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
            return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}"
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.values[0] == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                    description=F"{description}\n\n",
                    timestamp=self.help.context.message.created_at
                )
                for command in cmds:
                    mbed.description += F"{gts(command)}\n"
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                mbed.set_footer(text="<> is required | [] is optional")
                await interaction.response.edit_message(embed=mbed)
        if self.values[0] == "Home":
            await interaction.response.edit_message(embed=self.homepage)

class SelectView(discord.ui.View):
    def __init__(self, help, mapping, homepage):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        options = [
            discord.SelectOption(emoji="🏠", label=F"Home", description="The Hompage of this help", value="Home"),
        ]
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category..."
            if not name.startswith("On"):
                option = discord.SelectOption(emoji=self.help.emojis.get(name) if self.help.emojis.get(name) else '❓', label=name, description=description, value=name)
                options.append(option)
        self.add_item(SelectUI(placeholder="Where do you want to go...", options=options, min_values=1, max_values=1, view=self))
        self.add_item(discord.ui.Button(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(discord.ui.Button(emoji="🍩", label="Support Server", url="https://discord.gg/bWnjkjyFRz"))

    @discord.ui.button(emoji="💣", label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

    async def on_timeout(self):
        try:
            for item in self.children:
                if isinstance(item, discord.ui.Select):
                    item.placeholder = "Disabled due to timeout..."
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
        def gts(command):
            return F"• **{command.qualified_name}** {command.signature} - {command.help or 'No help found...'}"
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            cmds = cog.walk_commands() if cog else commands
            if self.custom_id == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.colour,
                    title=F"{self.help.emojis.get(name) if self.help.emojis.get(name) else '❓'} {name} Category",
                    description=F"{description}\n\n",
                    timestamp=self.help.context.message.created_at
                )
                for command in cmds:
                    mbed.description += F"{gts(command)}\n"
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                mbed.set_footer(text="<> is required | [] is optional")
                await interaction.response.edit_message(embed=mbed)
        if self.custom_id == "Home":
            await interaction.response.edit_message(embed=self.homepage)
        if self.custom_id == "Delete":
            await interaction.message.delete()

class ButtonsView(discord.ui.View):
    def __init__(self, help, mapping, homepage):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
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
            for item in self.children:
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
