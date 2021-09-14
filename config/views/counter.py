import discord
from discord.ext import commands

class CounterView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=5)
        self.clicks = 0
        self.clickers = ""
        self.client = client

    @discord.ui.button(label="➕1", style=discord.ButtonStyle.blurple)
    async def Plus1(self, button: discord.ui.Button, interaction: discord.Interaction):
        print("Plus 1 was pressed")
        self.clickers += F"<@{interaction.user.id}> pressed +1\n"
        self.clicks += 1
    
    @discord.ui.button(label="➖1", style=discord.ButtonStyle.red)
    async def Minus1(self, button: discord.ui.Button, interaction: discord.Interaction):
        print("Minus 1 was pressed")
        self.clickers += F"<@{interaction.user.id}> pressed -1\n"
        self.clicks += 1

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        ontimeoutmbed = discord.Embed(
            colour=self.client.color,
            title=F"Button was clicked {self.clicks} times",
            description="People who clicked:\n"
        )
        for clicker in self.clickers:
            ontimeoutmbed.description += F"{clicker}"
        await self.message.edit(embed=ontimeoutmbed, view=self)
