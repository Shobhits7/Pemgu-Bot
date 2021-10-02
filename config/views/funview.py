import discord

class NitroButton(discord.ui.Button):
    def __init__(self, view, **kwargs):
        super().__init__(**kwargs)
        self.bot = view.bot

    async def callback(self, interaction:discord.Interaction):
        anitrombed = discord.Embed(
            colour=self.bot.colour,
            title="Somebody claimed the Nitro.",
            description=F"{interaction.user} claimed the Nitro.",
            timestamp=interaction.message.created_at
        )
        anitrombed.set_footer(text=interaction.message.author, icon_url=interaction.message.author.display_avatar.url)
        self.label = "CLAIMED"
        self.style = discord.ButtonStyle.grey
        self.disabled = True
        await interaction.response.edit_message(embed=anitrombed, view=self.view)

class NitroView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=5)
        self.bot = bot
        self.add_item(item=NitroButton(label="ACCEPT", style=discord.ButtonStyle.green, view=self))

    async def on_timeout(self):
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                if item.disabled:
                    return
                self.clear_items()
                self.add_item(discord.ui.Button(emoji="💣", label="You took so long to answer...", style=discord.ButtonStyle.red, disabled=True))
                await self.message.edit(view=self)