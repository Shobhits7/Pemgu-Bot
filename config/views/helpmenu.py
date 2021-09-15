import discord
from discord.ext import commands

class HelpMenu(discord.ui.Select):
    def __init__(self, view):
        self.help = view.help
        self.mapping = view.mapping
        self.homepage = view.homepage
        self.emojis = view.emojis
        options = [
            discord.SelectOption(label="Home", description="The homepage of this menu", value="Home", emoji="🏠")
        ]
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if not name.startswith("On"):
                option = discord.SelectOption(label=F"{name} Category [{len(commands)}]", description=description, value=name, emoji=self.emojis.get(name) if self.emojis.get(name) else '❓')
                options.append(option)
        super().__init__(placeholder="Where do you want to go...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if self.values[0] == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.color,
                    title=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} Category [{len(commands)}]",
                    description=F"{description}\n\n",
                    timestamp=self.help.context.message.created_at
                )
                for command in commands:
                    mbed.description += F"• **{self.help.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=mbed)
        if self.values[0] == "Home":
            await interaction.response.edit_message(embed=self.homepage)

class HelpView(discord.ui.View):
    def __init__(self, help, mapping, homepage, emojis):
        super().__init__(timeout=10)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
        self.add_item(HelpMenu(self))
        self.add_item(discord.ui.Button(emoji="🧇", label="Add Me", url=discord.utils.oauth_url(client_id=self.help.context.me.id, scopes=('bot', 'applications.commands'), permissions=discord.Permissions(administrator=True))))
        self.add_item(discord.ui.Button(emoji="🍩", label="Support Server", url="https://discord.gg/bWnjkjyFRz"))

    async def on_timeout(self):
        try:
            for items in self.children:
                if isinstance(items, discord.ui.Select):
                    items.placeholder = "Disabled due to timeout..."
                items.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            return

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id == self.help.context.author.id:
            return True
        icheckmbed = discord.Embed(
            colour=self.help.context.bot.color,
            title="You can't use this",
            description=F"<@{interaction.user.id}> - Only <@{self.help.context.author.id}> can use that\nCause they did the command\nIf you wanted to use the command, do what they did",
            timestamp=self.help.context.message.created_at
        )
        icheckmbed.set_thumbnail(url=self.help.context.me.avatar.url)
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False

    @discord.ui.button(emoji="💣", label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        deletembed = discord.Embed(
            colour=self.help.context.bot.color,
            title="Deleted the message",
            timestamp=self.help.context.message.created_at
        )
        deletembed.set_thumbnail(url=self.help.context.me.avatar.url)
        deletembed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        await interaction.message.delete()
        await interaction.response.send_message(embed=deletembed, ephemeral=True)
