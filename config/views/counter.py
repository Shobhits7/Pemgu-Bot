import discord
from discord.ext import commands

class CounterView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=5)
        self.clicks = 0
        self.clickers = ""
        self.plus = 0
        self.minus = 0
        self.client = client

    @discord.ui.button(emoji="➕", style=discord.ButtonStyle.green)
    async def Plus1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clickers += F"**{interaction.user.name}** Plused\n"
        self.clicks += 1
        self.plus += 1
        button.label = F"{self.plus}"
    
    @discord.ui.button(emoji="➖", style=discord.ButtonStyle.red)
    async def Minus1(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.clickers += F"**{interaction.user.name}** Minused\n"
        self.clicks -= 1
        self.minus += 1
        button.label = F"{self.minus}"

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        ontimeoutmbed = discord.Embed(
            colour=self.client.color,
            title=F"Score: **{self.clicks}** between Pluses and Minuses",
        )
        if len(self.clickers) != 0 and self.clicks != 0:
            ontimeoutmbed.description = "People who clicked:\n"
            for clicker in self.clickers:
                ontimeoutmbed.description += F"{clicker}"
        else: ontimeoutmbed.description = "Nobody clicked the buttons"
        await self.message.edit(embed=ontimeoutmbed, view=self)
