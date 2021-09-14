import discord
from discord.ext import commands

class HelpButtons(discord.ui.Button):
    def __init__(self, help, mapping, homepage, emojis):
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
    
    async def callback(self, interaction: discord.Interaction):
        print("Something was pressed")
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if self.custom_id == name:
                mbed = discord.Embed(
                    colour=self.help.context.bot.color,
                    title=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} Category [{len(commands)}]",
                    description=F"{description}\n\n",
                    timestamp=self.help.context.message.created_at
                )
                for command in commands:
                    mbed.description += F"<:paimonkill:812299113223422012> **{self.help.get_command_signature(command)}** - {command.help or 'No help found...'}\n"
                mbed.set_thumbnail(url=self.help.context.me.avatar.url)
                mbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=mbed)
        if self.custom_id == "Home":
            await interaction.response.edit_message(embed=self.homepage)


class HelpView(discord.ui.View):
    def __init__(self, help, mapping, homepage, emojis):
        super().__init__(timeout=15)
        self.help = help
        self.mapping = mapping
        self.homepage = homepage
        self.emojis = emojis
        self.add_item(item=HelpButtons(label="🏠Home", style=discord.ButtonStyle.green, custom_id="Home"))
        for cog, commands in self.mapping.items():
            name = cog.qualified_name if cog else "No"
            description = cog.description if cog else "Commands without category"
            if not name.startswith("On"):
                self.add_item(item=HelpButtons(label=F"{self.emojis.get(name) if self.emojis.get(name) else '❓'} {name} [{len(commands)}]", style=discord.ButtonStyle.blurple, custom_id=name))

    async def on_timeout(self):
        try:
            for buttons in self.children:
                if isinstance(buttons, discord.ui.Button):
                    self.clear_items()
                    self.add_item(discord.ui.Button(label="❌Timeouted", style=discord.ButtonStyle.red, disabled = True))
                buttons.disabled = True
            await self.message.edit(view=self)
        except discord.NotFound:
            return

    @discord.ui.button(label="💣Delete", style=discord.ButtonStyle.red)
    async def delete(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()