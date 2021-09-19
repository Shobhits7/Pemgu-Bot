import discord, collections

class CounterView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=5)
        self.clicks = 0
        self.clickers = ""
        self.client = client

    @discord.ui.button(emoji="🍏", style=discord.ButtonStyle.green)
    async def click(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clicks += 1
        if interaction.user not in self.clickers:
            self.clickers += F"{str(interaction.user)}"
        else: pass
        button.label = self.clicks

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        ontimeoutmbed = discord.Embed(
            colour=self.client.color,
            title=F"Button was clicked: {self.clicks} times",
        )
        if len(self.clickers) != 0 or self.clicks != 0:
            ontimeoutmbed.description = "People who clicked:\n"
            for clicker in self.clickers:
                ontimeoutmbed.description += F"{clicker}\n"
        else: ontimeoutmbed.description = "Nobody clicked the buttons"
        await self.message.edit(embed=ontimeoutmbed, view=self)
