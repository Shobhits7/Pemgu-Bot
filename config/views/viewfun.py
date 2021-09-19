import discord

class CounterView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=5)
        self.clicks = 0
        self.clickers = ""
        self.client = client

    @discord.ui.button(emoji="🍏", style=discord.ButtonStyle.green)
    async def click(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clicks += 1
        if str(interaction.user) in self.clickers:
            pass
        else: self.clickers += F"{str(interaction.user)}\n"

    async def on_timeout(self):
        for item in self.children:
            self.clear_items()
        ontimeoutmbed = discord.Embed(
            colour=self.client.color,
            title=F"Button was clicked: {self.clicks} times",
        )
        if len(self.clickers) != 0 or self.clicks != 0:
            ontimeoutmbed.description = "People who clicked:\n"
            ontimeoutmbed.description += self.clickers
        else: ontimeoutmbed.description = "Nobody clicked the buttons"
        await self.message.edit(embed=ontimeoutmbed, view=self)
